import requests
import json
from lxml import etree
import time

# 获取当前时间
localtime = time.asctime( time.localtime(time.time()) )

url = 'https://shenzhen.8684.cn'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.142 Safari/537.36',
}
result = []
# 请求指定url的内容
def handle_request(request_url):
    try:
        request = requests.get(url=request_url,headers=headers)
        request.raise_for_status()
        request.encoding = request.apparent_encoding
        return request.text
    except:
        print(request_url + ' get failed')
        return 'NULL'

# 首页导航
def parse_navigation():
    content = handle_request(request_url=url)
    tree = etree.HTML(content)

    # 获取以数字开头的连接
    number_href_list = tree.xpath('//div[@class="bus_kt_r1"]/a/@href')
    # 获取以字母开头的连接
    char_href_list = tree.xpath('//div[@class="bus_kt_r2"]/a/@href')
    # 将爬取的导航链接列表返回
    return number_href_list + char_href_list

# 爬取以1（数字或字符）开头的某条线路的所有公交线
def parse_singlePath(navi_list):
    # 遍历上面的列表，依次发送请求，解析内容，获取每一个页面
    for navi in navi_list:
        path_url = url + navi
        print(path_url)
        content = handle_request(request_url=path_url)
        # 解析内容，获取每一路公交具体的url
        parse_specialroute(content)

    pass

# 获取每一条具体公交线的链接尾缀及名称
def parse_specialroute(content):
    tree = etree.HTML(content)
    route_infos = tree.xpath('//div[@class="stie_list"]/a')
    # print(len(route_infos))
    for route_info in route_infos:
        # 该线路的url后缀
        route_suffix = route_info.xpath('.//@href')[0]
        # 名称
        route_name = route_info.xpath('.//@title')[0]
        # print(route_suffix,route_name)
        # 获取每一条具体公交线路的具体信息
        get_specialroute(route_suffix,route_name)

#获取每一条具体公交线路的具体信息
def get_specialroute(route_suffix,route_name):
    # 请求页面
    content = handle_request(url+route_suffix)
    tree = etree.HTML(content)
    # 公交信息的标签位置
    bus_basic_infos = tree.xpath('//div[@class="bus_i_content"]')[0]

    # 获取线路名称、运营时间、票价
    bus_name = bus_basic_infos.xpath('./div[@class="bus_i_t1"]/h1/text()')[0]\
                                    .replace('&nbsp','')     # 替换掉特殊编码
    bus_runtime = bus_basic_infos.xpath('./p[1]/text()')[0].replace('运行时间：','')
    bus_fares = bus_basic_infos.xpath('./p[2]/text()')[0].replace('票价信息：','')
    bus_company = bus_basic_infos.xpath('./p[3]/a/text()')[0]
    bus_update = bus_basic_infos.xpath('./p[4]/text()')[0].replace('最后更新：','')
    # print(bus_name)
    # print(bus_runtime)
    # print(bus_fares)
    # print(bus_company)
    # print(bus_update)

    # 获取线路站点
    '''
        坑：原本思路是找到//div[@class="bus_line_site"][1](第一个，也就是起点到终点的单程站集）
            下的--div[@class="bus_site_layer"]，但是一直找不到，所以最后直接找后者，这时得到的站集
            是来回的，取列表的1/2，可以得到单程站集
        填坑：实际上是"bus_line_site "，得再加一个空格
    '''
    bus_line = tree.xpath('//div[@class="bus_site_layer"]')
    length = len(bus_line)
    bus_line = bus_line[:int(length/2)]
    sites = []
    for line in bus_line:
        for site in line.xpath('./div'):
            sites.append(site.xpath('./a/text()')[0])
    # print(sites)

    bus_data = {
        '线路名称' : bus_name,
        '运行时间' : bus_runtime,
        '票价信息' : bus_fares,
        '运营公司' : bus_company,
        '更新时间' : bus_update,
        '经过站点' : sites,
    }

    # 公交线路放入结果中
    result.append(bus_data)



def main():
    # 获取导航页全部的线路（数字字母）开头的url
    navi_list = parse_navigation()

    # 爬取以某个（数字或字符）开头的某条线路的所有公交线
    parse_singlePath(navi_list)

    # 将bus_data 存入一个result列表，构造<"result":result>键值对并存入一个新字典
    # 将字典转成json格式并存入json文件
    shenzhen_busLine = {
        'json_name' : '深圳公交线路汇总',
        'updatetime' : localtime,
        'results' : result
    }
    file = open('exe_file/10/bus_line.json','w',encoding='utf-8')

    """
        json.dump()
        把字典转成json串，并自动写入文件中
        dump参数是（字典，文件句柄，indent）。indent用于缩进美化json串的
        ensure_ascii=False用于写文件时有unicode时用，正常显示出中文来
    """
    json.dump(shenzhen_busLine,file,indent=4,ensure_ascii=False)
if __name__ == '__main__':
    main()