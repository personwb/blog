
from django.conf.urls import url

import view_artical

urlpatterns = [

    # url(r'^upload', views.upload, name='upload'),

    url(r'^levelone/add', view_artical.add_level_one, name='add_level_one'),
    url(r'^levelone/detail', view_artical.level_one_detail, name='level_one_detail'),
    url(r'^levelone/list', view_artical.level_one_list, name='level_one_list'),

    url(r'^leveltwo/add', view_artical.add_level_two, name='add_level_two'),
    url(r'^leveltwo/detail', view_artical.level_two_detail, name='level_two_detail'),
    url(r'^leveltwo/list', view_artical.level_two_list, name='level_two_list'),
    url(r'^leveltwo/delete', view_artical.remove_level_two, name='remove_level_two'),

    url(r'^artical/detail', view_artical.artical_detail_show, name='artical_detail_show'),
    url(r'^artical/manager/detail', view_artical.artical_detail, name='artical_detail'),
    url(r'^artical/add', view_artical.artical_add, name='artical_add'),
    url(r'^artical/manager/list', view_artical.artical_manager_list, name='artical_manager_list'),

    url(r'^artical/list', view_artical.artical_list, name='artical_list_by_level_one'),



    url(r'^levelonetwolist', view_artical.level_one_two_list, name='level_one_two_list'),


]