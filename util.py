import urllib.request
import json


def convertFunction0(tag):
    tag_dict = tag.printable.split(' ')
    date = tag_dict[0].replace(":", "-")
    time = tag_dict[1]
    return date + " " + time


def convertFunction1(tag):
    tag_dict = tag.printable[1:-1].replace(" ", "").replace("/", ",").split(",")
    if len(tag_dict) == 4:
        return float(tag_dict[0]) + float(tag_dict[1]) / 60 + float(tag_dict[2]) / float(tag_dict[3]) / 3600
    else:
        return float(tag_dict[0]) + float(tag_dict[1]) / 60 + float(tag_dict[2]) / 3600


def getLocation(lat, lng):
    url = 'https://api.map.baidu.com/geocoder/v2/?location=' + str(lat) + ',' + str(
        lng) + '&output=json&pois=1&ak=ok5FRlZKYuTOWq3aDzCDgwidTPKwonoG'
    req = urllib.request.urlopen(url)  # json格式的返回数据
    res = req.read().decode("utf-8")  # 将其他编码的字符串解码成unicode
    res_jsn = json.loads(res)

    # get()获取json里面的数据
    jsonResult = res_jsn.get('result')
    address = jsonResult.get('addressComponent')
    # 城市
    city = address.get('city')
    return city
