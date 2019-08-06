import json
import requests
import time
import pandas as pd


header = {'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; STF-AL00 Build/HUAWEISTF-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36 News/198 Android/9 NewsApp/198 SDK/28 VERSION/7.1.8 dongqiudiClientApp'}

id_list = []
flag = 0
for i in range(1, 91):  # 每一页20篇
    url= 'http://api.dongqiudi.com/search?keywords=%E8%BD%AC%E4%BC%9A&page= ' +str(i ) +'&type=news&'
    html = requests.get(url=url ,headers=header).content
    news = json.loads(html.decode('utf-8'))['news']
    this_id = [k['id'] for k in news]
    id_list = id_list + this_id
    time.sleep(2)
    flag += 1
    print(flag)
pd_data = pd.DataFrame(id_list ,columns=['id_news'])
pd_data.to_excel('id_news.xls', na_rep=False)