import sys
import json
import os
import urllib.request
import urllib.parse
import http.client

TOKEN_FILE = r"C:\Users\Admin\Downloads\ai-education-proposal\token.json"
DOCX_DIR = r"C:\Users\Admin\Downloads\ai-education-proposal\projects\한화오션\제안서\docx"

# Parent folder ID - we'll create a 한화오션 folder
# First, let's find or create a folder

def refresh_access_token(token_data):
    """Refresh the Google OAuth access token"""
    data = urllib.parse.urlencode({
        'client_id': token_data['client_id'],
        'client_secret': token_data['client_secret'],
        'refresh_token': token_data['refresh_token'],
        'grant_type': 'refresh_token'
    }).encode()
    
    req = urllib.request.Request('https://oauth2.googleapis.com/token', data=data, method='POST')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        return result['access_token']

def drive_api(method, path, token, body=None, headers=None):
    """Call Google Drive API"""
    url = f"https://www.googleapis.com{path}"
    data = None
    if body:
        data = json.dumps(body).encode()
    
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('Authorization', f'Bearer {token}')
    if body:
        req.add_header('Content-Type', 'application/json')
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def find_folder(token, folder_name, parent_id=None):
    """Find a folder by name"""
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    else:
        query += " and 'root' in parents"
    
    query_enc = urllib.parse.quote(query)
    fields = "files(id,name,parents)"
    result = drive_api('GET', f'/drive/v3/files?q={query_enc}&fields={fields}&pageSize=10', token)
    files = result.get('files', [])
    return files[0]['id'] if files else None

def create_folder(token, folder_name, parent_id=None):
    """Create a folder"""
    body = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        body['parents'] = [parent_id]
    result = drive_api('POST', '/drive/v3/files', token, body)
    return result['id']

def upload_file(token, file_path, file_name, parent_folder_id):
    """Upload a file using multipart upload"""
    boundary = '----FormBoundary7MA4YWxkTrZu0gW'
    
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    # Build multipart body manually
    metadata = json.dumps({'name': file_name, 'parents': [parent_folder_id]})
    
    body = b''
    body += f'--{boundary}\r\n'.encode()
    body += b'Content-Type: application/json; charset=UTF-8\r\n\r\n'
    body += metadata.encode() + b'\r\n'
    body += f'--{boundary}\r\n'.encode()
    body += b'Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document\r\n\r\n'
    body += file_data + b'\r\n'
    body += f'--{boundary}--\r\n'.encode()
    
    req = urllib.request.Request(
        'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart',
        data=body,
        method='POST'
    )
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Content-Type', f'multipart/related; boundary={boundary}')
    
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        return result.get('id'), result.get('name')

def main():
    # Load and refresh token
    with open(TOKEN_FILE) as f:
        token_data = json.load(f)
    
    print("Refreshing access token...")
    access_token = refresh_access_token(token_data)
    print(f"Token refreshed: {access_token[:20]}...")
    
    # Find or create 한화오션 folder
    folder_name = "한화오션"
    print(f"\nLooking for '{folder_name}' folder...")
    folder_id = find_folder(access_token, folder_name)
    
    if not folder_id:
        print(f"Creating '{folder_name}' folder...")
        folder_id = create_folder(access_token, folder_name)
        print(f"Created folder ID: {folder_id}")
    else:
        print(f"Found folder ID: {folder_id}")
    
    # Create 제안서 subfolder
    subfolder_name = "제안서"
    print(f"\nLooking for '{subfolder_name}' subfolder...")
    subfolder_id = find_folder(access_token, subfolder_name, folder_id)
    if not subfolder_id:
        print(f"Creating '{subfolder_name}' subfolder...")
        subfolder_id = create_folder(access_token, subfolder_name, folder_id)
        print(f"Created subfolder ID: {subfolder_id}")
    else:
        print(f"Found subfolder ID: {subfolder_id}")
    
    # Upload files
    files_to_upload = [
        "한화오션_AX수용성강화_제안서.docx",
        "워크숍_콘텐츠_설계안.docx",
        "FT_양성_계획서.docx",
        "운영_계획서.docx",
        "비용_제안서.docx",
    ]
    
    print(f"\n--- Uploading {len(files_to_upload)} files ---")
    uploaded = []
    for fname in files_to_upload:
        fpath = os.path.join(DOCX_DIR, fname)
        if not os.path.exists(fpath):
            print(f"SKIP: {fname} (not found)")
            continue
        
        size_kb = os.path.getsize(fpath) / 1024
        print(f"Uploading: {fname} ({size_kb:.0f}KB)...", end=' ')
        try:
            file_id, name = upload_file(access_token, fpath, fname, subfolder_id)
            print(f"OK (ID: {file_id[:12]}...)")
            uploaded.append(fname)
        except Exception as e:
            print(f"FAIL: {e}")
    
    print(f"\n=== Done: {len(uploaded)}/{len(files_to_upload)} files uploaded ===")
    print(f"\nGoogle Drive folder:")
    print(f"https://drive.google.com/drive/folders/{subfolder_id}")

if __name__ == '__main__':
    main()
