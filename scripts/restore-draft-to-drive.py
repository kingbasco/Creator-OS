#!/usr/bin/env python3
import json
import mimetypes
import os
import sys
import urllib.parse
import urllib.request

FOLDER_ID = "1Zu-JCivNtPf877-WwEonF4ybWihT1dgx"

def request_json(url, method="GET", headers=None, data=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    with urllib.request.urlopen(req, timeout=120) as r:
        body = r.read()
        return json.loads(body.decode("utf-8")) if body else {}

def access_token():
    payload = urllib.parse.urlencode({
        "client_id": os.environ["GOOGLE_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
        "refresh_token": os.environ["GOOGLE_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    return request_json(
        "https://oauth2.googleapis.com/token",
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=payload,
    )["access_token"]

def find_existing(token, name):
    q = f"'{FOLDER_ID}' in parents and trashed = false and name = '{name.replace(chr(39), chr(92)+chr(39))}'"
    params = urllib.parse.urlencode({"q": q, "fields": "files(id,name,size,modifiedTime)"})
    out = request_json(
        "https://www.googleapis.com/drive/v3/files?" + params,
        headers={"Authorization": f"Bearer {token}"},
    )
    return out.get("files", [])

def create_metadata(token, name, mime):
    payload = json.dumps({"name": name, "mimeType": mime, "parents": [FOLDER_ID]}).encode()
    return request_json(
        "https://www.googleapis.com/drive/v3/files?fields=id,name",
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        data=payload,
    )

def upload_bytes(token, file_id, path, mime):
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        req = urllib.request.Request(
            f"https://www.googleapis.com/upload/drive/v3/files/{file_id}?uploadType=media&fields=id,name,size,webViewLink",
            data=f.read(),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": mime,
                "Content-Length": str(size),
            },
            method="PATCH",
        )
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.loads(r.read().decode("utf-8"))

def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: restore-draft-to-drive.py <path> <drive-name>")
    path, name = sys.argv[1], sys.argv[2]
    if not os.path.isfile(path):
        raise SystemExit(f"missing file: {path}")
    mime = mimetypes.guess_type(name)[0] or "video/mp4"
    token = access_token()
    existing = find_existing(token, name)
    if existing:
        file_id = existing[0]["id"]
        action = "updated"
    else:
        file_id = create_metadata(token, name, mime)["id"]
        action = "created"
    out = upload_bytes(token, file_id, path, mime)
    print(json.dumps({
        "action": action,
        "id": out.get("id", file_id),
        "name": name,
        "size": out.get("size"),
        "url": f"https://drive.google.com/file/d/{out.get('id', file_id)}/view",
    }))

if __name__ == "__main__":
    main()
