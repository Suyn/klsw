# -*- coding: utf-8 -*-
from uuid import uuid4
from module.files.files_module import Files
from datetime import datetime


def upload_files_lib(self, files):
    """处理上传的所有文件"""
    for file in files:
        file_result = save_file(self, file)
    return file_result


def save_file(self, file):
    """处理单个文件"""
    files_ext = file['filename'].split('.')[-1]
    files_type = ['zip', 'rar', '7z', 'gz', 'tar']
    if files_ext not in files_type:
        return {'status': False, 'msg': '仅支持[zip,rar,7z,gz,tar]压缩格式','data': ''}
    uuid_num = str(uuid4())
    uuidname = uuid_num + '.%s' % files_ext
    #'sefaegaer.txt'   'sejfiajelgaeirf.jpg'
    file_content = file['body']
    old_file = Files.file_is_existed(file_content)
    if old_file is not None:
        file_path = 'http://192.168.213.128:9000/file/' + old_file.uuid
        old_uuid = old_file.uuid
        return old_uuid

    url = 'file/' + uuidname
    with open(url, 'wb') as f:
        f.write(file_content)

    file_name = file['filename']
    files = Files()
    files.users.append(self.current_user)
    files.filename = file_name
    files.uuid = uuid_num
    files.content_length = len(file_content)
    files.content_type = file['content_type']
    files.update_time = datetime.now()
    files.file_hash = file['body']
    self.db.add(files)
    self.db.commit()
    file_path = 'http://192.168.213.128:9000/file/' + files.uuid
    return uuid_num

def files_download_lib(self, files):
    uuid = files.uuid
    ext = files.filename.split('.')[-1]
    filepath = 'file/%s.%s' % (uuid, ext)
    self.set_header('Content-Type', 'application/octet-stream')
    self.set_header('Content-Disposition', 'attachment; filename=%s' % files.filename)
    with open(filepath, 'rb') as f:
        while 1:
            data = f.read(1024 * 5)
            print len(data)
            if not data:
                break
            self.write(data)  # IO
            self.flush()
    self.finish()