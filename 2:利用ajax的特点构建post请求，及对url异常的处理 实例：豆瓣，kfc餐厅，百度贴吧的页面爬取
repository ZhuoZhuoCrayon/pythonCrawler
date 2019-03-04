
"""
author:caixiaoxin
Ajax 即“Asynchronous Javascript And XML”（异步 JavaScript 和 XML），是指一种创建交互式网页应用的网页开发技术。
Ajax = 异步 JavaScript 和 XML 或者是 HTML（标准通用标记语言的子集）。
Ajax 是一种用于创建快速动态网页的技术。
Ajax 是一种在无需重新加载整个网页的情况下，能够更新部分网页的技术。
通过在后台与服务器进行少量数据交换，Ajax 可以使网页实现异步更新。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新
"""


import urllib.parse
import urllib.request





"""
                豆瓣爬取
"""
#如果url链接中出现我们要调配的参数并赋值常数，需要删除相关参数部分
url = "https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&"
page = 1
limit = 1
# 构建post表单
data = {
    'start':(page-1)*limit,
    'limit':limit,
}
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
}

"""
request = urllib.request.Request(url=url,headers=headers)
data = urllib.parse.urlencode(data).encode()
response = urllib.request.urlopen(request,data = data)
"""

# 等价于三部曲
query_string = urllib.parse.urlencode(data)
url += query_string

request = urllib.request.Request(url = url,headers=headers)
response = urllib.request.urlopen(request)

print(response.read().decode())















"""
                kfc爬取
"""
post_url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname'
form_data = {
    'cname': '深圳',
    'pid': '',
    'pageIndex': '2',
    'pageSize': '10',
}

request = urllib.request.Request(url = post_url,headers=headers)
form_data = urllib.parse.urlencode(form_data).encode()
response = urllib.request.urlopen(request,data = form_data)
print(response.read().decode())















"""
                贴吧爬取
"""

# tieba_url = 'http://tieba.baidu.com/f?ie=utf-8&kw=python&red_tag=d3356873073'
tieba_url = 'http://tieba.baidu.com/f?ie=utf-8'
# 页码变化参数 pn
# pn按50递增


for page in range(0,10):
    form_data = {
        'kw': 'python',
        'pn': (page-1)*50
    }
    form_data = urllib.parse.urlencode(form_data).encode()
    request = urllib.request.Request(url = tieba_url,headers = headers)
    response = urllib.request.urlopen(request,data = form_data)

    with open('tiebaPage//'+str(page)+'.html','wb') as file:
        file.write(response.read())





"""
            异常处理
"""
import urllib.error
url = 'http://www.maodan.com/'

#URLerror
try:
    response = urllib.request.urlopen(url)
except urllib.error.URLError as e:
    print(e)    #<urlopen error [Errno 11001] getaddrinfo failed>#

#HTTPerror

