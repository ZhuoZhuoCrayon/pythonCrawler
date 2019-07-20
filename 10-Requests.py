"""
    Requests库：安装 pip install requests
    官方文档：
        http://cn.python-requests.org/zh_CN/latest/
    what to do？
        与urllib功能相似
    get 请求
        定制头部 -requests.get(url=url,headers=headers,params=data)
        响应对象
            r.text 字符串形式查看响应
            r.content 字符类型查看响应
            r.encoding 查看或者设置编码类型
            r.status_code 查看响应状态
            r.headers 查看响应头部
            r.url 查看请求url
            r.json 查看json数据
            
    post 请求
        必应翻译
        requests.post(url=url,headers=headers,data=data)
    ajax、get、post
        和上面是一样的
    代理
        requests.get(url=url,headers=headers,proxies=proxy)
    cookie
        实现人人登陆
    留坑：
        教程中的chinaunix改版并且难以登陆操作，在此跳过
        如有解决方法，请联系我
"""

import requests


# 带头部的Requests应用
url = 'http://www.baidu.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.142 Safari/537.36',
}
request = requests.get(url=url,headers=headers)

request.encoding = 'utf-8'
# print(request.text)

# 带参数的get
# https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=中国
'''
    坑：一开始url用 'http://www.baidu.com/' 这个，
    结果在构造搜索请求时返回的一直是百度首页，尬住，请用下面这个
'''
url = 'http://www.baidu.com/s?'
data = {
    'ie':'utf-8',
    'wd':'中国'
}
request = requests.get(url=url,headers=headers,params=data)
request.encoding = 'utf-8'

with open('exe_file/10/baidu.html','wb') as fp:
    fp.write(request.content)




# post请求：必应翻译实战
url = 'https://cn.bing.com/tlookupv3?isVertical=1&&' \
      'IG=B25CDCC5FE9D4B2EA382D628AFEAFDCD&IID=translator.5028.5'
# 构造表单
data = {
    'from': 'zh-Hans',
    'to': 'en',
    'text': 'compute',
}
"""
request = requests.post(url=url,headers=headers,data=data)
# request.encoding = 'utf-8'
print(request.json())


# 代理的使用
url = 'https://www.baidu.com/s?ie=utf-8&f=8&' \
      'rsv_bp=1&rsv_idx=1&tn=baidu&wd=ip'
proxy = {
    'http':'http://113.54.153.217:1080'
}
request = requests.get(url=url,headers=headers,proxies=proxy)
request.encoding = 'utf-8'
with open('exe_file/10/set_proxy.html','wb') as fp:
    fp.write(request.content)
"""

"""
# 带cookie登陆
# 创建一个会话session,用于保存cookie信息，后续的请求利用session来发送
session = requests.Session()
url = 'http://www.renren.com/ajaxLogin/login?1=1'
formdata = {
    'email':'15625266605',
    'icode'	:'',
    'origURL':'http://www.renren.com/home',
    'domain':'renren.com',
    'key_id':'1',
    'captcha_type':	'web_login',
    'password':	'1162c49a98a09a374364c99e2ad203b82211bc9cfdf8411e3b47d3ae268ec869',
    'rkey':	'54fa0fe478cb62a6ae1184e8e15c9dbb',
    'f':'http%3A%2F%2Fwww.renren.com%2F969920379',
}

request = session.post(url=url,headers=headers,data=formdata)
# print(request.text)
# >>>{"code":true,"homeUrl":"http://www.renren.com/home"}

# 登陆后访问主页
home_url = 'http://www.renren.com/home'
home_page = session.get(url=home_url,headers=headers)
home_page.encoding = 'utf-8'
with open('exe_file/10/renren.html','wb') as fp:
    fp.write(home_page.content)

"""

