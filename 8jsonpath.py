"""
jsonpath--用来解析json数据
python处理json用到的函数
    import json
    json.dumps()--将字典获列表转化为json的字符串
    json.loads()--将json转化为python对象
    json.dump()---将字典/列表转化为json格式字符串并写入文件中
    json.load()---从文件中读取json格式字符串，转化为python对象
前端处理
    将json格式字符串转化为js对象
    JSON.parse('json格式字符串')
    eval('(' + json格式字符串 + ')')
安装:
    pip install jsonpath
    https://blog.csdn.net/luxideyao/article/details/77802389
    
与xpath的区别
    /	$	表示根元素
    .	@	 当前元素
    /	. or []	子元素
    ..	n/a	父元素
    //	..	递归下降，JSONPath是从E4X借鉴的。
    *	*	通配符，表示所有的元素
    xpath下标从1开始，jsonpath从0开始
    ---------------------------------------
    @	n/a	 属性访问字符
    []	[]	子元素操作符
    |	[,]	连接操作符在XPath 结果合并其它结点集合。JSONP允许name或者数组索引。
    n/a	[start:end:step]	数组分割操作从ES4借鉴。
    []	?()	应用过滤表示式
    n/a	()	脚本表达式，使用在脚本引擎下面。
    ()	n/a	Xpath分组
"""


import json

lt = [
    {'name': '王宝强', 'age': 30},
    {'name': 'pgone', 'age': 30},
    {'name': '马蓉', 'age': 30},
    {'name': '宋吉', 'age': 30},
    {'name': '李小璐', 'age': 30},
]
# 将字典获列表转化为json的字符串
string = json.dumps(lt)
print(string)
# out：[{"name": "\u738b\u5b9d\u5f3a", "age": 30},
# {"name": "pgone", "age": 30}, {"name": "\u9a6c\u84c9", "age": 30},
# {"name": "\u5b8b\u5409", "age": 30}, {"name": "\u674e\u5c0f\u7490", "age": 30}]

import jsonpath

# 将json格式文件转成python对象
obj = json.load(open('exe_file/book.json','r',encoding='utf-8'))
print(obj)

# 书单所有书的作者
ret = jsonpath.jsonpath(obj,'$.store.book[*].author')
print(ret)
# solve2
ret1 = jsonpath.jsonpath(obj,'$..author')
print(ret1)

# 查找store下面所有的节点
ret2 = jsonpath.jsonpath(obj,'$.store.*')
print(ret2)

# 查找store下面所有的price
ret3 = jsonpath.jsonpath(obj,'$.store..price')
print(ret3)

# 查找第三个book
ret4 = jsonpath.jsonpath(obj,'$..book[2]')
print(ret4)

# 查找最后一个book
ret5 = jsonpath.jsonpath(obj,'$..book[(@.length-1)]')
print(ret5)

# 查找前两本书
ret6 = jsonpath.jsonpath(obj,'$..book[0,1]')
# ret6 = jsonpath.jsonpath(obj,'$..book[:2]')
# ret6 = jsonpath.jsonpath(obj,'$..book')[:2]
print(ret6)

# 查找含有isbn键的book
ret7 = jsonpath.jsonpath(obj,'$..book[?(@.isbn)]')
print(ret7)

#查找所有price键对应的值小于10的所有book
ret8 = jsonpath.jsonpath(obj,'$..book[?(@.price<10)]')
print(ret8)



import urllib.request
import urllib.response
import jsonpath
import csv
"""
https://fe-api.zhaopin.com/c/i/sou?start=180&pageSize=90&
cityId=765&workExperience=-1&education=-1&companyType=-1&
employmentType=-1&jobWelfareTag=-1&kw=python&kt=3
"""

def main():

    # 创建csv文件
    csv_url = 'exe_file/python_postion.csv'
    fp = open(csv_url, 'wt', newline='', encoding='utf-8-sig')
    writer = csv.writer(fp)
    writer.writerow(('岗位', '企业名称', '企业规模', '企业类别', '企业主页', '工作地点', '薪酬', '学历要求', '工作经验', '岗位招聘主页'))

    # 智联招聘网址
    # kw表示职位关键字，cityId是城市代号
    # start和pageSize控制翻页
    url = 'https://fe-api.zhaopin.com/c/i/sou?start=90&pageSize=90&' \
          'cityId=765&workExperience=-1&education=-1&companyType=-1&' \
          'employmentType=-1&jobWelfareTag=-1&kw=python&kt=3'
    # 请求头
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    # 请求
    request = urllib.request.Request(url=url, headers=headers)
    json_text = urllib.request.urlopen(request).read().decode()

    # 将请求到的json转为python对象
    json_obj = json.loads(json_text)
    # print(json_text)

    # 筛选出招聘职位信息集合
    pos_infos = jsonpath.jsonpath(json_obj,'$.data.results[*]')

    for info in pos_infos:
        # 基于jsonpath的信息查找
        job_name = jsonpath.jsonpath(info,'$.jobName')[0]
        company_name = jsonpath.jsonpath(info,'$.company.name')[0]
        company_size = jsonpath.jsonpath(info,'$.company.size.name')[0]
        company_type = jsonpath.jsonpath(info,'$.company.type.name')[0]
        company_url = jsonpath.jsonpath(info,'$.company.url')[0]
        city = jsonpath.jsonpath(info,'$..city.display')[0]
        salary = jsonpath.jsonpath(info,'$.salary')[0]
        edu_level = jsonpath.jsonpath(info,'$.eduLevel.name')[0]
        working_exp = jsonpath.jsonpath(info,'$.workingExp.name')[0]
        position_url = jsonpath.jsonpath(info,'$.positionURL')[0]

        writer.writerow((job_name, company_name, company_size, company_type,
                         company_url, city, salary, edu_level, working_exp, position_url))




if __name__ == '__main__':
    main()
