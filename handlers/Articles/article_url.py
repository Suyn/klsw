# -*- coding: utf-8 -*-
from article_handler import (PublishArticlesHandler, ArticleIndexHandler,
                             ArticleDetailsHandler, ClassifyPageHandler,
                             SubmitCommentHandler,ArticleListPageHandler,
                             EditArticleHandler, ClassifyArticle,
                             DeleteArticles, AddClassify
                             )

article_handlers = [
    (r'/my_article/publish_articles', PublishArticlesHandler),
    (r'/my_article/article_index/([1-9]{1}[0-9]{0,2})', ArticleIndexHandler),
    (r'/my_article/article_details', ArticleDetailsHandler),
    (r'/my_article/article_classify/([1-9]{1}[0-9]{0,2})', ClassifyPageHandler),
    (r'/my_article/article_comment', SubmitCommentHandler),

    (r'/my_admin/article_list/([1-9]{1}[0-9]{0,2})', ArticleListPageHandler),
    (r'/my_admin/article_edit', EditArticleHandler),
    (r'/my_admin/classify_article_list/([1-9]{1}[0-9]{0,2})', ClassifyArticle),
    (r'/my_admin/article_delete', DeleteArticles),
    (r'/my_admin/add_classify', AddClassify),
]
