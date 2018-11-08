[TOC]

## 1、简介
近年来Python之火大家都有感而知，那亲们知道北京的Python开发岗位、运维开发岗位招聘地域都是如何分布的吗？薪水如何？是否有前景等等，这些数据呢直接通过招聘信息来了解到企业用人是最直接的，也是最简单的途径。
那本次分享将通过Python来抓取拉钩的招聘信息，然后加以分析，做一个北京的Python职位地域分布、薪资范围、福利待遇等维度出一个简单的分析报告，希望能帮助到想在Python这片田地耕耘的童鞋在发展方向上有所参考。


## 2、用到的工具
使用Python的requests工具到招聘网站爬取我们想要的数据，分析和可视化也使用Python的相关模块来实现，主要有如下：
- Python版本：Python 3.x
- requests：发起请求，从网站抓取数据
- math：数学运算函数，向上取整，这里主要用于分析数据
- time：时间模块，主要是控制爬虫不会因为频繁请求而被网站拉进小黑屋
- pandas：数据抓取后使用该模块保存为csv文件到本地
- matplotlib：可视化画图
- pylab：设置画图能显示中文
- wordcloud、scipy、jieba（字符串分割成单词）：生成中文词云


## 3、数据抓取
使用Chrome打开拉钩网站，在网站输入“Python开发”职位，使用“检查”功能查看网页源码。发现拉钩有反爬机制，职位信息并不在源代码里，而是在JSON文件里，因此直接通过JSON获取数据即可。

![拉钩页面分析](https://github.com/nicksors/JobAnalysis/blob/master/images/lagou_page.png)



抓取信息时，需要加上头部信息，才能获取到数据。（原理很简单：你得伪装成一个正常的client去请求网页才能拿到想要的数据）
```
def get_json(url, num):
    '''从网页获取JSON,使用POST请求,加上头部信息'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Host': 'www.lagou.com',
      'Referer':'https://www.lagou.com/jobs/list_python%E5%BC%80%E5%8F%91?labelWords=&fromSearch=true&suginput=',
        'X-Anit-Forge-Code': '0',
      'X-Anit-Forge-Token': 'None',
      'X-Requested-With': 'XMLHttpRequest'
    }

    data = {
        'first': 'true',
        'pn': num,
        'kd': 'Python开发'}
    res = requests.post(url, headers=headers, data=data)
    res.raise_for_status()
    res.encoding = 'utf-8'
    # 得到包含职位信息的字典
    page = res.json()
    return page
```
在搜索结果的第一页，我们可以从JSON里读取总职位数，按照每页15个职位，获得要爬取的页数。再使用循环按页爬取，将职位信息汇总，输出为CSV格式。

**程序运行如下：**

![运行结果](https://github.com/nicksors/JobAnalysis/blob/master/images/count_info.png)


**抓取结果如下：**

![抓取结果](https://github.com/nicksors/JobAnalysis/blob/master/images/count_results.png)


## 4、数据可视化画图展示

### 4.1 根据薪资制作直方图

薪资比例描述和可视化出图

![薪资描述](https://github.com/nicksors/JobAnalysis/blob/master/images/Salary.png)

![薪资直方图](https://github.com/nicksors/JobAnalysis/blob/master/images/histogram.png)    


根据上面的出图信息我们能知道，Python开发的薪资范围大概在15k-25k居多，也有20%在30k以上，最高能到60k左右每月，所以发展前景开始非常好滴！还犹豫什么？赶紧入坑吧！从此走上人生巅峰，迎接白富美指日可待，哈哈。

### 4.2 根据岗位地域分布制作饼图

![饼图](https://github.com/nicksors/JobAnalysis/blob/master/images/pie_chart.png)



根据上面的可视化信息，你不难发现，北京的岗位地区分布非常明显，海淀区和朝阳区占据所有岗位的90%之多，所以在找工作的时候，如果你不考虑这两个工作地区的话，那你就失去了90%的就业机会，哈哈！害不害怕！！

### 4.3 制作词云

将职位福利这一列数据进行汇总，按照词语出现的频率生成云词实现Python可视化，以下是原图和云词图对比：刻间五险一金、六险一金、团队气氛、弹性工作、发展空间好等字眼出现的平率最高。（你看到“周末双休”了么？说明要想高薪，少休息多努力哈！）

![词云](https://github.com/nicksors/JobAnalysis/blob/master/images/word_cloud.png)


## 5、结论报告
1、北京的就业机会主要集中分布在“海淀区”和“朝阳区”，这两个区域占据90%左右的机会，其他几个区只有10%的机会。，如果你不考虑这两个工作地区的话，那你就失去了90%的就业机会，所以在考虑地区的时候需要注意下这个问题。
2、Python开发的薪资范围主要集中在15K-25K，20%的人在30K-35K左右，存在高薪60K的，有进一步的发展空间，前景还是令人期待的。
3、工作经验需求集中在2-5年，比较年轻化，但是学历90%需要本科，所以本科以下的同学们，需要加强你的能力去补充短板哈！
4、福利待遇基本都能给到五险一金，在保证这一点的同时，大家还是趁年轻那几年多努力以下，将来会感谢你自己的。

最后送给大家一句话：现在苦，苦一个人；将来苦，苦一家人。这句话也激励着我，大家加油，遇见明天美好的自己。

文完。

