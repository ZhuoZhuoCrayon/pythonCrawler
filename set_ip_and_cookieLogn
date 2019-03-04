
"""
    Handler处理器，自定义Opener
    urlopen() 给一个url，发送请求，获取响应
    Request() 定制请求头，创建请求对象
    高级功能：使用代理，cookie
    
    代理：
        配置：浏览器配置:高级-代理设置
        代码配置：就此可以在xici上爬取ip代理，然后随机分配给爬虫，来突破爬取网站所给的爬取频率
                同时也防止自身ip被封
    cookie
        #服务器端访问网站所留下的识别信息#
        模拟登陆：抓包获取cookie
        通过cookieJar保存模拟登陆所得到的cookie
"""







"""利用handler和opener获取页面的基本操作"""
import urllib.request
import urllib.parse

url = 'http://baidu.com/'

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
}

#  创建
handler = urllib.request.HTTPHandler()

# 通过hander创建一个opener,使用opener中的方法发送请求
opener = urllib.request.build_opener(handler)

# 构建请求对象
request = urllib.request.Request(url,headers=headers)

# 发送请求
response = opener.open(request)
# print(response.read().decode())










"""
利用ProxyHandler进行ip伪装
ip伪装会出现问题，留坑
在西刺网获取ip进行实践成功率非常低
响应时间过长及ip伪装失败（成功响应但是ip仍为本机）
"""

url = 'https://baidu.com/s?'
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
}
data = {
    'ie' : 'utf-8',
    'wd' : 'ip',
}
# 构造表单请求链接
query_string = urllib.parse.urlencode(data)
url += query_string

# 伪装ip格式
handler = urllib.request.ProxyHandler({'http':'121.232.148.73:9000'})
opener = urllib.request.build_opener(handler)

request = urllib.request.Request(url,headers=headers)
# 很神奇，三部曲失效，所以只能构造url了
# data = urllib.parse.urlencode(data).encode()
response = opener.open(request)

with open("ip1.html",'wb') as file:
    file.write(response.read())







"""
利用fiddler抓取cookie实现人人网主页的获取
并没有抓取登陆时的json因为文件特别特别多
抓取的json来源于进入主页所发送的表单请求

问题：cookie是实时的，所以该方法捕获的cookie需要实时抓包，过期失效

该问题引出下一个实例，登陆人人网并进入个人主页
"""

renren_url = 'http://www.renren.com/969920379/profile'

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    'Cookie': 'anonymid=jsrj643rtki53d; depovince=GUZ; _r01_=1; ln_uact=15625266605; '
              'ln_hurl=http://head.xiaonei.com/photos/0/0/men_main.gif; ick_login=c8e7f87f-75da-4f2f-b840-104909404637; '
              'first_login_flag=1; JSESSIONID=abcJbn-wkjg1eh_WTZiLw; jebecookies=7817aaaf-eb35-4f05-b071-f3e5f75f07c2|||||;'
              ' _de=E00E5A467C4B17304268C536701AF72D; p=c14a2da80879c2daa73cc1a3853720609; t=1e2cbc27606389927d404e61f48774c19; '
              'societyguester=1e2cbc27606389927d404e61f48774c19; id=969920379; xnsid=b72aafa1; ver=7.0; loginfrom=null; '
              'wp_fold=0log=[{"hostId":"969920379","targetTag":"name_click","sendUserId":"969920379"}]&requestToken=-1644252112&_rtk=69bfb28a',
}

request = urllib.request.Request(url = renren_url,headers = headers)
response = urllib.request.urlopen(request)

with open('renren.html','wb') as file:
    file.write(response.read())












"""
    http.cookiejar的应用，保存cookie，通过保存的cookie访问主页
    密码是加密过的，所以并不能构造表单实现登陆
    表单的获取需要手动登陆得到post请求
    登陆后，由于cookie提前保存，所以能够登陆该账号的其他页面
"""


import http.cookiejar
#模拟真实浏览器，发送完post请求猴，将cookie保存到代码中

# 创建一个cookie对象
cj = http.cookiejar.CookieJar()
# 通过cookie创建一个handler
handler = urllib.request.HTTPCookieProcessor(cj)
# 根据handler创建一个opener
opener = urllib.request.build_opener(handler)

url = 'http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=2019212154558'
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
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
}

request = urllib.request.Request(url = url,headers = headers)
formdata = urllib.parse.urlencode(formdata).encode()
response = opener.open(request,data = formdata)



get_url = 'http://www.renren.com/969920379/profile'

# 进入自己的主页
request = urllib.request.Request(url=get_url,headers = headers)
response = opener.open(request)

with open('renren.html','wb') as file:
    file.write(response.read())



