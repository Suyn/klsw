# -*- coding: utf-8 -*-
from uuid import uuid4
from datetime import datetime
from string import printable

from pbkdf2 import PBKDF2
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, Integer, String, Text,
                        Boolean, Date, DateTime, ForeignKey,
                        )

from libs.db.dbsession import Base, dbSession


class LikeArticle(Base):
    """点赞表"""
    __tablename__ = 'likearticle'

    user_id = Column(Integer, ForeignKey('user.id'),nullable=False, primary_key=True)
    article_id = Column(Integer, ForeignKey('article.id'),nullable=False, primary_key=True)

class Favorite(Base):
    """收藏表"""
    __tablename__ = 'favorite'

    user_id = Column(Integer, ForeignKey('user.id'),nullable=False, primary_key=True)
    article_id = Column(Integer, ForeignKey('article.id'),nullable=False, primary_key=True)


class Article(Base):
    """文章表"""
    __tablename__ = 'article'

    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    title = Column(String(30), nullable=False)
    abstract = Column(String(100))
    content = Column(Text)
    create_time = Column(DateTime, default=datetime.now)
    read_num = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('user.id'))
    classify_id = Column(Integer, ForeignKey('classify.id'))
    files_uuid = Column(String(50))
    _avatar = Column(String(64))

    user_likes = relationship('User', secondary=LikeArticle.__table__)
    comments = relationship('Comment', backref='articles')

    @property
    def avatar(self):  # 取值
        return self._avatar if self._avatar else "default_pic.jpg"

    @avatar.setter  # 赋值
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
                if self._avatar and os.path.exists("static/avatar_images/article_pic/" + self._avatar):
                    os.unlink("static/avatar_images/article_pic/" + self._avatar)
                file_path = str("static/avatar_images/article_pic/" + self.uuid + '.' + ext)
                with open(file_path, 'wb') as f:
                    f.write(image_data)
                self._avatar = self.uuid + '.' + ext
            else:
                raise ValidationError("not in ['png', 'jpeg', 'gif', 'bmp']")
        else:
            raise ValidationError("64 < len(image_data) < 1024 * 1024 bytes")

    def is_xss_image(self, data):
        return all([char in printable for char in data[:16]])


    @classmethod
    def all(cls):
        return dbSession.query(cls).order_by(cls.id.desc())

    @classmethod
    def hot(cls):
        return dbSession.query(cls).order_by(cls.read_num.desc())

    @classmethod
    def by_id(cls, id):
        return dbSession.query(cls).filter_by(id=id).first()

    @classmethod
    def by_uuid(cls, uuid):
        return dbSession.query(cls).filter_by(uuid=uuid).first()


class Classify(Base):
    """分类表"""
    __tablename__ = 'classify'

    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    name = Column(String(10), unique=True)
    create_time = Column(DateTime, index=True, default=datetime.now)

    articles = relationship('Article', backref='classify')

    @classmethod
    def all(cls):
        return dbSession.query(cls).all()

    @classmethod
    def by_id(cls, id):
        return dbSession.query(cls).filter_by(id=id).first()

    @classmethod
    def by_uuid(cls, uuid):
        return dbSession.query(cls).filter_by(uuid=uuid).first()

    @classmethod
    def by_name(cls, name):
        return dbSession.query(cls).filter_by(name=name).first()


class Comment(Base):
    """评论表"""
    __tablename__ = 'comment'

    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    content = Column(Text)
    create_time = Column(DateTime, index=True, default=datetime.now)
    user_id = Column(Integer, ForeignKey('user.id'))
    article_id = Column(Integer, ForeignKey('article.id'))

    second_comment = relationship('SecondComment', backref='comment')

    @classmethod
    def all(cls):
        return dbSession.query(cls).all()

    @classmethod
    def by_id(cls, id):
        return dbSession.query(cls).filter_by(id=id).first()

    @classmethod
    def by_uuid(cls, uuid):
        return dbSession.query(cls).filter_by(uuid=uuid).first()


class SecondComment(Base):
    """二级评论"""
    __tablename__ = 'secondcomment'

    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    content = Column(Text)
    create_time = Column(DateTime, index=True, default=datetime.now)
    user_id = Column(Integer, ForeignKey('user.id'))
    first_comment_id = Column(Integer, ForeignKey('comment.id'))


