# -*- coding: utf-8 -*-
import json
from libs.files.files_lib import save_file
from module.article.article_module import Classify, Article, Comment
from libs.pagination.pagination_lib import Pagination

MAX_PAGE = 8
list_page = 5

def article_index_lib(self, page):
    """文章首页及分页"""
    hot_articles = Article.hot()[:6]
    classify = Classify.all()
    page = int(page)
    items = self.db.query(Article).order_by(Article.id.desc()).limit(MAX_PAGE).offset((page - 1) * MAX_PAGE).all()
    if page == 1 and len(items) < MAX_PAGE:
        total = len(items)
    else:
        total = self.db.query(Article).order_by(None).count()
    return hot_articles, classify, Pagination(page, MAX_PAGE, total, items)

def article_list_lib(self, page):
    """后台文章---->>>>---分页"""
    classify = Classify.all()
    page = int(page)
    items = self.db.query(Article).order_by(Article.id.desc()).limit(list_page).offset((page - 1) * list_page).all()
    if page == 1 and len(items) < list_page:
        total = len(items)
    else:
        total = self.db.query(Article).order_by(None).count()
    return classify, Pagination(page, list_page, total, items)

def classify_list_lib(self, page, articles):
    """分类文章列表"""
    classify = Classify.all()
    page = int(page)
    items = articles[::-1][(page - 1) * list_page:page * list_page]
    if page == 1 and len(items) < list_page:
        total = len(items)
    else:
        total = len(articles)
    return classify, Pagination(page, list_page, total, items)


def article_classify_lib(self, page, uuid):
    """文章分类页"""
    classify_uuid = Classify.by_uuid(uuid)
    if classify_uuid is None:
        return None,None,None
    classify_articles = classify_uuid.articles
    hot_articles = Article.hot()[:6]
    classify = Classify.all()
    page = int(page)
    items = classify_articles[::-1][(page - 1) * MAX_PAGE:page * MAX_PAGE]
    if page == 1 and len(items) < MAX_PAGE:
        total = len(items)
    else:
        total = len(classify_articles)
    return hot_articles, classify, Pagination(page, MAX_PAGE, total, items)

def publish_article_lib(self, title, abstract, article_pic, classify, content, article_file):
    """添加文章"""
    if title == '' or title is None:
        return {'status': False, 'msg': '标题为空'}
    if len(title) > 30:
        return {'status': False, 'msg': '标题超出30个字符'}
    if abstract == '' or abstract is None:
        return {'status': False, 'msg': '摘要为空'}
    if len(abstract) > 100:
        return {'status': False, 'msg': '摘要超出100个字符'}
    if article_pic == '' or article_pic is None:
        return {'status': False, 'msg': '未选择图片'}
    if classify == '' or classify is None:
        return {'status': False, 'msg': '未选择分类'}
    if content == '' or content is None:
        return {'status': False, 'msg': '内容为空'}
    classify = Classify.by_uuid(classify)
    if classify is None:
        return {'status': False, 'msg': '无此分类'}
    article_pic = article_pic[0]['body']

    try:
        article = Article()
        article.title = title
        article.abstract = abstract
        article.content = content
        article.classify_id = classify.id
        article.user_id = self.current_user.id
        self.db.add(article)
        self.db.commit()
        article.avatar = article_pic
        if article_file is not None:
            file_uuid = save_file(self, article_file[0])
            print '--------------', file_uuid
            if isinstance(file_uuid, dict) is True:
                return {'status': True, 'msg': file_uuid['msg']}
            article.files_uuid = file_uuid
        self.db.commit()
        return {'status': True, 'msg': '新文章上传成功'}
    except Exception as e:
        return {'status': False, 'msg': e}

def article_comment_lib(self, comment, article_uuid):
    """文章评论"""
    if not self.current_user:
        return {'status': False, 'msg': '您还未登录'}
    if article_uuid=='' or article_uuid is None:
        return {'status': False, 'msg': '请刷新页面重试'}
    if comment == '' or comment is None:
        return {'status': False, 'msg': '评论输入为空'}
    article_id = Article.by_uuid(article_uuid)
    if article_id is None:
        return {'status': False, 'msg': '您要评论的文章不存在'}
    cmts = Comment()
    cmts.content = comment
    cmts.article_id = article_id.id
    cmts.user_id = self.current_user.id
    self.db.add(cmts)
    self.db.commit()
    return {'status': True, 'msg': '评论成功'}

def edit_article_lib(self, title, abstract, article_pic, classify, content, uuid):
    """编辑文章"""
    if uuid == '' or uuid is None:
        return {'status': False, 'msg': '请刷新页面重试'}
    article = Article.by_uuid(uuid)
    if article is None:
        return {'status': False, 'msg': '文章不存在'}
    if self.current_user.name != article.user.name:
        return {'status': False, 'msg': '您没有权限修改该文章'}
    if title == '' or title is None:
        return {'status': False, 'msg': '标题为空'}
    if len(title) > 30:
        return {'status': False, 'msg': '标题超出30个字符'}
    if abstract == '' or abstract is None:
        return {'status': False, 'msg': '摘要为空'}
    if len(abstract) > 100:
        return {'status': False, 'msg': '摘要超出100个字符'}
    if classify == '' or classify is None:
        return {'status': False, 'msg': '未选择分类'}
    if content == '' or content is None:
        return {'status': False, 'msg': '内容为空'}
    classify = Classify.by_uuid(classify)
    if classify is None:
        return {'status': False, 'msg': '无此分类'}
    if article_pic == '' or article_pic is None:
        try:
            article.title = title
            article.abstract = abstract
            article.content = content
            article.classify_id = classify.id
            article.user_id = self.current_user.id
            # self.db.add(article)
            self.db.commit()
            return {'status': True, 'msg': '文章修改成功'}
        except Exception as e:
            return {'status': 400, 'msg': e}
    article_pic = article_pic[0]['body']
    try:
        article.avatar = article_pic
        article.title = title
        article.abstract = abstract
        article.content = content
        article.classify_id = classify.id
        article.user_id = self.current_user.id
        # self.db.add(article)
        self.db.commit()
        return {'status': True, 'msg': '文章修改成功'}
    except Exception as e:
        return {'status': 400, 'msg': e}


def delete_article_lib(self, uuid):
    """删除文章"""
    if uuid == '' or uuid is None:
        return {'status': False, 'msg': '请刷新页面重试'}
    article = Article.by_uuid(uuid)
    if article is None:
        return {'status': False, 'msg': '该文章不存在'}
    if article.user.id != self.current_user.id:
        return {'status': False, 'msg': '您无此权限'}
    self.db.delete(article)
    self.db.commit()
    return {'status': True, 'msg': '删除成功'}


def like_article_lib(self, uuid):
    """点赞"""
    if uuid == '' or uuid is None:
        return {'status': False, 'msg': '请刷新页面重试'}
    if self.current_user is None:
        return {'status': False, 'msg': '您还未登录账号'}
    article = Article.by_uuid(uuid)
    if article is None:
        return {'status': False, 'msg': '您要点赞的文章不存在，请刷新页面重试'}
    article.user_likes.append(self.current_user)
    self.db.commit()
    return {'status': True, 'msg': len(article.user_likes)}


def add_classify_name_lib(self, classify_name):
    """添加分类"""
    if classify_name is None or classify_name == '':
        return {'status': False, 'msg': '输入为空'}
    if len(classify_name) > 15:
        return {'status': False, 'msg': '输入的分类名过长，超过15个字符了'}
    if Classify.by_name(classify_name) is not None:
        return {'status': False, 'msg': '该名字已存在'}
    classify = Classify()
    classify.name = classify_name
    self.db.add(classify)
    self.db.commit()
    return {'status': True, 'msg': '添加成功'}