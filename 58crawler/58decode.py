import re
import lxml.html
import base64
from fontTools.ttLib import TTFont
import requests
import random
import sqlite3
import time

db = sqlite3.connect("58.db")
cursor = db.cursor()

UA = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
]
# https://sz.58.com/shixia/chuzu/pn68/?PGTID=0d3090a7-017c-74d8-4e30-b085460b77a1&ClickID=2
# https://sz.58.com/shixia/chuzu/pn66/?PGTID=0d3090a7-017c-74e7-0457-6697c22f0410&ClickID=2
headers = {
    "User-Agent": random.choice(UA)
}


def resp(i):

    base_url = "https://sz.58.com/chuzu/pn{}/?key=大望&PGTID=0d3090a7-017c-74d8-4e30-b085460b77a1&ClickID=2"
    response = requests.get(base_url.format(i), headers=headers)
    print("正在下载:", response.url)
    return response


def get_base64_str(response):
    base_font = re.compile("base64,(.*?)\'")
    base64_str = re.search(base_font, response.text).group().split(',')[1].split('\'')[0]
    return base64_str


def make_font_file(base64_str):
    b = base64.b64decode(base64_str)
    with open("58.ttf", "wb") as f:
        f.write(b)


def make_dict():
    font = TTFont('58.ttf')
    b = font['cmap'].tables[2].ttFont.getReverseGlyphMap()  # 编码对应的数字
    c = font['cmap'].tables[2].ttFont.tables['cmap'].tables[1].cmap  # 页面的十六进制数对应的编码
    return b, c


def parse_title(text):
    s = ""
    title_re = re.compile("\s")
    html = lxml.html.fromstring(text)
    title = html.xpath('//a[@class="strongbox"]//text()')[0]
    title = re.sub(title_re, '', title)
    for i in title:
        encode_str = str(i.encode("unicode-escape")).split(r'\\u')[-1].replace('\'', '').replace(r'b(', '').strip()
        try:
            num, code = make_dict()
            if len(encode_str) != 4:
                i = i
            elif int(encode_str, 16) not in code:
                i = i
            else:
                i = str(num[code[int(encode_str, 16)]] - 1)
            s += i
        except:
            s = "None"
    return s


def parse_price(text):
    s = ""
    html = lxml.html.fromstring(text)
    price_code = html.xpath('//div[@class="money"]/b/text()')[0]
    price_code = price_code.strip().replace('\r\n', '').replace(' ', '')
    price_encode_str = str(price_code.encode("unicode-escape")).split('\'')[1].split('-')
    if len(price_encode_str) > 1:
        s1 = ""
        s2 = ""
        encode_list1 = price_encode_str[0].split(r"\\u")[1:]
        encode_list2 = price_encode_str[1].split(r"\\u")[1:]
        for i in encode_list1:
            price = int(i, 16)
            num, code = make_dict()
            s1 += str(num[code[price]] - 1)
        for i in encode_list2:
            price = int(i, 16)
            num, code = make_dict()
            s2 += str(num[code[price]] - 1)
        s = s1 + '-' + s2

    else:
        str_list = price_encode_str[0].split(r'\\u')[1:]
        for i in str_list:
            price = int(i, 16)
            try:
                num, code = make_dict()
                s += str(num[code[price]] - 1)
            except:
                s = "None"

    return s


def parse_room(text):
    s = ""
    html = lxml.html.fromstring(text)
    p_rooms = html.xpath('//p[@class="room strongbox"]/text()')[0]
    room_re = re.compile('[\s]')
    room_re1 = re.compile(r'[m²]')
    room_re2 = re.compile(r'/')
    rooms = re.sub(room_re, '', p_rooms)
    rooms = re.sub(room_re1, "平米", rooms)
    rooms = re.sub(room_re2, "至", rooms)
    for i in rooms:
        # print(i.encode("unicode-escape"))
        encode_str = str(i.encode("unicode-escape")).split(r'\\u')[-1].replace('\'', '').replace(r'b/', '').strip()
        # print(encode_str)
        try:
            num, code = make_dict()
            if len(encode_str) != 4:
                i = i
            elif int(encode_str, 16) not in code:
                i = i
            else:
                i = str(num[code[int(encode_str, 16)]] - 1)
            s += i
        except:
            s = "None"
    return s

#debug
def parse_dist(text):
    s = ""
    html = lxml.html.fromstring(text)
    p_dist_re = re.compile('\skm')
    try:
        p_dist = html.xpath('//p[@class="add"]/text()')[3]
        p_dist = ''.join(p_dist).replace(' ', '')
        p_dist = re.sub(p_dist_re, '千米', p_dist)
        for i in p_dist:
            encode_str = str(i.encode("unicode-escape")).split(r'\\u')[-1].replace('\'', '').replace(r'\\r',
                                                                                                     '').replace(r'\\n',
                                                                                                                 '').replace(
                r'b.', '').strip()
            num, code = make_dict()
            if len(encode_str) != 4:
                i = i
            elif int(encode_str, 16) not in code:
                i = i
            else:
                i = str(num[code[int(encode_str, 16)]] - 1)
            s += i
        dist = s
    except:
        dist = "暂无"
    return dist


def short_rent(text):
    html = lxml.html.fromstring(text)
    try:
        rent = html.xpath('//p[@class="room"]/b/text()')[0]
    except:
        rent = "不可短租"
    return rent


def parse_li(response):
    li_re = re.compile('<li logr([\s\S]*?)</li>')
    li_list = re.findall(li_re, response.text)
    return li_list


def parse_target(text):
    html = lxml.html.fromstring(text)
    try:
        target = html.xpath('//p[@class="spec"]/span/text()')
        target = ','.join(target)
    except:
        target = "暂无"
    return target


if __name__ == '__main__':
    for i in range(1, 71):
        response = resp(i)
        time.sleep(5)
        base64_str = get_base64_str(response)
        make_font_file(base64_str)
        make_dict()
        li_list = parse_li(response)
        for i in li_list:
            # print(i)
            title = parse_title(i)
            price = parse_price(i)
            room = parse_room(i)
            dist = parse_dist(i)
            rent = short_rent(i)
            target = parse_target(i)
            city = "深圳"
            print(title,price,room,dist,rent,target)
            # cursor.execute("insert into home(title, price, room, dist, rent,target, city) values (?,?,?,?,?,?,?)",
            #                [title, price, room, dist, rent, target, city])
            db.commit()
