"""
TODO：xpath学习
TEST：段子网爬取
Author:caixiaoxin
Date:2019/7/10
"""
"""
    xpath?
        xml是用来存储和传输数据的
        和html的不同点：
            1 html是用来显示数据的，xml是用来传输的
            2 html是固定的，xml标签是自定义的
        <bookstore>
        <book>
            <title lang="en"> Harry Potter</title>
            <author> K.Rowling</author>
            <year>2005</year>
            <price>29.99</price>
        </book>
        </bookstore>
        
        <bookstore> 文档节点
        <author> K.Rowling</author> 元素节点
        lang="en" 属性节点
        
        // 不考虑位置的查找
        ./ 从当前节点开始往下查找
        .. 从当前节点的父结点查找
        @ 选取属性
        
        e:
        /bookstore/book 选取根节点bookstore下面所有直接子节点的book
        //book  选取所有的book
        bookstore//book 查找bookstore 下面所有的book,不管所在位置
        /bookstore/book[1] bookstore 里面的第一个book
        /bookstore/book[last()] bookstore里面的最后一个book
        /bookstore/book[position()<3] 前两个book
        //title[@lang] 所有带有lang属性的title
        //title[@lang='eng'] 所有的lang属性为eng的title节点
        * 任何元素节点
        
        
        属性定位
        //input[@id="kw"]
        //input[@class="g s_ btn"]
        层级定位
        //div[@id="head"]/div/div[2]/a[@class="toindex"]   --索引从1开始
        //div[@id="head"]//a[@class="toindex"]   --双斜杠表示下面的所有a节点，不管位置
        逻辑运算
        //input[@class="s_ipt" and @name="wd]
        模糊匹配
        contains://input[contains(@class,"s_i")]---所有input，有class属性，并且属性中带s_i节点
                //input[contains(text(),"爱")]
        starts-with://input[starts-with(@class,"s")]---所有的input，有class属性，并且属性以s开头
        取文本
        //div[@id="ul"]/a[5]/text()
        所有文本
        //div[@id="n1"]//text()   div下所有的文本
        
        取属性
        //div[@id="ul"]/a[5]/@href
        
        代码中应用xpath
        from lxml import etree
        将html文档变成一个对象，然后调用对象的方法去查找指定的节点
        1 本地文件
            tree=etree.parse
        2 网络文件
            tree=etree.HTML(网页字符串)
        
"""

# xpath测试

from lxml import etree
# 使用lxml.etree.parse()解析html文件，该方法默认使用的是“XML”解析器，所以如果碰到不规范的html文件时就会解析错误
# lxml.etree.XMLSyntaxError: Opening and ending tag mismatch: meta line 3 and head, line 3, column 87
# 创建html解析器，增加parser参数
parser = etree.HTMLParser(encoding="utf-8")
tree = etree.parse('exe_file/xpath.html', parser=parser)
# print(tree)

ret = tree.xpath('//div[@class="tang"]/ul/li[1]/text()')  #取文本
print(ret)  #out:['\r\n                停车坐爱枫林晚，霜叶红于二月花\r\n            ']

ret1 = tree.xpath('//div[@class="tang"]/ul/li[last()]/a/@href') #取属性
print(ret1) #out:['http://www.baidu.com/']

ret2 = tree.xpath('//div[@class="tang"]/ul/li[@class="love"]')  #层次定位
print(ret2)  #out:[<Element li at 0x1f4953f8788>, <Element li at 0x1f4953f8808>]

ret3 = tree.xpath('//div[@class="tang"]/ul/li[@class="love" and @name="yang"]') #逻辑定位
print(ret3)  #out:[<Element li at 0x1cb943b8788>]

ret4 = tree.xpath('//li[contains(@class,"l")]') #模糊搜索
print(ret4) #out:[<Element li at 0x201f60a8888>, <Element li at 0x201f60a8908>, <Element li at 0x201f60a8988>, <Element li at 0x201f60a89c8>, <Element li at 0x201f60a8a08>]

ret5 = tree.xpath('//li[contains(text(),"爱")]/text()')  #模糊文本搜索
print(ret5) #['\r\n                停车坐爱枫林晚，霜叶红于二月花\r\n            ', '爱就一个字，我只说一次', '爱情36计，我要立刻美丽']


ret6 = tree.xpath('//li[starts-with(@class,"li")]/text()') #模糊匹配
print(ret6) #['\r\n                乍暖还寒时候，最难将息\r\n            ', '\r\n                三杯两盏淡酒\r\n            ']

ret7 = tree.xpath('//div[@class="song"]//text()')
print(ret7) # ['\r\n        火药\r\n        ', '指南针', '\r\n        ', '印刷术', '\r\n        造纸术\r\n    ']


# 不建议采用，因为编码原因难以转换
ret8 = tree.xpath('//div[@class="song"]')  #提取拼接文本
str = ret8[0].xpath('string(.)')
print(str)
#        火药
#        指南针
#        印刷术
#        造纸术



"""
爬取段子网
"""
import urllib.request
import urllib.parse
from lxml import etree

# 构造url，返回请求内容
def handle_request(url,page):
    # 构造头部信息
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'duanziwang.com',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    # 构造相应页面的url
    url = url.format(page)
    print(url)
    request = urllib.request.Request(url, headers=headers)
    return request

# html内容解析
def parse_content(content):

    # 构造对象
    tree = etree.HTML(content)
    # 筛选本页面的文章概要列表
    article_list = tree.xpath('//article[@id and @class="post"]')
    # print(len(article_list))

    # 概要中提取信息
    for article in article_list:
        title = article.xpath('.//div[@class="post-head"]/h1/a/text()') [0]    #获取标题
        # print(title)
        text = article.xpath('.//div[@class="post-content"]//text()')   #获取文本
        content_text = ''
        for word in text:
            word = word.strip()
            content_text += word.replace('\n','').replace('\r','')
        # 空文本进行信息补充
        if len(content_text) == 0:
            content_text = "这个标题有点长"

        # 提取时间
        time = article.xpath('.//div[@class="post-meta"]/time[@class="post-date" and @datetime]/text()')[0]
        # print(time)

        # 提取点赞数
        like_num = article.xpath('.//div[@class="post-meta"]/time[@class="post-date"]/a/span/text()')[0]
        # print(like_num)

        print("title:" + title)
        print("time:" + time)
        print("like:" + like_num)
        print("text:" + content_text)
        print("------------------------------")


def main():
    # start_page = int(input('begin:'))
    # end_page = int(input('end:'))

    start_page = 1
    end_page = 100

    url = 'http://duanziwang.com/page/{}/'
    for page in range(start_page,end_page+1):
        request = handle_request(url, page)
        content = urllib.request.urlopen(request).read().decode()
        # print(content)

        parse_content(content)

if __name__ == '__main__':
    main()

