# -*- coding: utf-8 -*-
from files_handler import UploadFilesHandler, DownLoadFiles

files_handlers = [
    (r'/files/upload_files', UploadFilesHandler),
    (r'/files/download_file', DownLoadFiles),
]
