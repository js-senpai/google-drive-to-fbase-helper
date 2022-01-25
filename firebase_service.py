import json

from firebase_admin import credentials, storage, initialize_app


class FirebaseService:
    def __init__(self, firebase_secrets_path, firebase_app_config_path):
        cred = credentials.Certificate(firebase_secrets_path)
        with open(firebase_app_config_path, 'r') as file:
            # Read file
            get_data = file.read()
            initialize_app(cred, json.loads(get_data))
    def upload_files(self,folder_name = '',file_name = '',path_to_file = '',mimeType = ''):
        bucket = storage.bucket()
        blob = bucket.blob(f"{folder_name}/{file_name}")
        blob.upload_from_filename(filename=path_to_file, content_type=mimeType)
