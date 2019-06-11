
from django.conf.urls import url

#import trans

import view_article

urlpatterns = [

    # url(r'^upload', views.upload, name='upload'),

    url(r'^article/list', view_article.article_list, name='article_list'),
    url(r'^article/detail/(\d+)', view_article.article_detail, name='article_detail'),
    url(r'^article/create', view_article.article_create, name='article_create'),
    url(r'^article/update', view_article.article_update, name='article_update'),
    url(r'^article/delete', view_article.article_delete, name='article_delete'),

    url(r'^article/directory/create', view_article.article_directory_create, name='article_directory_create'),
    url(r'^article/directory/update', view_article.article_directory_update, name='article_directory_update'),

    # url(r'^levelone/add', view_artical.add_level_one, name='add_level_one'),
    # url(r'^levelone/detail', view_artical.level_one_detail, name='level_one_detail'),
    # url(r'^levelone/list', view_artical.level_one_list, name='level_one_list'),
    #
    # url(r'^leveltwo/add$', view_artical.add_level_two, name='add_level_two'),
    # url(r'^leveltwo/detail', view_artical.level_two_detail, name='level_two_detail'),
    # url(r'^leveltwo/list', view_artical.level_two_list, name='level_two_list'),
    # url(r'^leveltwo/delete', view_artical.remove_level_two, name='remove_level_two'),
    #
    # url(r'^artical/detail', view_artical.artical_detail_show, name='artical_detail_show'),
    # url(r'^artical/manager/detail', view_artical.artical_detail, name='artical_detail'),
    # url(r'^artical/add$', view_artical.artical_add, name='artical_add'),
    # url(r'^artical/manager/list', view_artical.artical_manager_list, name='artical_manager_list'),
    #
    # url(r'^artical/list', view_artical.artical_list, name='artical_list_by_level_one'),
    #
    # url(r'^artical/addbyuuid$', view_artical.safe_create_artical_with_uuid, name='safe_create_artical_with_uuid'),
    #
    #
    # url(r'^levelonetwolist', view_artical.level_one_two_list, name='level_one_two_list'),


]