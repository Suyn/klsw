# -*- coding: utf-8 -*-
import tornado.web

from handlers.BaseHandler.base import BaseHandler
from libs.files.files_lib import upload_files_lib, files_download_lib
from handlers.Mainhandler.main_handler import authpermission
from module.files.files_module import Files

class UploadFilesHandler(BaseHandler):
    """上传文件"""
    @authpermission
    def get(self):
        return self.render('files/upload_files.html')

    @authpermission
    def post(self):
        files = self.request.files.get('upload_files', None)
        result = upload_files_lib(self, files)
        if result['status'] is True:
            return self.write(result['msg'])
        return self.write(result['msg'])

#------------------------------------------------------------
import tornado.gen
from concurrent.futures import ThreadPoolExecutor
class DownLoadFiles(BaseHandler):
    executor = ThreadPoolExecutor(50)
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def get(self):
        uuid = self.get_argument('uuid', '')
        if uuid != '':
            file_path = Files.by_uuid(uuid)
            if file_path is None:
                self.write('该文件不存在')
            yield files_download_lib(self, file_path)
        else:
            self.write('no uuid')