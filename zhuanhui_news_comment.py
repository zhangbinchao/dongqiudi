import json
import requests
import pymongo
import time
import pandas as pd
import random


MONGO_URL = 'localhost'
MONGO_DB = 'dongqiudi'
MONGO_TABLE1 = 'zhuanhui_news_comments'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
header = {'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; STF-AL00 Build/HUAWEISTF-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36 News/198 Android/9 NewsApp/198 SDK/28 VERSION/7.1.8 dongqiudiClientApp'}


def save_to_mongo(result,MONGO_TABLE):
    if not db[MONGO_TABLE].find_one({'article_id': result['article_id']}):
        try:
            if db[MONGO_TABLE].insert(result):
                print('存储到MongoDB成功',result)
        except Exception:
            print('存储到MongoDB失败', result)
    else:
        print('已经爬过了',result)


def main():
    id_list = pd.read_excel('id_news.xls', usecols=['id_news'])
    for i in range(208, len(id_list)):
        url = 'http://api.dongqiudi.com/v2/article/'+str(id_list.iloc[i, 0])+'/comment?size=20&version=198&platform=h5 '
        tags = []
        ups = []
        Comments_info = {
            'article_id': None,
            'title': None,
            'comment_total': None,
            'recommend_list': None,
            'up': None,
        }
        cookies = 'v=3; iuuid=1A6E888B4A4B29B16FBA1299108DBE9CDCB327A9713C232B36E4DB4FF222CF03; webp=true; ci=1%2C%E5%8C%97%E4%BA%AC; __guid=26581345.3954606544145667000.1530879049181.8303; _lxsdk_cuid=1646f808301c8-0a4e19f5421593-5d4e211f-100200-1646f808302c8; _lxsdk=1A6E888B4A4B29B16FBA1299108DBE9CDCB327A9713C232B36E4DB4FF222CF03; monitor_count=1; _lxsdk_s=16472ee89ec-de2-f91-ed0%7C%7C5; __mta=189118996.1530879050545.1530936763555.1530937843742.18'
        cookie = {}
        for line in cookies.split(';'):
            name, value = cookies.strip().split('=', 1)
            cookie[name] = value
        try:
            html = requests.get(url=url,cookies=cookie, headers=header).content
        except:
            print('请求失败', id_list.iloc[i,0])
            continue
        n = 1 + random.uniform(0, 1)
        time.sleep(n)

        try:
            comment_info = json.loads(html.decode('utf-8'))['data']
            Comments_info['article_id'] = comment_info['article']['id']
            Comments_info['title'] = comment_info['article']['title']
            Comments_info['comment_total'] = comment_info['comment_total']
            comments = comment_info['recommend_list'][:]
            for comment in comments:
                infos_tag = comment['content']
                infos_up = comment['up']
                tags.append(infos_tag)
                ups.append(infos_up)
            Comments_info['recommend_list']=tags
            Comments_info['up']=ups

            save_to_mongo(Comments_info, MONGO_TABLE1)
        except:
            print('爬取出错',Comments_info['title'])
            continue



if __name__ == '__main__':
    main()