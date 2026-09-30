"""Read-only scheduled production preflight. Never invokes rendering or paid APIs."""
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CALENDAR = '1xAELwjFzWvvUYo_H0NcTujVqLJm9VxSiAF2M1z7BPDo'
RENDERS = '1Zu-JCivNtPf877-WwEonF4ybWihT1dgx'
ROOT = Path(__file__).resolve().parents[1]


def publish_date(value):
    if isinstance(value, (int, float)):
        return (dt.datetime(1899, 12, 30) + dt.timedelta(days=value)).date()
    text = str(value).strip()
    try:
        return dt.date.fromisoformat(text)
    except ValueError:
        return dt.datetime.strptime(text, '%b %d, %Y').date()


def select_episode(values):
    if not values:
        raise ValueError('Calendar returned no header.')
    headers = {re.sub(r'[^a-z]', '', str(v).lower()): i for i, v in enumerate(values[0])}
    if not {'videoid', 'publishdate', 'status'}.issubset(headers):
        raise ValueError('Calendar columns do not match Video ID, Publish Date and Status.')
    episodes, seen = [], set()
    for number, row in enumerate(values[1:], 8):
        def cell(key):
            index = headers[key]
            return row[index] if len(row) > index else ''
        episode = str(cell('videoid')).strip().upper()
        if not episode:
            continue
        if not re.fullmatch(r'V\d{2,3}', episode) or episode in seen:
            raise ValueError('Invalid or duplicated video ID in calendar.')
        seen.add(episode)
        status = str(cell('status')).strip().lower()
        if status == 'in progress':
            return {'state': 'busy', 'episode': episode}
        if status == 'queued':
            try:
                date = publish_date(cell('publishdate'))
            except (ValueError, OverflowError):
                raise ValueError('A queued episode has an invalid publish date.') from None
            episodes.append((date, episode, number))
    if not episodes:
        return {'state': 'idle'}
    date, episode, number = min(episodes)
    return {'state': 'selected', 'episode': episode, 'row': number, 'publish_date': date.isoformat()}


def preflight(selection, files, root=ROOT):
    result = dict(selection)
    result['mode'] = 'monitor-only'
    if selection['state'] != 'selected':
        return result
    episode = selection['episode'].lower()
    pattern = re.compile(r'(?<![a-z0-9])' + re.escape(episode) + r'(?![a-z0-9])', re.I)
    existing = [f for f in files if f.get('mimeType') == 'video/mp4' and (
        f.get('appProperties', {}).get('creatorOsEpisode', '').lower() == episode
        or pattern.search(f.get('name', '')))]
    blockers = []
    if existing:
        blockers.append('An episode MP4 already exists in Renders; reconcile its calendar status before production.')
    request_path = root / 'render-requests' / (episode + '.json')
    if not request_path.is_file():
        blockers.append('Episode render request and production pipeline are missing.')
    else:
        request = json.loads(request_path.read_text())
        if request.get('episode', '').lower() != episode or not request.get('requestId') or request.get('status') != 'ready':
            blockers.append('Episode render request is not ready.')
    blockers.append('Production execution is not implemented in this monitor; paid AI calls are disabled.')
    result.update({'existing_episode_masters': len(existing), 'blockers': blockers, 'production_started': False})
    return result


class Google:
    def __init__(self):
        names = ('GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET', 'GOOGLE_REFRESH_TOKEN')
        if any(not os.environ.get(n, '').strip() for n in names):
            raise RuntimeError('Required Google Actions secrets are missing.')
        body = urllib.parse.urlencode(dict(client_id=os.environ[names[0]].strip(), client_secret=os.environ[names[1]].strip(), refresh_token=os.environ[names[2]].strip(), grant_type='refresh_token')).encode()
        response = self.request('https://oauth2.googleapis.com/token', body=body)
        self.token = response.get('access_token')
        if not self.token:
            raise RuntimeError('OAuth refresh did not return an access token.')
        if os.environ.get('GITHUB_ACTIONS'):
            print('::add-mask::' + self.token)

    def request(self, url, body=None):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'} if body else {}
        if hasattr(self, 'token'):
            headers['Authorization'] = 'Bearer ' + self.token
        for attempt in range(3):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, data=body, headers=headers), timeout=30) as r:
                    return json.load(r)
            except urllib.error.HTTPError as error:
                if error.code not in (429, 500, 502, 503, 504) or attempt == 2:
                    raise RuntimeError('Google request failed (HTTP ' + str(error.code) + '). Check API enablement, credentials and account access.') from None
            except (urllib.error.URLError, TimeoutError):
                if attempt == 2:
                    raise RuntimeError('Google connection failed after two retries.') from None
            time.sleep(2 ** attempt)

    def calendar(self):
        params = urllib.parse.urlencode({'valueRenderOption': 'UNFORMATTED_VALUE', 'dateTimeRenderOption': 'SERIAL_NUMBER'})
        path = urllib.parse.quote("'Content Calendar'!A7:Q1000", safe='')
        return self.request('https://sheets.googleapis.com/v4/spreadsheets/' + CALENDAR + '/values/' + path + '?' + params).get('values', [])

    def renders(self):
        files, page = [], None
        while True:
            params = {'q': "'" + RENDERS + "' in parents and trashed = false", 'pageSize': 1000, 'fields': 'nextPageToken,files(id,name,mimeType,appProperties)'}
            if page:
                params['pageToken'] = page
            result = self.request('https://www.googleapis.com/drive/v3/files?' + urllib.parse.urlencode(params))
            files.extend(result.get('files', []))
            page = result.get('nextPageToken')
            if not page:
                return files
            if len(files) >= 10000:
                raise RuntimeError('Render folder exceeds monitor scan limit; refusing an incomplete duplicate check.')


def main():
    google = Google()
    result = preflight(select_episode(google.calendar()), google.renders())
    print(json.dumps(result, indent=2))
    text = '## Creator OS daily queue check\n\nMode: monitor only. No paid AI calls or production writes.\n\n'
    text += 'State: ' + result['state'] + '\n\n'
    if result.get('episode'):
        text += 'Episode: ' + result['episode'] + '\n\n'
    for blocker in result.get('blockers', []):
        text += '- ' + blocker + '\n'
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        Path(os.environ['GITHUB_STEP_SUMMARY']).write_text(text)


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, ValueError, KeyError, IndexError):
        # Do not leak spreadsheet values, Google responses or credential material.
        print('Queue check failed. Check Google access, calendar IDs/dates, and render request JSON. No production started.', file=sys.stderr)
        sys.exit(1)
