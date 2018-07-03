# -*- coding: utf-8 -*-
from handlers.Mainhandler.main_handler import authpermission
from handlers.BaseHandler.base import BaseHandler
from libs.articles.articles_lib import (publish_article_lib, article_index_lib,
                                        article_classify_lib, article_comment_lib,
                                        article_list_lib, edit_article_lib,
                                        classify_list_lib, delete_article_lib,
                                        like_article_lib, add_classify_name_lib
                                        )
from module.article.article_module import Classify, Article, SecondComment
from module.files.files_module import Files


class ArticleIndexHandler(BaseHandler):
    """文章首页"""
    def get(self, page):
        hot_articles, classify, pagination = article_index_lib(self, page)
        kwargs = {
            'hot_articles': hot_articles,
            'classifies': classify,
            'pagination': pagination,
            'current_user': self.current_user
        }
        return self.render('article/article_index.html', **kwargs)


class PublishArticlesHandler(BaseHandler):
    """添加文章"""
    @authpermission
    def get(self):
        classify = Classify.all()
        return self.render('back_end/admin-form.html', classify=classify)

    @authpermission
    def post(self):
        title = self.get_argument('title', None)
        abstract = self.get_argument('abstract', None)
        article_pic = self.request.files.get('article_pic', None)
        classify = self.get_argument('classify', None)
        content = self.get_argument('article', None)
        article_file = self.request.files.get('article_file', None)
        print '????',article_file
        result = publish_article_lib(self, title, abstract, article_pic, classify, content, article_file)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})

class ArticleDetailsHandler(BaseHandler):
    """文章详情"""
    def get(self):
        uuid = self.get_argument('unique_id', None)

        # 文章阅览数+1
        article = Article.by_uuid(uuid)
        if article is None:
            return self.render('back_end/admin-404.html')
        article.read_num += 1
        self.db.commit()
        #---------------------------------------------

        # 获取该文章的点赞数目
        likes = article.user_likes
        #---------------------------------------------

        # 获取文章对应的附属文件
        file_uuid = article.files_uuid
        file_name = None
        if file_uuid is not None:
            file_uuid = Files.by_uuid(file_uuid)

            # file_name
            file_name = file_uuid.filename
        #---------------------------------------------

        # 详细页的下一篇文章
        next_article_id = article.id + 1
        while Article.by_id(next_article_id) is None:
            if next_article_id > Article.all()[0].id:
                break
            next_article_id += 1
        next_article = Article.by_id(next_article_id)
        #---------------------------------------------
        comments = article.comments
        kwargs = {
            'current_user': self.current_user,
            'likes': likes,
            'article': article,
            'next_article': next_article,
            'comments': comments,
            'file_uuid': file_uuid,
            'filename': file_name,
        }
        return self.render('article/article_detail.html', **kwargs)

    def post(self):
        """提交点赞"""
        uuid = self.get_argument('article_id', None)
        result = like_article_lib(self, uuid)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})

class ClassifyPageHandler(BaseHandler):
    """文章首页 ------> 文章分类"""
    def get(self, page):
        uuid = self.get_argument('classify_unique_id', None)
        hot_articles, classify, pagination = article_classify_lib(self, page, uuid)
        if hot_articles is None or classify is None or pagination is None:
            return self.render('back_end/admin-404.html')
        kwargs = {
            'uuid': uuid,
            'hot_articles': hot_articles,
            'classifies': classify,
            'pagination': pagination
        }
        return self.render('article/article_classify.html', **kwargs)

class SubmitCommentHandler(BaseHandler):
    """添加文章评论"""
    def post(self):
        comment = self.get_argument('comment', None)
        article_uuid = self.get_argument('article_id', None)
        result = article_comment_lib(self, comment, article_uuid)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})


class ArticleListPageHandler(BaseHandler):
    """后台文章列表---->>>-----分页"""

    @authpermission
    def get(self, page):
        number = self.db.query(Article).order_by(None).count()
        classifies, pagination = article_list_lib(self, page)
        kwargs = {
            'number': number,
            'classifies': classifies,
            'current_classify': None,
            'pagination': pagination,
        }
        return self.render('back_end/admin-table.html', **kwargs)


class ClassifyArticle(BaseHandler):
    """分类文章列表"""
    def get(self, page):
        classify_uuid = self.get_argument('classify', None)
        #获取分类的uuid以及是否存在----------------------------------------
        if classify_uuid == '' or classify_uuid is None:
            return self.redirect('/my_admin/article_list/1')
        classify = Classify.by_uuid(classify_uuid)
        if classify is None:
            return self.redirect('/my_admin/article_list/1')
        #----------------------------------------
        articles = classify.articles

        #共有记录的条数--------
        number = len(articles)
        #---------------------

        classifies, pagination = classify_list_lib(self, page, articles)
        kwargs = {
            'number': number,
            'current_classify': classify,
            'classifies': classifies,
            'pagination': pagination,
        }
        return self.render('back_end/admin-classify-table.html', **kwargs)


class EditArticleHandler(BaseHandler):
    """编辑文章"""

    @authpermission
    def get(self):
        uuid = self.get_argument('unique_id', None)
        print uuid
        article = Article.by_uuid(uuid)
        if article.user.id != self.current_user.id:
            return self.write('您无此权限')
        classify = Classify.all()
        kwargs = {
            'classify': classify,
            'article': article,
        }
        return self.render('back_end/admin-edit-article.html', **kwargs)

    @authpermission
    def post(self):
        title = self.get_argument('title', None)
        abstract = self.get_argument('abstract', None)
        article_pic = self.request.files.get('article_pic', None)
        classify = self.get_argument('classify', None)
        content = self.get_argument('article', None)
        uuid = self.get_argument('article_unique_id', None)
        print title,abstract,article_pic,classify,content,uuid
        result = edit_article_lib(self, title, abstract, article_pic, classify, content, uuid)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})

class DeleteArticles(BaseHandler):
    """删除文章"""

    @authpermission
    def post(self):
        uuid = self.get_argument('delete_unique_id', None)
        result = delete_article_lib(self, uuid)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})


class AddClassify(BaseHandler):
    """添加分类"""
    @authpermission
    def get(self):
        return self.render('back_end/admin-add-classify.html')

    @authpermission
    def post(self):
        classify_name = self.get_argument('classify_name', None)
        result = add_classify_name_lib(self,classify_name)
        if result['status'] is True:
            return self.write(result['msg'])
        return self.write(result['msg'])