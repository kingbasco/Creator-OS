"""Deliver V04 media using a persisted reserved Drive ID; never changes sharing."""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

spec = importlib.util.spec_from_file_location('calendar_worker', Path(__file__).with_name('calendar-worker.py'))
worker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worker)
ASSETS = '18BvGNEE4fYiJLfdsZXLpsenSMFWvhd1X'
DRIVE = 'https://www.googleapis.com/drive/v3/files'


def verify_media(path, final=False):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)], capture_output=True, text=True, check=True)
    media = json.loads(result.stdout)
    video = next((s for s in media['streams'] if s['codec_type'] == 'video'), {})
    size = (2160, 3840) if final else (1080, 1920)
    if (video.get('width'), video.get('height')) != size or video.get('codec_name') != 'h264' or video.get('r_frame_rate') != '30/1':
        raise RuntimeError('Media does not match the expected dimensions, H.264 and 30 fps.')
    duration = float(media['format']['duration'])
    if not 65 <= duration <= 110:
        raise RuntimeError('Episode duration is outside the 65–110 second delivery limit.')
    if final:
        audio = next((s for s in media['streams'] if s['codec_type'] == 'audio'), {})
        if audio.get('codec_name') != 'aac' or audio.get('sample_rate') != '48000' or audio.get('channels') != 2:
            raise RuntimeError('Final master must have 48 kHz stereo AAC narration.')
        report = json.loads(path.with_name('v04-media-qa.json').read_text())
        if report.get('sha256') != hashlib.sha256(path.read_bytes()).hexdigest():
            raise RuntimeError('Final QA report is not bound to the supplied media file.')
        qa = report['loudness']
        if abs(float(qa['input_i']) + 14) > 1 or float(qa['input_tp']) > -1.3:
            raise RuntimeError('Final loudness QA failed.')
    subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(path), '-f', 'null', '-'], check=True, capture_output=True)
    return duration


class API:
    def __init__(self):
        self.google = worker.Google()

    def call(self, url, method='GET', body=None, mime='application/json', extra=None, missing=False):
        headers = {'Authorization': 'Bearer ' + self.google.token, 'Content-Type': mime}
        headers.update(extra or {})
        try:
            with urllib.request.urlopen(urllib.request.Request(url, data=body, method=method, headers=headers), timeout=55) as r:
                data = r.read()
                return (json.loads(data) if data else {}, dict(r.headers))
        except urllib.error.HTTPError as error:
            if missing and error.code == 404:
                return None, {}
            raise RuntimeError('Drive/Sheets operation failed (HTTP ' + str(error.code) + '). No completion claimed.') from None
        except (urllib.error.URLError, TimeoutError):
            raise RuntimeError('Drive/Sheets connection interrupted. Retry with the same request ID.') from None

    def get(self, file_id):
        params = urllib.parse.urlencode({'fields': 'id,size,md5Checksum,parents,trashed,mimeType,appProperties'})
        return self.call(DRIVE + '/' + file_id + '?' + params, missing=True)[0]

    def matches(self, request_id):
        params = {'q': "'" + ASSETS + "' in parents and trashed=false and appProperties has { key='creatorOsRequest' and value='" + request_id + "' } and appProperties has { key='creatorOsKind' and value='delivery-state' }", 'fields': 'files(id),nextPageToken', 'pageSize': 100}
        result = self.call(DRIVE + '?' + urllib.parse.urlencode(params))[0]
        if result.get('nextPageToken') or len(result.get('files', [])) > 1:
            raise RuntimeError('Multiple delivery states found. Reconcile them before continuing.')
        return result.get('files', [])

    def checkpoint(self, request_id, digest, mode, size):
        matches = self.matches(request_id)
        if matches:
            state = self.call(DRIVE + '/' + matches[0]['id'] + '?alt=media')[0]
            if state['sha256'] != digest or state['mode'] != mode or state['size'] != size:
                raise RuntimeError('This request ID belongs to different media. Use a new revision request ID.')
            return state
        ids = self.call(DRIVE + '/generateIds?count=2&space=drive&type=files')[0]['ids']
        state = {'requestId': request_id, 'episode': 'V04', 'mode': mode, 'sha256': digest, 'size': size, 'fileId': ids[1]}
        metadata = {'id': ids[0], 'name': request_id + '-delivery-state.json', 'parents': [ASSETS], 'mimeType': 'application/json', 'appProperties': {'creatorOsRequest': request_id, 'creatorOsKind': 'delivery-state'}}
        boundary = 'creatoros_deliver_checkpoint'
        body = ('--' + boundary + '\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n' + json.dumps(metadata) + '\r\n--' + boundary + '\r\nContent-Type: application/json\r\n\r\n' + json.dumps(state) + '\r\n--' + boundary + '--\r\n').encode()
        for attempt in range(3):
            try:
                self.call('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart', 'POST', body, 'multipart/related; boundary=' + boundary)
                break
            except RuntimeError:
                if not self.get(ids[0]):
                    if attempt == 2:
                        raise
                    time.sleep(2 ** attempt)
        stored = self.call(DRIVE + '/' + ids[0] + '?alt=media')[0]
        if stored != state:
            raise RuntimeError('Delivery checkpoint readback failed.')
        return state

    def upload(self, path, state, folder):
        checksum = hashlib.md5(path.read_bytes()).hexdigest()
        def verified(item):
            return item and not item.get('trashed') and item.get('mimeType') == 'video/mp4' and int(item.get('size', -1)) == state['size'] and item.get('md5Checksum') == checksum and folder in item.get('parents', [])
        existing = self.get(state['fileId'])
        if existing:
            if not verified(existing):
                raise RuntimeError('Reserved Drive file differs from the expected media; refusing to replace it.')
            return existing['id']
        metadata = {'id': state['fileId'], 'name': path.name, 'mimeType': 'video/mp4', 'parents': [folder], 'appProperties': {'creatorOsEpisode': 'V04', 'creatorOsRequest': state['requestId'], 'creatorOsKind': state['mode'], 'creatorOsSha256': state['sha256']}}
        for attempt in range(3):
            try:
                _, headers = self.call('https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable', 'POST', json.dumps(metadata).encode(), extra={'X-Upload-Content-Type': 'video/mp4', 'X-Upload-Content-Length': str(state['size'])})
                session = headers.get('Location') or headers.get('location')
                if not session or not session.startswith('https://www.googleapis.com/'):
                    raise RuntimeError('Invalid Drive upload session.')
                self.call(session, 'PUT', path.read_bytes(), 'video/mp4')
            except RuntimeError:
                if not verified(self.get(state['fileId'])):
                    if attempt == 2:
                        raise
                    time.sleep(2 ** attempt)
                    continue
            item = self.get(state['fileId'])
            if not verified(item):
                raise RuntimeError('Drive checksum, size or destination verification failed.')
            return item['id']
        raise RuntimeError('Upload did not complete.')

    def calendar_update(self, link, final):
        # Re-read IDs, header, status and validation immediately before a content-only update.
        params = urllib.parse.urlencode({'ranges': "'Content Calendar'!A7:P1000", 'includeGridData': 'true', 'fields': 'sheets(properties(sheetId),data(startRow,rowData(values(userEnteredValue,dataValidation))))'})
        sheet = self.call('https://sheets.googleapis.com/v4/spreadsheets/' + worker.CALENDAR + '?' + params)[0]['sheets'][0]
        rows = sheet['data'][0]['rowData']
        def text(row, col):
            values = row.get('values', [])
            return values[col].get('userEnteredValue', {}).get('stringValue', '') if len(values) > col else ''
        if text(rows[0], 0) != 'Video ID' or text(rows[0], 14) != 'Next Action' or text(rows[0], 15) != 'Status':
            raise RuntimeError('Calendar header changed; refusing the update.')
        matches = [(i, r) for i, r in enumerate(rows) if text(r, 0).upper() == 'V04']
        if len(matches) != 1:
            raise RuntimeError('V04 calendar row is missing or duplicated.')
        i, row = matches[0]
        if text(row, 15) in ('Ready for review', 'Approved', 'Scheduled', 'Published'):
            print('Completed calendar status preserved; verified delivery link is in the Actions summary.')
            return
        action = 'Ready' if final else 'Review Prototype'
        changed = [(14, action)] + ([(15, 'Ready for review')] if final else [])
        for col, value in changed:
            condition = row['values'][col].get('dataValidation', {}).get('condition', {})
            if condition and (condition.get('type') != 'ONE_OF_LIST' or value not in [v.get('userEnteredValue') for v in condition.get('values', [])]):
                raise RuntimeError('Calendar validation does not allow the intended status/action.')
        values = [{'userEnteredValue': {'stringValue': action}, 'note': ('Final master, technical QA passed; human review pending: ' if final else 'Silent motion preview; narration pending: ') + link}]
        index = sheet['data'][0].get('startRow', 6) + i
        requests = [{'updateCells': {'range': {'sheetId': sheet['properties']['sheetId'], 'startRowIndex': index, 'endRowIndex': index + 1, 'startColumnIndex': 14, 'endColumnIndex': 15}, 'rows': [{'values': values}], 'fields': 'userEnteredValue,note'}}]
        if final:
            requests.append({'updateCells': {'range': {'sheetId': sheet['properties']['sheetId'], 'startRowIndex': index, 'endRowIndex': index + 1, 'startColumnIndex': 15, 'endColumnIndex': 16}, 'rows': [{'values': [{'userEnteredValue': {'stringValue': 'Ready for review'}}]}], 'fields': 'userEnteredValue'}})
        body = {'requests': requests}
        self.call('https://sheets.googleapis.com/v4/spreadsheets/' + worker.CALENDAR + ':batchUpdate', 'POST', json.dumps(body).encode())
        check = self.call('https://sheets.googleapis.com/v4/spreadsheets/' + worker.CALENDAR + '/values/' + urllib.parse.quote("'Content Calendar'!O" + str(index + 1) + ':P' + str(index + 1), safe=''))[0]['values'][0]
        if check[0] != action or (final and check[1] != 'Ready for review'):
            raise RuntimeError('Calendar readback failed; uploaded file is preserved for recovery.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, type=Path)
    parser.add_argument('--request-id', required=True)
    parser.add_argument('--mode', choices=['preview', 'final'], default='preview')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if not re.fullmatch(r'v04-[a-z0-9-]{1,80}', args.request_id):
        raise RuntimeError('Invalid V04 delivery request ID.')
    duration = verify_media(args.file, args.mode == 'final')
    size = args.file.stat().st_size
    if size > 256 * 1024 * 1024:
        raise RuntimeError('File exceeds this delivery worker’s 256 MB limit.')
    digest = hashlib.sha256(args.file.read_bytes()).hexdigest()
    if args.dry_run:
        print('Delivery preflight passed: ' + str(round(duration, 2)) + ' seconds. No Google writes.')
        return
    api = API()
    state = api.checkpoint(args.request_id, digest, args.mode, size)
    file_id = api.upload(args.file, state, worker.RENDERS if args.mode == 'final' else ASSETS)
    link = 'https://drive.google.com/file/d/' + file_id + '/view'
    api.calendar_update(link, args.mode == 'final')
    report = {'episode': 'V04', 'mode': args.mode, 'requestId': args.request_id, 'fileId': file_id, 'link': link, 'sha256': digest, 'verified': True}
    args.file.with_name('v04-delivery.json').write_text(json.dumps(report, indent=2))
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as out:
            out.write('\n## Verified Drive delivery\n\n[' + args.mode + ' video](' + link + ')\n\n' + ('Narration is pending; episode is not complete.' if args.mode == 'preview' else 'Technical QA passed; human review pending.') + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    try:
        main()
    except RuntimeError as error:
        print('Delivery failed: ' + str(error), file=sys.stderr)
        sys.exit(1)
    except (ValueError, KeyError, subprocess.CalledProcessError, OSError):
        print('Delivery failed. No successful completion claimed. Retry the same request ID; reserved files are preserved.', file=sys.stderr)
        sys.exit(1)
