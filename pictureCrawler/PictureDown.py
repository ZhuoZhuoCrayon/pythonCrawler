import requests
import re
import os
import time
url_root = 'http://www.win4000.com/wallpaper_big_154'
# http://www.win4000.com/wallpaper_big_154(3bits).html
user = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
pattern = re.compile(r'http://pic1.win4000.com/wallpaper/[\w|-]+/[\w]+.jpg')

def get_picture_url(suffix):
    try:
        url = url_root + str(suffix) + ".html"
        print(url)
        r = requests.get(url,headers = user)
        r.raise_for_status()
        validpart = r.text.split('当前位置')[-1]
        validpart = validpart.split('listBox')[0]
        picurl_list = pattern.findall(validpart)
        return picurl_list
    except:
        print("ERROR")
        return ["NULL"]

def store_pic(picurl_list):

    if "NULL" in picurl_list:
        return 0
    file_root = "D://pics//"

    for picurl in picurl_list:
        path = file_root + picurl.split('/')[-1]
        try:
            if not os.path.exists(file_root):
                os.mkdir(file_root)
            if not os.path.exists(path):
                pic = requests.get(picurl)
                with open(path,'wb') as f:
                    f.write(pic.content)
                    f.close()
                    print("图片:"+picurl+" 成功下载")
            else:
                print("图片已存在")
        except:
            print("爬取失败")
    return 1

if __name__ == '__main__':
    for suffix in range(800,900):
        store_pic(get_picture_url(suffix))
        time.sleep(5)