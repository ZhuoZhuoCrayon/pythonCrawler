import requests
import random
import _thread
import threading
import re
from bs4 import BeautifulSoup
UA = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
    ]
# 随机构造头部信息
headers = {
    "User-Agent": random.choice(UA)
}
global thread_max_num
thread_max_num = 20
init_links = ['http://www.win4000.com/wallpaper_193_0_0_1.html', 'http://www.win4000.com/wallpaper_0_0_0_1.html',
             'http://www.win4000.com/hj/haolanzhuan.html', 'http://www.win4000.com/wallpaper_192_0_0_1.html',
             'http://www.win4000.com/wallpaper.html', 'http://www.win4000.com/wallpaper_detail_155224.html',  'http://www.win4000.com/mt/index.html',
             'http://www.win4000.com/wallpaper_201_0_0_1.html', 'http://www.win4000.com/meitu.html',
             'http://www.win4000.com/wallpaper_197_0_0_1.html', 'http://www.win4000.com/wallpaper_195_0_0_1.html',
             'http://www.win4000.com/mobile.html', 'http://www.win4000.com/retu.html','http://www.win4000.com'
             'http://www.win4000.com/wallpaper_194_0_0_1.html', 'http://www.win4000.com/zt/index.html',
             'http://www.win4000.com/hj/index.html', 'http://www.win4000.com/wallpaper_191_0_0_1.html',
             'http://www.win4000.com/wallpaper_196_0_0_1.html', 'http://www.win4000.com/mt/star.html']
pages = set()
class myThread(threading.Thread):
    def __init__(self,name,url):
        threading.Thread.__init__(self)
        self.name = name
        self.url = url
    def run(self):
        crawler(self.name,self.url,1)

def get_html(url):
    try:
        HTML = requests.get(url, headers=headers)
        HTML.raise_for_status()
        HTML.encoding=HTML.apparent_encoding
        return HTML.text
    except:
        # print("ERROR:"+url)
        return "NULL"


def crawler(thread_name,url,depth):
    if depth > 20:
        return
    demo = get_html(url)
    try:
        soup = BeautifulSoup(demo,"html.parser")
        get_pic_url(soup)
        for link in soup.findAll("a",href=re.compile("http://www.win4000.com/[\S]*.html")):
            if "href" in link.attrs:
                if link.attrs['href'] not in pages:
                    newpage = link.attrs['href']
                    pages.add(newpage)
                    crawler(thread_name,newpage,depth+1)


    except:
        print("e!")
        pass
# <div class="paper-down">
# <a href="http://pic1.win4000.com/pic/6/68/5d2043f8a5.jpg?down" class="">下载图片</a>
pic_urls = set()
def get_pic_url(soup):
    try:
        a_tag = soup.find("div",attrs={"class":"paper-down"}).a
        if "href" in a_tag.attrs:
            pic_url = a_tag['href']
            if pic_url not in pic_urls:
                title = soup.find("h1").string
                pic_urls.add(pic_url)
                print("NO."+str(len(pic_urls))+"-"+title+":"+pic_url)
    except:
        pass


threads = []
counter = 0
for link in init_links:
    threads.append(myThread(str(counter),link))
    counter += 1
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

"""
url = "http://www.win4000.com/wallpaper_detail_40709.html"
demo = get_html(url)
soup = BeautifulSoup(demo,"html.parser")
get_pic_url(soup)
"""