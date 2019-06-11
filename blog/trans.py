# -*- coding: utf-8 -*-

from model_artical import Artical, ArticalLevelTwo, ArticalLevelOne

from model_article import Article, ArticleNodeType, ArticleNo

import model_article_tool

import json

Article.objects.all().update(s_node=None)
Article.objects.all().delete()
ArticleNo.objects.all().delete()
ArticleNo.get_no()
ano = ArticleNo.objects.all().first()
ano.no = 500
ano.save()

for i in range(1, 100):
    a = Article.objects.create()
    a.title = '根节点'
    a.node_type = ArticleNodeType.Root
    a.root_node = True
    a.no = 'root_%d' % i
    a.save()

root = Article.objects.get(no='root_1')

l_one = ArticalLevelOne.objects.all()

saved = []

try:

    for one in l_one:

        new_one = Article()
        new_one.s_node = root
        new_one.node_type = ArticleNodeType.Directory
        new_one.title = one.title
        new_one.no = ArticleNo.get_no()
        new_one.save()
        saved.append(new_one)

        for two in ArticalLevelTwo.objects.filter(level_one=one):

            new_two = Article()
            new_two.node_type = ArticleNodeType.Directory
            new_two.title = two.title
            new_two.s_node = new_one
            new_two.no = ArticleNo.get_no()
            new_two.save()
            saved.append(new_two)

            for atl in Artical.objects.filter(level_two=two):

                new_atl = Article()
                new_atl.title = atl.title
                new_atl.node_type = ArticleNodeType.Article
                new_atl.s_node = new_two
                new_atl.scan = atl.scan
                new_atl.thumbnail_text = atl.thumbnail_text
                new_atl.content_type = atl.content_type
                new_atl.route_path = atl.route_path
                new_atl.html_file = atl.html_file
                new_atl.mark_down_file = atl.mark_down_file
                new_atl.no = '%s' % atl.id
                new_atl.save()
                saved.append(new_atl)


except Exception as e:
    print(e)
    print('开始清理')
    for s in saved:
        s.delete()

# print(json.dumps(model_article_tool.article_list()))



