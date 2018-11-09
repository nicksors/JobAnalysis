#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tanshuai
# @Contact  : tyh9436@gmail.com
# @Software : PyCharm
# @File     : data_analysis.py
# @Time     : 2018/11/6 12:17

import pandas as pd
import matplotlib.pyplot as plt # 导入模块报错解决 https://www.cnblogs.com/harelion/p/5637767.html
from wordcloud import WordCloud
from scipy.misc import imread
import jieba
from pylab import mpl
import sys

# 使matplotlib模块能显示中文
mpl.rcParams['font.sans-serif'] = ['Arial Unicode MS'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

# 1、读取数据
filename = '运维工程师'
filename = 'dba'
filename = 'Python开发工程师'
filename = 'Python开发'
# filename = '运维开发工程师'
# filename = 'lagou_jobs'
# df = pd.read_csv('lagou_jobs.csv', encoding='utf-8')
df = pd.read_csv('./JobPosition/'+filename + '.csv', encoding='utf-8')
# print('./JobPosition/'+filename + '.csv')
# sys.exit()
# 2、计算薪水, 将字符串转化为列表, 再取区间的前25%, 比较贴近现实, 由于CSV文件内的数据是字符串形式,先用正则表达式将字符串转化为列表
pattern = '\d+'
df['salary'] = df['工资'].str.findall(pattern)

avg_salary = []
for k in df['salary']:
    int_list = [int(n) for n in k]
    avg_wage = int_list[0]+(int_list[1]-int_list[0])/4
    avg_salary.append(avg_wage)
df['月工资'] = avg_salary
# 2.1 将清洗后的数据保存,以便检查
df.to_csv('draft.csv', index=False)
# 2.2 描述统计
print('岗位工资描述：\n{}'.format(df['月工资'].describe()))

# '''
# 3、绘制频率直方图并保存
plt.hist(df['月工资'], bins = 12) # bins指定画多大的格子
plt.xlabel('工资 (千元)')
plt.ylabel('次数')
plt.title(filename + "工资直方图")
plt.savefig('histogram.jpg')
plt.show()
# '''


# '''
# 4、绘制饼图并保存
count = df['区域'].value_counts()
plt.pie(count, labels=count.keys(), labeldistance=1.4, autopct='%2.1f%%')
plt.axis('equal')  # 使饼图为正圆形
plt.title(filename + "岗位地区分布图")
plt.legend(loc='upper left', bbox_to_anchor=(-0.1, 1))
plt.savefig('pie_chart.jpg')
plt.show()
# '''

# '''
# 5、绘制词云,将职位福利中的字符串汇总
text = ''
for line in df['职位福利']:
   text += line
   
# 5.1 使用jieba模块将字符串分割为单词列表
cut_text = ' '.join(jieba.cut(text)) # 字符串分词
cloud = WordCloud(
       font_path='Arial Unicode.ttf',
       background_color='white', # 背景设置成(white)白色
       mask=imread('./images/cloud.jpg'), #设置背景图
       max_words=1000,
       max_font_size=100
       )

word_cloud = cloud.generate(cut_text)
# 5.2 保存词云图片
word_cloud.to_file('word_cloud.jpg')
plt.imshow(word_cloud)
plt.axis('off')
plt.show()
# '''
