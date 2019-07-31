import requests
import random
import os
from bs4 import BeautifulSoup
import threading

class crawler_pic(threading.Thread):
    begin_index = 0 # 起始页面
    end_index = 0   # 终止页
    grads = 20      # 爬取梯度：每个线程爬虫需要执行的爬取页数
    # 链接
    base_url = "http://www.win4000.com/wallpaper_big_154{}.html"
    # 图片保存根目录
    file_root = "D://pics_multi//"
    # 伪装浏览器
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
    def __init__(self, name, begin):
        threading.Thread.__init__(self)
        self.name = name
        self.begin_index = begin
        self.end_index = begin + self.grads
    # 获取
    def get_html(self, url):
        try:
            HTML = requests.get(url,headers=self.headers)
            HTML.raise_for_status()
            HTML.encoding = HTML.apparent_encoding
            return HTML.text
        except:
            print("In "+self.name+":ERROR Load "+url)
            return "NULL"
    # 将获取的图片存储至根目录下
    def store_pics(self,pic_urls):
        fileName = pic_urls[0]+"//"
        for picurl in pic_urls[1:]:
            # 构造图片存储地址
            path = self.file_root + fileName + picurl.split('/')[-1]
            print(path)

            try:
                # 需要逐层创建目录
                if not os.path.exists(self.file_root):
                    os.mkdir(self.file_root)
                # 如无该目录，先行构建
                if not os.path.exists(self.file_root+fileName):
                    os.mkdir(self.file_root+fileName)
                # 图片存在，不重复保存
                # 不存在，创建
                if not os.path.exists(path):
                    # request获取图片内容
                    pic = requests.get(picurl)
                    with open(path, 'wb') as f:
                        f.write(pic.content)
                        f.close()
                        print("图片:" + picurl + " 成功下载")
                else:
                    print("图片已存在")
            except:
                print("爬取失败")
        return 1

    # 在html页面中获取图片链接，返回链接列表
    def get_pic_urls(self, HTML):

        pic_urls = ["filename"]
        soup = BeautifulSoup(HTML, "html.parser")
        """
        页面分析：
        图片链接位于标签<div "id": "picBox", "class": "picBox">  -- <li> -- <img> [href:pic_url]
        获取最上层:div 全部子孙标签  选取a 获取a的属性信息
        """
        for tag in soup.find("div", attrs={"id": "picBox", "class": "picBox"}).descendants:
            if tag.name == 'img':
                pic_urls.append(tag.attrs['src'])
                pic_urls[0] = tag.attrs['title']
        """
        for a_tag in soup.find("div", attrs={"id": "picBox", "class": "picBox"}).findAll("a"):
            pic_urls.append(a_tag.attrs['href'])
        """
        # 全局，记录图片数量
        global pic_num
        pic_num += len(pic_urls) - 1
        return pic_urls

    # 线程方法
    def run(self):
        # 爬取一遍分配的页面
        for i in range(self.begin_index,self.end_index):
            html = self.get_html(self.base_url.format(i))
            # 页面爬取成功的情况下获取图片链接
            if html != "NULL":
                pic_urls = self.get_pic_urls(html)
                self.store_pics(pic_urls)
                """
                for pic in pic_urls:
                    print("in "+self.name+":"+pic)
                """


if __name__ == '__main__':

    threads = []
    count = 0
    pic_num = 0
    # 构造爬虫
    for begin in range(700,900,20):
        threads.append(crawler_pic("Thread-begin:"+str(begin),begin))

    # 开始爬取
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


    print(pic_num)