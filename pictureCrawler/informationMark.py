# XML
""" 
<img(Name) [src="china.jpg"(Tag) size="10"](Attribute)>...</img>
缩写  <img src="china.jpg" size="10"/>
注释 <!-- This i a comment -->
"""
#JSON 有类型的键值对
"""
"key" : "value"
"key" : ["value1","value2"]
"key" : {"subkey" : "subvalue"}   嵌套键值对采用花括号
"""

# YAML 缩进体现所属关系
"""
1: "|"表示整块可跨行信息

key : value
key : #comment
- value1
- value2
key :
    subkey : subvalue 
"""

from bs4 import BeautifulSoup
import requests
import re

r = requests.get("https://st.58.com/chuzu/?PGTID=0d100000-0030-f99b-60c3-61bb358828a0&ClickID=3")
demo = r.text
soup = BeautifulSoup(demo,"html.parser")
# print(soup.prettify())
"""
for link in soup.find_all('a'):
    print(link.get('href'))
"""
allTag=[]
for tag in soup.find_all("div","des"):
    a_soup = BeautifulSoup(tag.text,"html.parser")
    for a_tag in a_soup("a",tongji_label="listclick",
                       onclick="clickLog('from=fcpc_zflist_gzcount');",
                       target="_blank",rel="nofollow"):
        print(str(a_tag.string).strip())
    for a_tag in soup.find_all("p","room strongbox"):
        print(str(a_tag.string).strip())


# 利用正则搜索
allTag = []
for tag in soup.find_all(re.compile('h')):
    if tag.name not in allTag:
        allTag.append(tag.name)
        # print(tag.name)
    else:
        pass

# 重点！！！
# 规定标签"img" 及标签属性 alt="孟子义写真图片高清桌面壁纸" 可准确找到所查找信息，"孟子义写真图片高清桌面壁纸"是准确匹配
# 模糊匹配用正则
for tag in soup.find_all("img",alt="孟子义写真图片高清桌面壁纸"):
    print(tag.get('src'))