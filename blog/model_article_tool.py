# -*- coding: utf-8 -*-

from model_article import Article, ArticleNodeType


from common.utils import parse_to_url


def article_list():

    root = Article.objects.get(no='root_1')

    obj = [article_to_simple_obj(article) for article in Article.objects.filter(s_node=root)]

    return obj


def article_to_simple_obj(article):
    """
    转为JSON对象
    """
    nodes = []
    if article.node_type in [ArticleNodeType.Directory.key,
                             ArticleNodeType.DirectoryArticle.key,
                             ArticleNodeType.Root.key]:
        nodes = [article_to_simple_obj(a) for a in Article.objects.filter(s_node=article)]
    return {
        'nodeType': article.node_type,
        'thumbnailText': article_get_thumbnail_text(article),
        'createTime': article_to_time(article.create_time),
        'no': article.no,
        'title': article.title,
        'contentType': article.content_type,
        'routePath': article.route_path,
        'scan': article.scan,
        'nodes': nodes
    }


def article_to_obj(article):
    """
    转为JSON对象
    """
    html_text = None
    if article.html_file:
        with open(article.html_file.path, 'r') as r:
            html_text = r.read().decode()
            r.close()
    md_path = None
    if article.mark_down_file:
        md_path = parse_to_url(article.mark_down_file.url)
    return {
        'nodeType': article.node_type,
        'thumbnailText': article_get_thumbnail_text(article),
        'createTime': article_to_time(article.create_time),
        'title': article.title,
        'htmlText': html_text,
        'markDownFilePath': md_path,
        'contentType': article.content_type,
        'routePath': article.route_path,
        'scan': article.scan,
        'no': article.no
    }


def article_get_thumbnail_text(article):
    """
    获取指定文章的缩略文本
    """
    if article.thumbnail_text:
        return article.thumbnail_text
    else:
        if article.mark_down_file:
            try:
                r = open(article.mark_down_file.path, 'r')
                content = r.read().decode()
                length = len(content)
                if length > 150:
                    valid = content[0:150]
                    article.thumbnail_text = valid.replace('\n', '').replace('#', ' ')
                    article.save()
                    return valid
                elif length == 0:
                    return ''
                else:
                    article.thumbnail_text = content.replace('\n', '').replace('#', ' ')
                    article.save()
                    return content
            except:
                return ''
        else:
            return ''


def article_by_no(no):
    if not no:
        return None
    try:
        return Article.objects.get(no=no)
    except Exception as e:
        return None


def article_scan(article):
    """
    浏览文章
    """
    article.scan += 1
    article.save()
    return article.to_obj()


def article_to_time(t):
    """
    时间格式化
    """
    return t.strftime('%Y-%m-%d %H:%M')
