from pathlib import Path
from firebase_service import FirebaseService
from gdrive_service import GdriveService
from transport_files_service import TransportFilesService

files_path = Path.cwd() / './files'
firebase_secrets_path = Path.cwd() / './firebase_cred.json'
firebase_app_config_path = Path.cwd() / './firebase_app_config.json'
service = TransportFilesService(FirebaseService(firebase_secrets_path,firebase_app_config_path),GdriveService())
service.start()
