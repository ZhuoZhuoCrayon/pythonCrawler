"""
多线程爬虫
    分析
        两类线程：下载、解析
        内容队列：下载线程往队列中put数据，解析线程从队列get数据
        数据
            url队列:下载线程从url队列中get数据
            写数据：上锁
            
"""
import threading
import requests
import json
from lxml import etree
from queue import Queue
import time
import timeit

# 队空退出标志
navi_EXIT = False
line_EXIT = False
route_EXIT = False
data_EXIT = False

# 获取当前时间
localtime = time.asctime( time.localtime(time.time()) )

url = 'https://shenzhen.8684.cn'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.142 Safari/537.36',
}
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

# 获取页面线程类-获取关键字页面
class crawlerThread_getLine(threading.Thread):
    def __init__(self, threadName, naviQueue, lineQueue):
        super(crawlerThread_getLine, self).__init__()

        self.threadName = threadName
        self.naviQueue = naviQueue
        self.lineQueue = lineQueue
    def run(self):
        # 需保证主线程中队列空才能退出
        while not navi_EXIT:
            try:
                navi = self.naviQueue.get(False)    # 设置False是为了避免队空阻塞死循环现象
                content = handle_request(url + navi)
                self.lineQueue.put(content)
            except:
                pass

# 解析线程-将关键字页面中对应的线路url及名称解析出来
class parseThread_getline(threading.Thread):
    def __init__(self, threadName, lineQueue, routeQueue):
        super(parseThread_getline, self).__init__()
        self.threadName = threadName
        self.lineQueue = lineQueue
        self.routeQueue = routeQueue
    def parse(self, content):
        tree = etree.HTML(content)
        route_infos = tree.xpath('//div[@class="stie_list"]/a')
        # print(len(route_infos))
        for route_info in route_infos:
            # 该线路的url后缀
            route_suffix = route_info.xpath('.//@href')[0]
            # 名称
            route_name = route_info.xpath('.//@title')[0]
            # print(route_suffix,route_name)
            self.routeQueue.put((route_suffix, route_name))

    def run(self):
        while not line_EXIT:
            try:
                content = self.lineQueue.get(False)
                self.parse(content)
            except:
                pass

# 获取页面线程-获取具体线路信息页
class crawlerThread_getRoute(threading.Thread):
    def __init__(self, threadName, routeQueue, dataQueue):
        super(crawlerThread_getRoute, self).__init__()

        self.threadName = threadName
        self.routeQueue = routeQueue
        self.dataQueue = dataQueue

    def run(self):
        while not route_EXIT:
            try:
                route_suffix, route_name = self.routeQueue.get(False)
                content = handle_request(url + route_suffix)
                # print(content)
                self.dataQueue.put(content)
            except:
                pass

# 解析线程-解析具体线路的信息
class parseThread_getRoute(threading.Thread):
    def __init__(self, threadName, dataQueue, result, lock):
        super(parseThread_getRoute, self).__init__()
        self.threadName = threadName
        self.dataQueue = dataQueue
        self.result = result
        self.lock = lock
    def parse(self, content):
        tree = etree.HTML(content)
        # 公交信息的标签位置
        bus_basic_infos = tree.xpath('//div[@class="bus_i_content"]')[0]

        # 获取线路名称、运营时间、票价
        bus_name = bus_basic_infos.xpath('./div[@class="bus_i_t1"]/h1/text()')[0] \
            .replace('&nbsp', '')  # 替换掉特殊编码
        bus_runtime = bus_basic_infos.xpath('./p[1]/text()')[0].replace('运行时间：', '')
        bus_fares = bus_basic_infos.xpath('./p[2]/text()')[0].replace('票价信息：', '')
        bus_company = bus_basic_infos.xpath('./p[3]/a/text()')[0]
        bus_update = bus_basic_infos.xpath('./p[4]/text()')[0].replace('最后更新：', '')
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
        bus_line = bus_line[:int(length / 2)]
        sites = []
        for line in bus_line:
            for site in line.xpath('./div'):
                sites.append(site.xpath('./a/text()')[0])
        # print(sites)

        bus_data = {
            '线路名称': bus_name,
            '运行时间': bus_runtime,
            '票价信息': bus_fares,
            '运营公司': bus_company,
            '更新时间': bus_update,
            '经过站点': sites,
        }
        # print(bus_data)
        with self.lock:
            # 公交线路放入结果中
            self.result.append(bus_data)
            print('\r' + self.threadName + '-当前已爬取线路数量：' + str(len(self.result)),end=' ')
    def run(self):
        while not data_EXIT:
            try:
                content = self.dataQueue.get(False)
                self.parse(content)
            except:
                pass

def main():

    # 初始化队列
    naviQueue = Queue()
    lineQueue = Queue()
    routeQueue = Queue()
    dataQueue = Queue()

    result = []
    # 设置锁
    # 但好像没必要，因为list本来就是线程安全？？？
    lock = threading.Lock()

    # 获取导航页面
    navi_list = parse_navigation()
    for navi in navi_list:
        naviQueue.put(navi)

    # -------------------------------------------------------------------------------------------
    # 开启获取线程
    craw_getLine = ['craw-getLine' + str(i) for i in range(16)]
    # craw_getLine = ['craw-getLine1', 'craw-getLine2', 'craw-getLine3', 'craw-getLine4']
    craw_getLine_Threads = []
    for threadName in craw_getLine:
        thread = crawlerThread_getLine(threadName, naviQueue, lineQueue)
        thread.start()
        craw_getLine_Threads.append(thread)

    #-------------------------------------------------------------------------------------------
    # 开启解析线程-获取以某个关键字开头的所有线路概要信息
    parse_getLine = ['parse-getLine' + str(i) for i in range(16)]
    # parse_getLine = ['parse-getLine1', 'parse-getLine2', 'parse-getLine3', 'parse-getLine4']
    parse_getLine_Threads = []
    for threadName in parse_getLine:
        thread = parseThread_getline(threadName, lineQueue, routeQueue)
        thread.start()
        parse_getLine_Threads.append(thread)

    # -------------------------------------------------------------------------------------------
    # 开启获取线程-获取具体的线路信息页
    craw_getRoute = ['craw-getRoute' + str(i) for i in range(16)]
    # craw_getRoute = ['craw-getRoute1', 'craw-getRoute2', 'craw-getRoute3', 'craw-getRoute4']
    craw_getRoute_Threads = []
    for threadName in craw_getRoute:
        thread = crawlerThread_getRoute(threadName, routeQueue, dataQueue)
        thread.start()
        craw_getRoute_Threads.append(thread)

    # -------------------------------------------------------------------------------------------
    parse_getRoute = ['parse-getRoute' + str(i) for i in range(16)]
    # parse_getRoute = ['parse-getRoute1', 'parse-getRoute2', 'parse-getRoute3', 'parse-getRoute4']
    parse_getRoute_Threads = []
    for threadName in parse_getRoute:
        thread = parseThread_getRoute(threadName, dataQueue, result, lock)
        thread.start()
        parse_getRoute_Threads.append(thread)

    """
        while.........
        for.........
            .join()
        以上结构在下面一共设置四个，起到阻塞作用
        主线程队空才是真正的队空情况，防止子线程在暂时队空的状态下退出
    """
    #-----------------------------------------------------------------------------------------------
    while not naviQueue.empty():
        pass

    global navi_EXIT
    navi_EXIT = True
    print('\rnaviQueue empty!',end='')

    for thread in craw_getLine_Threads:
        thread.join()
    #------------------------------------

    while not lineQueue.empty():
        pass

    global line_EXIT
    line_EXIT = True
    print('\rlineQueue empty!',end='')

    for thread in parse_getLine_Threads:
        thread.join()
    #------------------------------------

    while not routeQueue.empty():
        pass

    global route_EXIT
    route_EXIT = True
    print('\rrouteQueue empty!',end='')

    for thread in craw_getRoute_Threads:
        thread.join()
    #-----------------------------------

    while not dataQueue.empty():
        pass

    global data_EXIT
    data_EXIT = True
    print('\rdataQueue empty!',end='')

    for thread in parse_getRoute_Threads:
        thread.join()
    #-----------------------------------


    # 将bus_data 存入一个result列表，构造<"result":result>键值对并存入一个新字典
    # 将字典转成json格式并存入json文件
    shenzhen_busLine = {
        'json_name': '深圳公交线路汇总',
        'updatetime': localtime,
        'results': result
    }
    file = open('exe_file/13/bus_line.json', 'w', encoding='utf-8')

    """
        json.dump()
        把字典转成json串，并自动写入文件中
        dump参数是（字典，文件句柄，indent）。indent用于缩进美化json串的
        ensure_ascii=False用于写文件时有unicode时用，正常显示出中文来
    """
    json.dump(shenzhen_busLine, file, indent=4, ensure_ascii=False)
    file.close()

if __name__ == '__main__':
    # 比单线程的程序快5倍左右
    start = timeit.default_timer()
    main()
    print('\ntime:' + str(timeit.default_timer() - start))
