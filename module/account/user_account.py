# -*- coding: utf-8 -*-
from uuid import uuid4
from datetime import datetime
from string import printable

from pbkdf2 import PBKDF2
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, Integer, String, Text, Boolean, Date, DateTime, ForeignKey)

from libs.db.dbsession import Base, dbSession
from module.article.article_module import Favorite, LikeArticle
from module.files.files_module import FilesToUser

class User(Base):
    """用户表"""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    name = Column(String(50), nullable=False)

    _password = Column('password', String(64), nullable=False)
    createtime = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime)
    last_login = Column(DateTime)

    loginnum = Column(Integer, default=0)
    _locked = Column(Boolean, default=False, nullable=False)
    _avatar = Column(String(64))
    _isdelete = Column(Boolean, default=False, nullable=False)

    integral = Column(Integer, default=0)
    email = Column(String(50), unique=True, nullable=False)
    mobile = Column(String(50))
    num = Column(String(50), unique=True)
    qq = Column(String(50))

    #与文章一对多关系
    articles = relationship('Article', backref='user')

    #与点赞多对多关系
    like = relationship('Article', secondary=LikeArticle.__table__)

    #与收藏文章多对多关系
    favorite = relationship('Article', secondary=Favorite.__table__)

    #与文章评论一对多关系
    comments = relationship('Comment', backref='author')
    secondcomments = relationship('SecondComment', backref='author')

    #用户与文件的多对多关系
    user_files = relationship('Files', secondary=FilesToUser.__table__, lazy='dynamic')



    @classmethod
    def all(cls):
        return dbSession.query(cls).all()

    @classmethod
    def by_id(cls, id):
        return dbSession.query(cls).filter_by(id=id).first()

    @classmethod
    def by_email(cls, email):
        return dbSession.query(cls).filter_by(email=email).first()

    @classmethod
    def by_uuid(cls, uuid):
        return dbSession.query(cls).filter_by(uuid=uuid).first()

    @classmethod
    def by_name(cls, name):
        return dbSession.query(cls).filter_by(name=name).first()

    def _hash_password(self, password):
        return PBKDF2.crypt(password, iterations=0x2537)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        print self._hash_password(password)
        self._password = self._hash_password(password)

    def auth_password(self, other_password):
        if self._password is not None:
            return self.password == PBKDF2.crypt(other_password, self.password)
        else:
            return False

    @property
    def avatar(self): #取值
        return self._avatar if self._avatar else "default_avatar.jpg"


    @avatar.setter #赋值
    def avatar(self, image_data):
        class ValidationError(Exception):
            def __init__(self, message):
                super(ValidationError, self).__init__(message)
        if 64 < len(image_data) < 1024 * 1024:
            import imghdr
            import os
            ext = imghdr.what("", h=image_data)
            print ext
            print self.uuid
            if ext in ['png', 'jpeg', 'jpg', 'gif', 'bmp'] and not self.is_xss_image(image_data):
                if self._avatar and os.path.exists("static/avatar_images/useravatars/" + self._avatar):
                    os.unlink("static/avatar_images/useravatars/" + self._avatar)
                file_path = str("static/avatar_images/useravatars/" + self.uuid + '.' + ext)
                with open(file_path, 'wb') as f:
                    f.write(image_data)
                self._avatar = self.uuid + '.' + ext
            else:
                raise ValidationError("not in ['png', 'jpeg', 'gif', 'bmp']")
        else:
            raise ValidationError("64 < len(image_data) < 1024 * 1024 bytes")

    def is_xss_image(self, data):
        return all([char in printable for char in data[:16]])

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        assert isinstance(value, bool)
        self._locked = value

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.username,
            'last_login': self.last_login,
        }

