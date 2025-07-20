from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import json

# -----------------------------
# Configuration
# -----------------------------
SERVICE_ACCOUNT_FILE = json.loads(os.environ['SERVICE_ACCOUNT_JSON'])
SCOPES = ['https://www.googleapis.com/auth/drive']
CSV_FILE = 'lahore_aqi_iqair.csv'
FOLDER_ID = '100x3cRbI-JzrNAKjhBrnnYR_5ZUktJQZ'

def upload_to_drive():
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build('drive', 'v3', credentials=creds)

        if not os.path.exists(CSV_FILE):
            print(f"File {CSV_FILE} not found.")
            return

        query = f"'{FOLDER_ID}' in parents and name = '{CSV_FILE}' and trashed = false"
        results = service.files().list(q=query, fields="files(id)").execute()
        files = results.get('files', [])

        media_body = MediaFileUpload(CSV_FILE, resumable=True, mimetype='text/csv')

        if files:
            # File exists, update it
            file_id = files[0]['id']
            service.files().update(fileId=file_id, media_body=media_body).execute()
            print(f"Updated existing file: {CSV_FILE}")
        else:
            file_metadata = {
                'name': CSV_FILE,
                'parents': [FOLDER_ID],
            }
            service.files().create(
                body=file_metadata,
                media_body=media_body,
                fields='id'
            ).execute()
            print(f"Uploaded new file: {CSV_FILE}")
    except Exception as e:
        print("UPLOAD TO DRIVE EXC: ", e)
        return None

if __name__ == "__main__":
    upload_to_drive()
