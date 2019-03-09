"""     
    5.2 正则表达式-爬取励志网
    code utf8
    date 03/08/2019
    author caixiaoxin
"""


import urllib.parse
import urllib.request
import re
import os


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
}
# html文件头-不加会乱码
html_head = """
<head>
    <meta charset="UTF-8">
    <title>5.2正则：爬取励志网</title>
</head>
"""

file_address = 'lizhi.html'

# 文件存在则先删除原有文件
if os.path.exists(file_address):
    os.remove(file_address)
else:
    os.mkdir(file_address)

# 写入文件头
file = open(file_address,'a',encoding='utf8')
file.write(html_head)


# 获取url请求
def get_request(url):
    request = urllib.request.Request(url = url,headers = headers)
    return request

# 提取每篇文章的标题和链接
def parse_content(content):
    """
    # <a href="/lizhi/qianming/20180139714.html">努力，奋斗，坚持，不抛弃，不放弃，一切皆有可能</a>
    # <h3><a href="/lizhi/qianming/20190241246.html"><b>我不知道年少轻狂，我只知道胜者为王——追梦赤子心</b></a></h3>
    查出标签有两个版本，一个带b标签，一个没有
    决定暂时保留b标签，过后单独处理
    """

    pattern = re.compile(r'<h3><a href="(/lizhi/qianming/\d+.html)">(.*?)</a></h3>')

    articleList = pattern.findall(content)
    # print(len(articleList))
    for article in articleList:
        # 可能出现带b标签的标题，清除
        # article[1].replace('</b>','').replace('<b>','')
        get_text(url = 'http://www.yikexun.cn'+article[0],title = article[1].replace('</b>','').replace('<b>',''))


# 提取文章内容
def get_text(url,title):
    request = urllib.request.Request(url = url,headers = headers)
    content = urllib.request.urlopen(request).read().decode()

    # 提取文章内容
    pattern = re.compile(r'<div class="neirong">(.*?)</div>',re.S)
    article = pattern.findall(content)[0].strip()


    """
    bug：
    写入html后打开，会出现文章渐进的排版错误
    
    源：因为有些文章结尾不明多出<p>，缺失结束标签 </li></ol>
    
    修复：去除内容结尾空格，检查尾缀是否为<p> ，将<p>替换成结束标签 </li></ol>
    """
    title = title.strip()
    if article[-3:] == "<p>":
        article = article[:-3] + "</li></ol>"



    # 美化：去除所有无法加载（其实也就是全部）的图片
    # <img src="/uploads/image/201901/121547293661170287.png" title="121547293661170287.png" alt="v2-fbdde028d48d572b2425965acf058add_hd.png">
    image_pattern = re.compile(r'<img .*?/>')

    """
        这个替换挺简便的
    """
    article = image_pattern.sub('',article)
    parse_html(title = title,article = article)



# 文章写入html文件
def parse_html(title,article):

    #标题加上h1标签，设置每篇文章排版
    complete_arc = '<h1>%s</h1>%s\n\n'%(title,article)

    file.write(complete_arc)



def main():
    url = 'http://www.yikexun.cn/lizhi/qianming/list_50_{}.html'
    start_page = 1
    end_page = 10

    for page in range(start_page,end_page+1):
        request = get_request(url.format(page))

        #预览页（主页内容）
        content = urllib.request.urlopen(request).read().decode()
        parse_content(content)






if __name__ == '__main__':
    main()

