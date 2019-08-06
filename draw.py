import pymongo
import numpy as np
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Calendar
import datetime
import wordcloud
import collections
from PIL import Image
import matplotlib.pyplot as plt


MONGO_DB = 'dongqiudi'
MONGO_TABLE = 'zhuanhuinews'
client = pymongo.MongoClient(host='localhost', port=27017)
db = client['dongqiudi']
collection1 = db['zhuanhuinews']
collection2 = db['teams']
collection3 = db['zhuanhui_news_comments']
date_final = [0]*31


visit_total_pack=[]
def visit_total():
    #1.新闻关注总量
    records = collection1.find({}).sort([("visit_total", pymongo.ASCENDING)])
    for record in records:
        visit_total_temp = []
        id = record['article_id']
        title = record['title']
        visit_total = str(record['visit_total']).replace('+','')
        visit_total_temp.append(id)
        visit_total_temp.append(title)
        visit_total_temp.append(visit_total)
        print(visit_total_temp)
        visit_total_pack.append(visit_total_temp)
    np_data = np.array(visit_total_pack)
    pd_data = pd.DataFrame(np_data, columns=['article_id', 'title', 'visit_total'])
    pd_data.to_excel('visit_total.xls', na_rep=True)

def tag():
    #2.球队、球员出现次数
    records2 = collection1.find({})

    team_tag = []
    player_tag = []

    #球队的标签 要有一个球队名称的对应表
    for record2 in records2:
        tag = record2['tag']
        for i2 in range(0, len(tag)):
            counts = collection2.find({})
            for count in counts:
                if count['team_name'] == tag[i2]:
                    team_tag.append(tag[i2])
                    print(len(team_tag))
                    break
    #球员的标签
    records2 = collection1.find({})
    for record2 in records2:
        tag = record2['tag']
        for i2 in range(0, len(tag)):
            if tag[i2] in team_tag:
                pass
            else:
                player_tag.append(tag[i2])
     #统计词频
    word_counts1 = collections.Counter(team_tag)
    word_counts2 = collections.Counter(player_tag)

    data_pack = []
    for key in word_counts1:
        data_temp = []
        data_temp.append(key)
        data_temp.append(word_counts1[key])
        data_pack.append(data_temp)
    np_data = np.array(data_pack)

    pd_data = pd.DataFrame(np_data, columns=['name','frequency'])
    pd_data.to_excel('word_counts1.xls', na_rep=False)

    data_pack = []
    for key in word_counts2:
        data_temp = []
        data_temp.append(key)
        data_temp.append(word_counts2[key])
        data_pack.append(data_temp)
    np_data1 = np.array(data_pack)

    pd_data1 = pd.DataFrame(np_data1, columns=['name','frequency'])
    pd_data1.to_excel('word_counts2.xls', na_rep=False)
    # word_counts_top10_teams = word_counts1.most_common(10)
    # word_counts_top10_players = word_counts2.most_common(10)


    #做球队云图
    word_counts1 = pd.read_excel('word_counts1.xls', usecols=['name','frequency'])
    name = list(word_counts1.name)
    value = word_counts1.frequency
    #dataframe转成dic
    for m in range(len(name)):
        name[m] = str(name[m])
    dic = dict(zip(name, value))

    mask1 = np.array(Image.open('C.png'))  # 定义词频背景
    wc1 = wordcloud.WordCloud(
        background_color="white",
        font_path="fonts/simkai.ttf",
        mask=mask1,  # 设置背景图
        max_words=200,  # 最多显示词数
        max_font_size=100,  # 字体最大值
        width=300,
        height = 500,
    )
    wc1.generate_from_frequencies(dic)  # 从字典生成词云
    image_colors = wordcloud.ImageColorGenerator(mask1)  # 从背景图建立颜色方案
    wc1.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案
    plt.imshow(wc1)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    plt.show()  # 显示图像

    #做球队云图
    word_counts2 = pd.read_excel('word_counts2.xls', usecols=['name','frequency'])
    name = list(word_counts2.name)
    value = word_counts2.frequency

    for m in range(len(name)):
        name[m] = str(name[m])
    dic = dict(zip(name, value))
    mask2 = np.array(Image.open('C.png'))  # 定义词频背景
    wc2 = wordcloud.WordCloud(
        background_color="white",
        font_path="fonts/simkai.ttf",
        mask=mask2,  # 设置背景图
        max_words=200,  # 最多显示词数
        max_font_size=100  # 字体最大值
    )
    wc2.generate_from_frequencies(dic)  # 从字典生成词云
    image_colors = wordcloud.ImageColorGenerator(mask2)  # 从背景图建立颜色方案
    wc2.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案
    plt.imshow(wc2)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    plt.show()  # 显示图像

    ##3.每天新闻量的变化

def News_num_per_day():
    records3 = collection1.find({})
    for record3 in records3:
        time = record3['time'].split(' ')
        for day in range(1, 32):
            if day < 10:
                date = '07-0%d' % day
            else:
                date = '07-%d' % day
            if date == time[0]:
                date_final[day - 1] += 1
    print(date_final)

    begin = datetime.date(2019, 7, 1)
    end = datetime.date(2019, 7, 31)
    data3 = [
        [str(begin + datetime.timedelta(days=i)), date_final[i]]
        for i in range((end - begin).days + 1)
    ]

    calendar = (
            Calendar(init_opts=opts.InitOpts(width='600px',height='800px'))
            .add("", data3,calendar_opts=opts.CalendarOpts(range_=['2019-06-01', '2019-08-31']))
            .set_global_opts(
                title_opts=opts.TitleOpts(title="2019年7月每日发布转会新闻数量",pos_left='15%'),
                visualmap_opts=opts.VisualMapOpts(
                    max_=120,
                    min_=0,
                    orient="horizontal",
                    is_piecewise=False,
                    pos_top="230px",
                    pos_left="100px",
                    pos_right="10px"
                )
                )
            .render('日期热力图.html')
         )

    ##4.新闻来源top10

def source():
    source = []
    records4 = collection1.find({})
    for record4 in records4:
        source.append(record4['source'])
    word_counts4 = collections.Counter(source)

    data_pack = []
    for key in word_counts4:
        data_temp = []
        data_temp.append(key)
        data_temp.append(word_counts4[key])
        data_pack.append(data_temp)
    np_data4 = np.array(data_pack)

    pd_data4 = pd.DataFrame(np_data4, columns=['name','frequency'])
    pd_data4.to_excel('word_counts4.xls', na_rep=False)

    from pyecharts.globals import ThemeType
    from pyecharts.charts import  Pie
    source_top10 = pd.read_excel('word_counts4.1.xls', usecols=['name', 'frequency'])
    name = list(source_top10.name)
    value = source_top10.frequency

    data_pack = []
    for m in range(len(name)):
        data_temp = []
        data_temp.append(name[m])
        data_temp.append(value[m])
        data_pack.append(data_temp)
    np_data5 = np.array(data_pack)
    pie = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.CHALK))
            .add("", np_data5)
            .set_global_opts(title_opts=opts.TitleOpts(title="转会新闻来源图", pos_left='center'),
                             legend_opts=opts.LegendOpts(is_show=False))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}", font_size=16), )
            .render('转会新闻来源图饼图.html')
    )

    # ##5.标题词云

def title():
    import jieba
    import jieba.analyse

    title = []
    jieba.load_userdict('dict.txt')
    jieba.analyse.set_stop_words('stop_words.txt')
    records5 = collection1.find({})
    for record5 in records5:
        title.append(record5['title'])
    words = "".join(title)
    wordlist = jieba.cut(words, cut_all=True)
    word_space_split = " ".join(wordlist)
    stopwords = set()
    mask2 = np.array(Image.open('CR.jpg'))  # 定义词频背景
    wc2 = wordcloud.WordCloud(
        background_color="white",
        font_path="fonts/simkai.ttf",
        stopwords=stopwords,
        mask=mask2,  # 设置背景图
        max_words=200,  # 最多显示词数
        max_font_size=100  # 字体最大值
    )
    wc2.generate(word_space_split)  # 从字典生成词云
    image_colors = wordcloud.ImageColorGenerator(mask2)  # 从背景图建立颜色方案
    wc2.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案
    plt.imshow(wc2)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    plt.show()  # 显示图像

    ##5.评论词云

def comment():
    import jieba
    import jieba.analyse
    comment = []
    records6 = collection3.find({})
    for record6 in records6:
        for n in range(0,len(record6['up'])):
            comment_temp = []
            comment_temp.append(record6['up'][n])
            comment_temp.append(record6['title'])
            comment_temp.append(record6['recommend_list'][n])
            comment.append(comment_temp)
    np_data6 = np.array(comment)
    np_data6 = pd.DataFrame(np_data6, columns=['up','title','recommend_list'])
    np_data6.to_excel('word_counts6.xls', na_rep=False)

    comment = []
    jieba.load_userdict('dict.txt')
    jieba.analyse.set_stop_words('stop_words.txt')
    records6 = collection3.find({})
    for record6 in records6:
        for n in range(0,len(record6['recommend_list'])):
            comment.append(record6['recommend_list'][n])
    words = "".join(comment)
    wordlist = jieba.cut(words, cut_all=True)
    word_space_split = " ".join(wordlist)
    stopwords = set()
    mask2 = np.array(Image.open('ca.jpg'))  # 定义词频背景
    wc2 = wordcloud.WordCloud(
        background_color="white",
        font_path="fonts/simkai.ttf",
        stopwords=stopwords,
        mask=mask2,  # 设置背景图
        max_words=200,  # 最多显示词数
        max_font_size=100  # 字体最大值
    )
    wc2.generate(word_space_split)  # 从字典生成词云
    image_colors = wordcloud.ImageColorGenerator(mask2)  # 从背景图建立颜色方案
    wc2.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案
    plt.imshow(wc2)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    plt.show()  # 显示图像

def main():
    visit_total()
    tag()
    News_num_per_day()
    source()
    title()
    comment()

if __name__ == '__main__':
    main()