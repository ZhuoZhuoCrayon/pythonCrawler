import urllib.parse
import urllib.request
import re
import csv
import time
import json
import gzip
from io import StringIO
from bs4 import BeautifulSoup

class crawler:
    date = '20190320'

    # 城市编码
    cityIds = {
        '北京': '530',
        '上海': '538',
        '广州': '763',
        '深圳': '765',
        '杭州': '653',
        '天津': '531',
        '武汉': '736',
        '重庆': '551',
        '苏州': '639',
        '南京': '635',
        '长沙': '749',
    }
    UA = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
    ]
    # 随机构造头部信息
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Host': 'fe-api.zhaopin.com',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q =0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive'
    }

    zhilian_url = 'https://fe-api.zhaopin.com/c/i/sou?'
    start_page = 1
    end_page = 100
    pos_infor = {
        'local':'NULL',
        'name' :'NULL',
        'size':'NULL',
        'type' :'NULL',
        'position' :'NULL',
        'education':'NULL',
        'experience' :'NULL',
        'need' :'NULL',
        'salary' :'NULL',
        'welfare' :'NULL',
        'num' :'NULL',
        'workplace' :'NULL',
        'companyPage' :'NULL',
    }

    def __init__(self,city,keyword):
        self.kw = keyword
        self.cityId = self.cityIds[city]
        csv_url = 'csvfile//智联招聘-'+city+'-'+keyword+'-'+self.date+'.csv'
        self.fp = open(csv_url,'wt',newline='',encoding='utf-8-sig')
        self.writer = csv.writer(self.fp)
        self.writer.writerow(('地区', '企业名称', '企业规模', '企业类别', '招聘岗位', '学历', '工作经验', '工作职责/要求', '薪酬', '福利', '招聘人数', '工作地点', '公司主页'))

    def textDecoration(self,text):
        delspace = re.compile(r'\s+')
        text = delspace.sub('',text)
        set_newline = re.compile(r'[；|：|。|！]')
        text = set_newline.sub('\n',text)
        text = text.replace("展开",'').strip()
        return text

    def getPosition(self,url):
        request = urllib.request.Request(url=url,headers=self.headers)
        content = urllib.request.urlopen(request)
        if content.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(content.read())
            f = gzip.GzipFile(fileobj=buf)
            content = f.read()
        else:
            content = content.read()
        soup = BeautifulSoup(content,'lxml')
        main = soup.find('div',class_ = 'main')


        lis = main.find('div',class_ = 'main1 cl main1-stat').find_all('li')

        self.pos_infor['salary'] = lis[0].strong.text;
        self.pos_infor['position'] = lis[0].h1.text;

        self.pos_infor['name'] = lis[1].find('div',class_ = 'company l').a.text;
        _companyPage = lis[1].find('div',class_ = 'company l').a.attrs['href']
        spans = lis[1].find('div',class_ = 'info-three l').find_all('span')

        self.pos_infor['local'] = spans[0].a.text
        self.pos_infor['experience'] = spans[1].text
        self.pos_infor['education'] = spans[2].text
        self.pos_infor['num'] = spans[3].text[1:-1]

        # 福利信息异步加载，改为在json中提取
        """
        # pos_info_in = main.find('div',class_ = 'l pos-info-in')
        # print(pos_info_in)
        welfareSpans = main.find('div',class_ = 'l pos-info-in').find_all('div',class_ = 'pos-info-tit')
        print(welfareSpans)
        # self.welfare = ''
        for span in welfareSpans:
            print(span.text)
            # self.welfare += str(span.text())+'\n'
        """

        companyAttrs = main.find('ul',class_ = 'promulgator-ul cl')
        lis1 = companyAttrs.find_all('li')

        self.pos_infor['type'] = lis1[1].strong.text
        self.pos_infor['size'] = lis1[2].strong.text
        self.pos_infor['companyPage'] = lis1[3].strong.a['href']
        if self.pos_infor['companyPage'] == '' or self.pos_infor['companyPage'] =='NULL':
            self.pos_infor['companyPage'] = _companyPage

        self.pos_infor['workplace'] = lis1[4].strong.text
        self.pos_infor['need'] = self.textDecoration(main.find('div',class_ = 'responsibility pos-common').get_text())

        self.writer.writerow((self.pos_infor['local'],self.pos_infor['name'],self.pos_infor['size'],self.pos_infor['type'],self.pos_infor['position'] ,
                              self.pos_infor['education'],self.pos_infor['experience'],self.pos_infor['need'] ,self.pos_infor['salary'],
                              self.pos_infor['welfare'],self.pos_infor['num'],self.pos_infor['workplace'],self.pos_infor['companyPage']))
        """
        print(self.pos_infor['local'],self.pos_infor['name'],self.pos_infor['size'],self.pos_infor['type'],self.pos_infor['position'] ,
                              self.pos_infor['education'],self.pos_infor['experience'],self.pos_infor['need'] ,self.pos_infor['salary'],
                              self.pos_infor['welfare'],self.pos_infor['num'],self.pos_infor['workplace'],self.pos_infor['companyPage'])
        """

    def handle_request(self,page):
        data = {
            'start':90*(page-1),
            'pageSize':'90',
            'cityId':self.cityId,
            'workExperience':'-1',
            'education':'-1',
            'companyType':'-1',
            'employmentType':'-1',
            'jobWelfareTag':'-1',
            'kw': self.kw,
            'kt':'3',
            '_v':'0.70987222',
            'x-zp-page-request-id':'5c93296b093c49febba0d63d812d38d6-1553071553649-676137',
        }

        url = self.zhilian_url + urllib.parse.urlencode(data)
        print(url)
        request = urllib.request.Request(url = url, headers = self.headers)
        return request

        # requests.get(url, headers=headers)

    def parse_content(self, content):
        selector = json.loads(content)
        # print(selector)
        data = selector['data']['results']

        if len(data) == 0:
            return 'crawler all'

        for position in data:
            # print(position['positionURL'])
            self.pos_infor['welfare'] =''
            for _welfare in position['welfare']:
                self.pos_infor['welfare'] += _welfare + '\n'
            try:
                self.getPosition(position['positionURL'])
            except:
                pass
            time.sleep(0.1)


        return 'next page'

    def run(self):
        for page in range(self.start_page,self.end_page+1):

            request = self.handle_request(page)
            content = urllib.request.urlopen(request)

            """
            html = content.read()
            print(html)
            buff = BytesIO(html)
            f = gzip.GzipFile(fileobj=buff)
            content = f.read().decode()
            print(content)
            """
            if content.info().get('Content-Encoding')=='gzip':
                buf = StringIO(content.read())
                f = gzip.GzipFile(fileobj=buf)
                content = f.read()
            else:
                content = content.read()

            status = self.parse_content(content)
            if status == 'crawler all':
                print('crawler all')
                break
            else:
                print('crawler end in Page.'+str(page))
            time.sleep(0.5)

import threading
class crawlerThread(threading.Thread):

    def __init__(self,name,city,keyword):
        threading.Thread.__init__(self)
        self.name = name
        self.city = city
        self.keyword = keyword
    def run(self):
        print(self.name)
        test = crawler(self.city,self.keyword)
        test.run()
        print(self.name+"-----------------get all now!")



if __name__ == '__main__':
    cities = [
        '北京',
        '上海',
        '广州',
        '深圳',
        '杭州',
        '天津',
        '武汉',
        '重庆',
        '苏州',
        '南京',
        '长沙',]
    positions_IT = ['Java开发',
                 'UI设计师',
                 'Web前端',
                 'PHP',
                 'Python',
                 'Android',
                 '深度学习',
                 '算法工程师',
                 'hadoop',
                 'Node.js',
                 '数据开发',
                 '数据分析师',
                 '数据架构',
                 '人工智能'
                 '区块链'
                ]
    positions_Finance = [
        '投资经理',
        '风控',
        '催收',
        '银行柜员',
        '银行销售',
        '信审',
        '信用卡',
        '贷款',
        '金融产品',
        '汽车金融',
        '金融研究',
        '证券交易员',
        '投资经理',
        '期货',
        '操盘手',
        '基金',
        '股票',
        '投资顾问',
        '信托',
        '典当',
        '担保',
        '信贷',
        '权证',
        '保险',
        '理赔',
        '精算师',
        '理财',
        '顾问',
        '查勘定损',
        '车险'
    ]


    for city in cities:
        threads = []
        for position in positions_Finance:
            thread = crawlerThread(city+'-'+position,city,position)
            # thread.start()
            # thread.join()
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

