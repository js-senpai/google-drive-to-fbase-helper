from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


class GdriveService:
    def __init__(self):
        self.gauth = GoogleAuth()
        self.gauth.CommandLineAuth()
        self.drive = GoogleDrive(self.gauth)
