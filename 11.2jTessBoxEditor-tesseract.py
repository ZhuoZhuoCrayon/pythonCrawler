"""
    验证码训练脚本
    Author:caixiaoxin
    date：2019/7/23
"""
from PIL import ImageEnhance
from PIL import Image
import pytesseract
from bs4 import BeautifulSoup
import os
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.142 Safari/537.36',
}
# 根据训练字库识别验证码
def get_varifyCode()->str:
    img = Image.open('exe_file/11/code.png')
    # print(img)
    img = img.convert('RGB')
    # 颜色调到最暗
    enhancer = ImageEnhance.Color(img)
    enhancer = enhancer.enhance(0)
    # 增加亮度
    enhancer = ImageEnhance.Brightness(enhancer)
    enhancer = enhancer.enhance(2)
    # 增加对比度
    enhancer = ImageEnhance.Contrast(enhancer)
    enhancer = enhancer.enhance(8)
    # 增加图片锐度
    enhancer = ImageEnhance.Sharpness(enhancer)
    img = enhancer.enhance(20)
    # img.show()

    # 转成灰度图片
    img = img.convert('L')
    # img.show()
    # 二值化处理
    threshold = 140
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    out = img.point(table, '1')
    # out.show()
    # img = img.convert('RGB')
    out.save('exe_file/11/code.png','png')
    code = pytesseract.image_to_string(out,lang='gu',config='--psm 7')
    code = code.replace(' ','')     # 除去空格
    return code

# 下载验证码
def download_code(session):
    url = 'https://so.gushiwen.org/user/login.aspx?' \
          'from=http://so.gushiwen.org/user/collect.aspx'
    request = session.get(url=url, headers=headers)
    soup = BeautifulSoup(request.text,'lxml')

    '''
        问题：url相同,为什么每次获取的验证码不同
        同个url下，通过cookie随机生成验证码
        所以需要在获取验证码，登陆这个过程需要建立会话
    '''
    img_src = 'https://so.gushiwen.org' + \
              soup.find('img',id='imgCode')['src']
    # print(img_src)
    img = session.get(url=img_src,headers=headers)
    with open('exe_file/11/code.png','wb') as fp:
        fp.write(img.content)

    # 查找表单需要的两个参数
    __VIEWSTATE = soup.find('input', id='__VIEWSTATE')['value']
    __VIEWSTATEGENERATOR = soup.find('input', id='__VIEWSTATEGENERATOR')['value']

    # 识别验证码
    code = get_varifyCode()

    return __VIEWSTATE, __VIEWSTATEGENERATOR, code

# post登陆
def login(__VIEWSTATE, __VIEWSTATEGENERATOR, code, session)->bool:
    post_url = 'https://so.gushiwen.org/user/login.aspx?' \
               'from=http%3a%2f%2fso.gushiwen.org%2fuser%2fcollect.aspx'
    data = {
        '__VIEWSTATE' : __VIEWSTATE,
        '__VIEWSTATEGENERATOR' : __VIEWSTATEGENERATOR,
        'from' : 'http://so.gushiwen.org/user/collect.aspx',
        'email' : '15625266605',
        'pwd' : '123456',
        'code' : code,
        'denglu': '登录',
    }
    # 登陆
    request = session.post(url=post_url,headers=headers,data=data)
    # print(len(request.text))
    if len(request.text)==35822:
        return False
    else:
        return True
# 实现模拟登陆，如果验证码识别错误，将有误验证码存入
def test_login()->bool:
    # 创建会话
    session = requests.Session()
    # 下载验证码到本地
    __VIEWSTATE, __VIEWSTATEGENERATOR, code = download_code(session)

    status = login(__VIEWSTATE, __VIEWSTATEGENERATOR, code ,session)

    if status is not True:
        try:
            img = Image.open('exe_file/11/code.png')
            img.save('exe_file/11/verify_code/{}.png'.format(code), 'png')
        except OSError:
            pass
        return False
    else:   return True

# 批量处理验证码图片
def deal_img():
    root = 'exe_file/11/gushiwen_code/'
    ind = 0
    # 从100张图片中提取出字符样本
    for image in os.listdir(root):
        img = Image.open(root + image)
        img = img.convert('RGB')
        # 颜色调到最暗
        enhancer = ImageEnhance.Color(img)
        enhancer = enhancer.enhance(0)
        # 增加亮度
        enhancer = ImageEnhance.Brightness(enhancer)
        enhancer = enhancer.enhance(2)
        # 增加对比度
        enhancer = ImageEnhance.Contrast(enhancer)
        enhancer = enhancer.enhance(8)
        # 增加图片锐度
        enhancer = ImageEnhance.Sharpness(enhancer)
        img = enhancer.enhance(20)
        # img.show()

        # 转成灰度图片
        img = img.convert('L')
        # img.show()
        # 二值化处理
        threshold = 140
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        out = img.point(table, '1')
        out.save(root+'{}.png'.format(ind),'png')
        ind = ind + 1

if __name__ == '__main__':
    # 测试识别准确率
    test_num = 200
    correct_num = 0
    for i in range(test_num):
        if test_login() is True:
            correct_num += 1
    print("准确率{}%".format(correct_num*100/test_num))
    # deal_img()



