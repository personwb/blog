# -*- coding: utf-8 -*-

import threading

import time

import urllib2

import json

import logging

logger = logging.getLogger('default')

last_time = time.time()

key_tencent_map = 'QJYBZ-TCCRF-KF3JN-NVYBM-UUXSF-DVFWJ'


# safe request tencent
def safe_request(fn):

    def p_safe(*args):

        global last_time

        now = time.time()

        if now - last_time < 0.2:
            time.sleep(now - last_time)
            logger.info('tencent request to many, auto just %f' % (now - last_time))

        last_time = now

        return fn(*args)

    return p_safe


@safe_request
def get_distance(f, t):

    path = 'https://apis.map.qq.com/ws/distance/v1/?mode=walking&from=%s&to=%s&key=%s' % (f, t, key_tencent_map)

    logger.info('距离计算：from: %s to: %s' % (f, t))
    try:
        res = urllib2.urlopen(path)
        cont = res.read()
        obj = json.loads(cont)
        logger.info('距离计算：%s' % (cont))
        if 'result' in obj and 'elements'in obj['result'] and len(obj['result']['elements']):
            info = obj['result']['elements'][0]
            return {
                'distance': info['distance'],
                'duration': info['duration']
            }
        return None
    except Exception:
        return None


@safe_request
def trans_location(lat, lng):
    path = 'https://apis.map.qq.com/ws/coord/v1/translate?type=5&key=%s&locations=%s,%s' % (key_tencent_map, lat, lng)
    logger.info('定位转换：%f  %f %s' % (lat, lng, path))
    try:
        res = urllib2.urlopen(path)
        cont = res.read()
        obj = json.loads(cont)
        logger.info('定位转换：%s' % (cont))
        if 'locations' in obj and len(obj['locations']):
            location = obj['locations'][0]
            return {
                'latitude': location['lat'],
                'longitude': location['lng'],
            }
        return None
    except Exception:
        return None
# 同步腾讯地址
# def syn_address():
#     def get_all_province():
#         path = 'https://apis.map.qq.com/ws/district/v1/getchildren?key=%s' % (key_tencent_map,)



# 根据定位获取周边信息
@safe_request
def get_poi_by_location(lat, lng):

    path = 'https://apis.map.qq.com/ws/geocoder/v1/?location=%f,%f&key=%s&get_poi=1&poi_options=policy=2;radius=200' % (lat, lng, key_tencent_map)

    try:
        logger.info('获取坐标周边信息：%s' % path)
        res = urllib2.urlopen(path)
        cont = res.read()
        obj = json.loads(cont)
        logger.info('获取坐标周边信息：%s' % cont)
        if 'result' in obj and 'pois' in obj['result']:

            pois = obj['result']['pois']

            if not len(pois):
                return None

            poi = pois[0]
            poi['province'] = poi['ad_info']['province']
            poi['city'] = poi['ad_info']['city']
            poi['district'] = poi['ad_info']['district']
            return poi
        return None
    except Exception:
        return None


# 根据定位获取省市
@safe_request
def get_province_city_by_location(lat, lng):

    path = 'https://apis.map.qq.com/ws/geocoder/v1/?location=%f,%f&key=%s&get_poi=0' % (lat, lng, key_tencent_map)

    try:
        res = urllib2.urlopen(path)
        cont = res.read()
        obj = json.loads(cont)
        if 'result' in obj and 'address_component' in obj['result']:

            address_component = obj['result']['address_component']

            return {
                'province': address_component.get('province'),
                'city': address_component.get('city'),
            }
        return None
    except Exception:
        return None


# 根据关键字获取周边信息
@safe_request
def get_location_by_key_word(body):

    key_word = body['keyWord']

    # city = body['city']

    # latitude = body['latitude']
    #
    # longitude = body['longitude']

    page = body['page']

    pageSize = body['pageSize']

    # parse_location = get_province_city_by_location(latitude, longitude)

    path = "https://apis.map.qq.com/ws/place/v1/suggestion/?"

    params = {
        'keyword': key_word,
        'region': '郑州',
        'region_fix': 1,
        # 'location': latitude + longitude,
        'policy': 1,
        'page_index': page,
        'page_size': pageSize,
        'key': key_tencent_map,
        'output': 'json',
    }

    for key in params:
        path += ('%s=%s&' % (key, params[key]))

    try:
        res = urllib2.urlopen(path)
        cont = res.read()
        obj = json.loads(cont)

        if 'status' in obj and obj['status'] == 0 and 'data' in obj:

            count = obj['count']
            data = obj['data']

            return {
                'count': count,
                'data': data,
            }

        return None
    except Exception:
        return None
