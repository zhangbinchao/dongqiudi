import json
import requests
import pymongo
import time
import pandas as pd
import random


MONGO_URL = 'localhost'
MONGO_DB = 'dongqiudi'
MONGO_TABLE1 = 'teams'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
header = {'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; STF-AL00 Build/HUAWEISTF-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36 News/198 Android/9 NewsApp/198 SDK/28 VERSION/7.1.8 dongqiudiClientApp'}

def save_to_mongo(result,MONGO_TABLE):
    if not db[MONGO_TABLE].find_one({'team_id': result['team_id']}):
        try:
            if db[MONGO_TABLE].insert(result):
                print('存储到MongoDB成功',result)
        except Exception:
            print('存储到MongoDB失败', result)
    else:
        print('已经爬过了',result)

def spider(url,i,fail):
    News_info = {
        'team_id': None,
        'team_name': None,
        'team_en_name': None,
        'team_logo': None,
        'country': None,
        'city': None,
        'founded': None,
        'venue_name': None,
        'venue_capacity': None,
        'competition_name': None,
        'competition_id': None,
    }
    cookies = 'v=3; iuuid=1A6E888B4A4B29B16FBA1299108DBE9CDCB327A9713C232B36E4DB4FF222CF03; webp=true; ci=1%2C%E5%8C%97%E4%BA%AC; __guid=26581345.3954606544145667000.1530879049181.8303; _lxsdk_cuid=1646f808301c8-0a4e19f5421593-5d4e211f-100200-1646f808302c8; _lxsdk=1A6E888B4A4B29B16FBA1299108DBE9CDCB327A9713C232B36E4DB4FF222CF03; monitor_count=1; _lxsdk_s=16472ee89ec-de2-f91-ed0%7C%7C5; __mta=189118996.1530879050545.1530936763555.1530937843742.18'
    cookie = {}
    for line in cookies.split(';'):
        name, value = cookies.strip().split('=', 1)
        cookie[name] = value
    try:
        html = requests.get(url=url, cookies=cookie, headers=header).content
        news_info = json.loads(html.decode('utf-8'))['base_info']
        try:
            News_info['team_id'] = news_info['team_id']
        except:
            pass
        try:
            News_info['team_name'] = news_info['team_name']
        except:
            pass
        try:
            News_info['team_en_name'] = news_info['team_en_name']
        except:
            pass
        try:
            News_info['team_logo'] = news_info['team_logo']
        except:
            pass
        try:
            News_info['country'] = news_info['country']
        except:
            pass
        try:
            News_info['city'] = news_info['city']
        except:
            pass
        try:
            News_info['founded'] = news_info['founded']
        except:
            pass
        try:
            News_info['venue_capacity'] = news_info['venue_capacity']
        except:
            pass
        try:
            news_info1 = json.loads(html.decode('utf-8'))['trophy_info'][0]
            News_info['competition_name'] = news_info1['competition_name']
            News_info['competition_id'] = news_info1['competition_id']
        except:
            pass
        save_to_mongo(News_info, MONGO_TABLE1)
    except:
        print('请求失败', i)
        fail.append(i)
        print(fail)
        pass
    n = random.uniform(0, 1)
    time.sleep(n)

def Url(i):
    if 0 < i < 10:
        url = 'http://api.dongqiudi.com/data/v1/detail/team/5000000' + str(i) + '?app=dqd&lang=zh-cn'
    elif 10 <= i < 100:
        url = 'http://api.dongqiudi.com/data/v1/detail/team/500000' + str(i) + '?app=dqd&lang=zh-cn'
    elif 100 <= i < 1000:
        url = 'http://api.dongqiudi.com/data/v1/detail/team/50000' + str(i) + '?app=dqd&lang=zh-cn'
    else:
        url = 'http://api.dongqiudi.com/data/v1/detail/team/5000' + str(i) + '?app=dqd&lang=zh-cn'

    return url
def main():
    fail = []
    for i in range(1,10000):
        url = Url(i)
        spider(url,i,fail)

    # fail1 = []
    # try:
    #     for i in range(0,len(fail)):
    #         url = Url(fail[i])
    #         spider(url, i,fail1)
    # except:
    #     pass
    #
    # fail2 = []
    # try:
    #     for i in range(0,len(fail1)):
    #         url = Url(fail1[i])
    #         spider(url, i,fail2)
    # except:
    #     pass
    #
    # fail3 = []
    # try:
    #     for i in range(0,len(fail2)):
    #         url = Url(fail2[i])
    #         spider(url, i,fail3)
    # except:
    #     pass
    #
    # print(fail3)



if __name__ == '__main__':
    main()