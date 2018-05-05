# -*- coding: UTF-8 -*-

import requests, json, time, base64
import urllib, os, sys, random

# 禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_sign(params):
    appSec = 'h5app07a02944776b7638e9b90793363'
    src = appSec + ''.join(["%s%s" % (k, v) for k, v in sorted(params.iteritems(),reverse=True)]) + appSec
    src = src.encode('utf-8')
    src = base64.b64encode(src)
    path = sys.path[0] + "/"
    sign = os.popen('node ' + path + 'didi_sign.js %s' %src).read().replace('\n','')
    return sign

def get_bicycle_list(latitude, longitude):
    headers = {
        'User-Agent': ('Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) '
                       'AppleWebKit/605.1.15 (KHTML, like Gecko) '
                       'Mobile/15E216 MicroMessenger/6.6.6 NetType/WIFI Language/zh_CN'),
        'Content-Type': 'application/json',
        'Referer': 'https://servicewechat.com/wx9e9b87595c41dbb7/25/page-frame.html',
        'Accept-Language': 'zh-cn'
    }
    get_data = {
        'api': 'htw.l.nearbyVehicles',
        'apiVersion': '1.0.0',
        'appKey': 'h5appbcd0af7461691c1e30bcd61098f',
        'appVersion': '1.0.0',
        'hwId': '10000',
        'mobileType': 'iPhone',
        'osType': '1',
        'osVersion': 'iOS 11.3',
        'timestamp': int(round(time.time() * 1000)),
        'ttid': 'h5',
        'userRole': '1'
    }
    post_data = {
        'pinLat': round(latitude, 9),
        'pinLng': round(longitude, 9),
        'cityId': 1,
        'queryRadius': 100,
    }
    sign_data = get_data
    for key, value in post_data.items():
        sign_data[key] = value
    get_data['sign'] = get_sign(sign_data)

    url = 'https://htwkop.xiaojukeji.com/gateway?' + urllib.urlencode(get_data).replace('+', '%20')
    data = urllib.quote(json.dumps(post_data).replace(' ', ''))

    retry_num = 1
    retry_num_max = 3
    bicycle_list = []
    while True:
        try:
            z = requests.post(url, data=data, headers=headers, verify=False)
            z_json = json.loads(z.text)
            for bicycle in z_json.get("data").get("vehiclePosInfoList"):
                bicycle_list.append(bicycle)
            break

        except  TypeError,e:
            if retry_num > retry_num_max:
                break
            print u"请求拒绝，开始第%s次重试" % retry_num, "%s,%s" %(latitude, longitude)
            retry_num += 1
            time.sleep(1)

        except  Exception,e:
            print u"未知错误", e.message
            break
    return bicycle_list

def search_bluegogo(start_latitude, start_longitude, radius, bicycle_number, level):
    xys = []
    # 画出一个正方形的四条边进行搜索
    [xys.append((i, level)) for i in range(-level,level)]
    [xys.append((i, -level)) for i in range(-level+1,level+1)]
    [xys.append((level,i)) for i in range(-level+1,level+1)]
    [xys.append((-level,i)) for i in range(-level,level)]
    if level == 0:
        xys.append((0,0))

    for xy in xys :
        num_lat = xy[0]
        num_lon = xy[1]
        offset_lat = num_lat * radius + float(random.randint(100000,300000))/1000000000
        offset_lon = num_lon * radius + float(random.randint(100000,300000))/1000000000
        bicycle_list =  get_bicycle_list(start_latitude + offset_lat, start_longitude + offset_lon)
        for bicycle in bicycle_list:
            if bicycle["vehicleId"] == bicycle_number :
                print u'找到了',bicycle["vehicleId"],bicycle
                quit()
        print num_lat, num_lon, "%s,%s"%(str(start_latitude + offset_lat), str(start_longitude + offset_lon)), "有%s辆车" % (str(len(bicycle_list)))

    return None

def test_length(latitude=None, longitude=None):
    if latitude == None or longitude == None:
        latitude, longitude = 39.9088600000,116.3973900000

    bicycle_list = get_bicycle_list(latitude, longitude)
    print u"结果数据："
    print bicycle_list
    print ""
    if len(bicycle_list) == 0 :
        quit()
    lat = []
    lon = []
    [lat.append(float(i['lat'])) for i in bicycle_list ]
    [lon.append(float(i['lng'])) for i in bicycle_list ]
    print u"最大距离经纬度:"
    print  "%s,%s" %(max(lat) , max(lon))
    print  "%s,%s" %(min(lat) , min(lon))
    print ""
    print  u"区域最大边长"
    print  "%s,%s" % ( max(lat)- min(lat), (max(lon)-min(lon)))
    print ""
    print u"原点位置 和 单车位置 , 一共%s辆车" %len(bicycle_list)
    print "%s,%s" %(latitude,longitude)
    for bicycle in bicycle_list:
        print "%s,%s" % (bicycle.get("lat"), bicycle.get("lng")), bicycle.get("vehicleId")
    quit()

# test_length(39.9769880000,116.4377940000)

# 地毯式搜索某一辆车的位置
# 设置原点
start_latitude, start_longitude = 39.9759270000,116.4382450000

# 扫描半径(经纬度)  每次最多返回20辆车，设置不合理的话拿不到全部的车
# radius = 0.0022 # 0.187公里
radius = 0.0003  # 0.033公里

# 要查找的自行车ID
bicycle_ID = 10727844

for round_num in range(0, 60):
    search_bluegogo(start_latitude, start_longitude, radius, bicycle_ID, round_num)





