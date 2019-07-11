#  http://sc.chinaz.com/tupian/xingganmeinvtupian.html
"""
懒加载：只显示可视区的图片
实现方式
<img src2/data_src/总之不少src="图片路径">
监视 -> <img src="图片路径" src2="">
特点：找不到src
"""
import urllib.request
import urllib.parse
from lxml import etree
import os

#  构造请求
def handle_request(url, page):
    if page == 1:
        url = url.format('')
    else:
        url = url.format('_' + str(page))
    #print(url)
    # 构造头部信息
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    request = urllib.request.Request(url=url,headers=headers)
    return request

# 页面信息解析提取
def parse_content(content):
    tree = etree.HTML(content)
    # //div[@id="container"]/div/div/a/img/@src
    image_list = tree.xpath('//div[@id="container"]/div/div/a/img/@src2')
    # 懒加载
    # print(image_list)
    for image_url in image_list:
            download_image(image_url)

# 下载图片
def download_image(image_url):
    # 下载目录
    dirpath = 'exe_file/xinggan'
    # 不存在目录即创建
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    # 生成文件名
    filename = os.path.basename(image_url)
    # 加入文件
    filepath = os.path.join(dirpath, filename)

    # 构造头部信息
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    # 保存图片
    request = urllib.request.Request(url=image_url, headers=headers)
    response = urllib.request.urlopen(request)
    with open(filepath, 'wb') as fp:
        fp.write(response.read())


def main():
    url = 'http://sc.chinaz.com/tupian/xingganmeinvtupian{}.html'
    start_page = 1
    end_page = 2
    for page in range(start_page,end_page+1):
        request = handle_request(url, page)
        # UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 1: invalid start by
        # slove:headers有一句'Accept-Encoding': 'gzip, deflate'，删掉就好了
        content = urllib.request.urlopen(request).read().decode()
        parse_content(content)


if __name__ == '__main__':
    main()