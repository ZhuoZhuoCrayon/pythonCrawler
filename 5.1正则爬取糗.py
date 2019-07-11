"""     
    5.1 正则表达式-爬取糗图
    code utf8
    date 03/08/2019
    author caixiaoxin
"""

import urllib.parse
import urllib.request
import re
def download_image(content,file):
    # pattern = re.compile(r'<div class="thumb">.*?<img src="(.*?)" alt="(.*?)" />.*?</div>',re.S)
    """
    re.S 可以使 . 具有匹配换行的功能
    
    正则中加入括号，表示匹配的目标字段，也就是想要获取的信息
    
    pattern 为得到的图片的url
    _pattern 为得到图片相应的段子
    """
    pattern = re.compile(r'<div class="thumb">.*?<img src="(.*?)".*?</div>',re.S)
    _pattern = re.compile(r'div class="content".*?<span>(.*?)</span>.*?</div>',re.S)

    """
        findall：返回匹配目标字段的列表
    """
    image_urls = pattern.findall(content)
    image_titles = _pattern.findall(content)


    # 将爬取得到的图片url及段子写入文件
    for index in range(len(image_urls)):
        image_urls[index] = 'http:' + image_urls[index]
        try:
            file.writelines(image_urls[index] + ':\n' +
                            image_titles[index] + '\n\n')
        except:
            pass

def main():
    url = 'https://www.qiushibaike.com/pic/page/{}/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    }
    file = open('qiutu.html', 'w')

    start_page = 1
    end_page = 5
    for page in range(start_page,end_page+1):
        request = urllib.request.Request(url = url.format(page),headers = headers)
        content = urllib.request.urlopen(request).read().decode()
        download_image(content,file)

if __name__ == '__main__':
    main()
