#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tanshuai
# @Contact  : tyh9436@gmail.com
# @Software : PyCharm
# @File     : getinfo.py
# @Time     : 2018/11/6 11:43

import requests
import math
import pandas as pd
import time
import sys

def get_json(url, page_num): # 接收两个参数：地址、页数
    '''从网页获取JSON,使用POST请求,加上头部信息'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Host': 'www.lagou.com',
        'Referer':'https://www.lagou.com/jobs/list_python%E5%BC%80%E5%8F%91?labelWords=&fromSearch=true&suginput=',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest'
    }

    data = {'first': 'true', 'pn': page_num, 'kd': 'Python开发'}
    res = requests.post(url, headers=headers, data=data)
    res.raise_for_status()  # 如果请求错误，则抛出错误代码
    res.encoding = 'utf-8'
    # 得到包含职位信息的字典
    page = res.json()
    return page


def get_page_num(count):
    '''计算要抓取的页数'''
    # 每页15个职位,向上取整
    res = math.ceil(count/15)
    # 拉勾网最多显示30页结果
    if res > 30:
        return 30
    else:
        return res


def get_page_info(jobs_list):
    '''对一个网页的职位信息进行解析,返回列表'''
    page_info_list = []
    for i in jobs_list:
        job_info = []
        job_info.append(i['companyFullName'])       # 公司全名
        job_info.append(i['companyShortName'])      # 公司简称
        job_info.append(i['companySize'])           # 公司规模
        job_info.append(i['financeStage'])          # 融资阶段
        job_info.append(i['district'])              # 区域
        job_info.append(i['positionName'])          # 职位名称
        job_info.append(i['workYear'])              # 工作经验
        job_info.append(i['education'])             # 学历要求
        job_info.append(i['salary'])                # 工资
        job_info.append(i['positionAdvantage'])     # 职位福利
        page_info_list.append(job_info)
    return page_info_list


def main():
    # 第一步：确定获取数据的URL
    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'
    # 第二步：请求数据，获取总的职位数
    page_one = get_json(url, 1) # 先设定页数为1,获取总的职位数
    total_count = page_one['content']['positionResult']['totalCount']
    # 2.1 根据总的职位数，根据每页15个职位数分割，最后得到请求的次数
    num = get_page_num(total_count)
    # 2.2 第一次请求后暂停20秒，防止被封；
    time.sleep(20)
    print('职位总数:{},页数:{}'.format(total_count, num))

    total_info = []  # 存储所有抓取的数据
    for n in range(1, num+1):
        # 对每个网页读取JSON, 获取每页数据
        page = get_json(url, n)
        jobs_list = page['content']['positionResult']['result']
        page_info = get_page_info(jobs_list)
        total_info += page_info
        print('已经抓取第{}页, 职位总数:{}'.format(n, len(total_info)))
        # 每次抓取完成后,暂停一会,防止被服务器拉黑
        time.sleep(30)
    # 将总数据转化为data frame再输出
    df = pd.DataFrame(data=total_info, columns=['公司全名','公司简称','公司规模','融资阶段','区域','职位名称','工作经验','学历要求','工资','职位福利'])
    df.to_csv('./JobPosition/lagou_jobs.csv', index=False)
    print('已保存为csv文件.')

if __name__ == "__main__":
    main()
