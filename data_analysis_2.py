#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tanshuai
# @Contact  : tyh9436@gmail.com
# @Software : PyCharm
# @File     : data_analysis.py
# @Time     : 2018/11/12 16:22

import pandas as pd
import matplotlib.pylab as plt
from pylab import mpl
from wordcloud import WordCloud
from scipy.misc import imread
import jieba
import sys


def get_salary_chart():
    # 2、计算薪资，25%比较接近现实
    df['salary'] = df['工资'].str.findall('\d+')

    avg_salary = []
    for k in df['salary']:
        int_list = [int(n) for n in k]
        avg_wage = int_list[0]+(int_list[1]-int_list[0])/4
        avg_salary.append(avg_wage)
    df['月工资'] = avg_salary
    df.to_csv('draft.csv', index=False)
    # print('岗位薪资比例: \n{}'.format(df['月工资'].describe()))

    # 3、薪资直方图
    plt.hist(df['月工资'], bins=24)
    plt.xlabel('工资(千元)')
    plt.ylabel('次数')
    plt.title('薪资直方图')
    plt.savefig('histogram.jpg')
    plt.show()


# 4、饼图
def get_region_chart():
    count = df['区域'].value_counts()
    print(count)
    plt.pie(count, labels=count.keys(), labeldistance=1.4, autopct='%2.1f%%')
    plt.axis('equal')
    plt.title('岗位地区分布图')
    plt.legend(loc='upper left', bbox_to_anchor=(-0.1, 1))
    plt.savefig('pie_chart.jpg')
    plt.show()


# 5、词云
def get_cloud_chart():
    text = ''
    for line in df['职位福利']:
        text += line

    cut_text = ' '.join(jieba.cut(text))
    cloud = WordCloud(
        font_path='Arial Unicode.ttf',
        background_color='white',
        mask=imread('./images/cloud.jpg'),
        max_words=1000,
        max_font_size=100
    )
    word_cloud = cloud.generate(cut_text)
    word_cloud.to_file('word_cloud.jpg')
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    # 使matplotlib模块能显示中文
    mpl.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    # 1、读取数据
    df = pd.read_csv('./JobPosition/Python开发.csv', encoding='utf-8')

    get_salary_chart()
    get_region_chart()
    get_cloud_chart()
