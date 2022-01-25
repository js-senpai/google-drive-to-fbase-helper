import os
import re


class TransportFilesService:
    def __init__(self, firebase_service, gdrive_service, files_path=''):
        self.firebase_service = firebase_service
        self.gdrive_service = gdrive_service.drive
        self.files_path = files_path

    def start(self):
        file_list = self.gdrive_service.ListFile(
            {'q': "title='Resource' and mimeType='application/vnd.google-apps.folder'"}).GetList()
        if len(file_list):
            parent_id = ''
            for parent in file_list:
                parent_id = parent['id']
                print(f"Parent folder name: {parent['title']}")
            if parent_id:
                get_subfolders = self.gdrive_service.ListFile({'q': f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder'"}).GetList()
                if len(get_subfolders):
                    filtered_files = []
                    for child in get_subfolders:
                        get_files = self.gdrive_service.ListFile(
                            {'q': f"'{child['id']}' in parents"}).GetList()
                        print(f"Subfolder name: {child['title']}")
                        if len(get_files):
                            for file in get_files:
                                get_folder_name = re.findall('([0-9]+)_', file['title'], flags=re.IGNORECASE)
                                print(f"File name: {file['title']}")
                                if len(get_folder_name):
                                    filtered_files.append({
                                        'parent_id': child['id'],
                                        'folder_name': get_folder_name[0],
                                        'id': file['id'],
                                        'name': file['title'],
                                        'mimeType': file['mimeType']
                                    })
                                else:
                                    print('Dont find title for file')
                        else:
                            print(f"Files not found in subfolder {child['title']}")
                    if len(filtered_files):
                        for filtered_file in filtered_files:
                            get_file = self.gdrive_service.CreateFile({'id': filtered_file['id']})
                            get_file.GetContentFile(f"{self.files_path}/{filtered_file['name']}")
                            path_to_file = f"{self.files_path}/{filtered_file['name']}"
                            self.firebase_service.upload_files(filtered_file['folder_name'], filtered_file['name'],
                                                               path_to_file, filtered_file['mimeType'])
                            # Remove file
                            os.remove(path_to_file)
                        print('Files successfully moved')
                    else:
                        print('Filtered files array is empty')
                else:
                    print('Json folder not found in Resource folder')
            else:
                print('Subfolders not found in Resource folder')
        else:
            print('Resource folder not found.')
