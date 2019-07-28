import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.142 Safari/537.36',
}


# e：下载视频
"""
tip:视频播放窗口是无法右键F12的,正确的做法是在暂停、倍数的功能栏进入开发者模式，就可以简单获取视频的url
"""
url = 'http://v1-default.ixigua.com/0675cf76b8a56330683ebbae99e4986e/5d3bbed0/video/m/' \
      '220ed97da2708af47afa4bb16d59e4eba1f116131fb7000082d6359fa977/?rc=amd1NDY0dTtpajM' \
      'zPDczM0ApQHRAbzw7NTs6MzgzMzUzNDUzNDVvQGg2dilAZzN3KUBmM3UpZHNyZ3lrdXJneXJseHdmOzpAa' \
      'C1wNGtqMG9rXy0tLS0vc3MtbyNvIy8uMy0wMy4uMC4tNDQ2LTojbyM6YS1vIzpgLXAjOmB2aVxiZitgXmJmK15xbDojMy5e'

r = requests.get(url=url,headers=headers)

with open('exe_file/12/1.mp4','wb') as file:
    file.write(r.content)


'''
    首先向365yg.com发送请求
    获取响应，解析响应，将里面所有的标题链接获取到
    依次向每个标题链接发送请求
    获取响应，解析响应，获取video标签的src属性
    向src属性发送请求，获取响应，将内容保存到本地
'''

# 爬取主页的推荐视频
from lxml import etree
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# 请求指定url的内容
def handle_request(request_url):
    try:
        request = requests.get(url=request_url,headers=headers)
        request.raise_for_status()
        request.encoding = request.apparent_encoding
        return request
    except:
        print(request_url + ' get failed')
        return 'NULL'

# 解析视频页，获取视频的url
def handle_href(a_href)->str:
    # 通过chrome-headless解决
    path = r'exe_file/chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')  # 上面三行代码就是为了将Chrome不弹出界面，实现无界面爬取
    browser = webdriver.Chrome(path, options=chrome_options)
    browser.get(a_href)
    time.sleep(3)
    # 获取源码，生成tree对象，然后查找video里面的src属性
    '''
    code:tree = etree.HTML(browser.page_source,'lxml)
    TypeError: Argument 'parser' has incorrect type (expected lxml.etree._BaseParser, got str)
    去掉lxml完美解决
    '''
    # 利用xpath获取视频的url
    tree = etree.HTML(browser.page_source)
    video_src = tree.xpath('//video/@src')[0]
    browser.close()
    return video_src

# 获取主页的视频信息
def handle_title(widen:int):
    # json内容会根据widen属性变化
    basic_url = 'http://365yg.com/api/pc/feed/?max_behot_time=1564196117&category=video_new&utm_source=toutiao' \
          '&widen={}&tadrequire=true&as=A125ED93CB0BDA9&cp=5D3B3BBDAA498E1&_signature=.sLedBAXpAP3jqRhTQlB7.7C3m'
    # 获取请求
    request = handle_request(basic_url.format(widen))
    # 解析json数据
    json_obj = json.loads(request.text)
    # 取出与视频相关的数据,data是一个字典元素的列表，每个元素都是一个视频的所有信息
    data = json_obj['data']
    # 循环data列表，依次取出每一个视频信息
    for video_data in data:
        title = video_data['title']
        a_href = 'http://365yg.com' + video_data['source_url']
        print('downloading~...' + title)
        video_src = handle_href(a_href)
        # print(video_src)
        '''
            调用写好的函数，下载速度会慢很多
            request = handle_request(video_src)
            with open('exe_file/12/download/{}.mp4'.format(title), 'wb') as file:
            file.write(request.content)
        '''
        r = requests.get(url=url, headers=headers)
        with open('exe_file/12/download/{}.mp4'.format(title), 'wb') as file:
            file.write(r.content)
        print('finish')
def main():
    handle_title(1)
if __name__ == '__main__':
    main()