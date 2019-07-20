"""
    验证码
        登陆古诗文网
        将验证码下载到本地
        在登陆页面中获取表单的两个重要参数
        整个过程在会话状态下进行
"""

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.142 Safari/537.36',
}
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

    return __VIEWSTATE, __VIEWSTATEGENERATOR

def login(__VIEWSTATE, __VIEWSTATEGENERATOR,session):
    post_url = 'https://so.gushiwen.org/user/login.aspx?' \
               'from=http%3a%2f%2fso.gushiwen.org%2fuser%2fcollect.aspx'
    # 提示用户输入验证码
    code = input('input verification code:')
    data = {
        '__VIEWSTATE' : __VIEWSTATE,
        '__VIEWSTATEGENERATOR' : __VIEWSTATEGENERATOR,
        'from' : 'http://so.gushiwen.org/user/collect.aspx',
        'email' : '15625266605',
        'pwd' : '123456',
        'code' : code,
        'denglu': '登录',
    }
    # 登陆并且将页面写入文件
    request = session.post(url=post_url,headers=headers,data=data)
    with open('exe_file/11/gushi.html','w',encoding='utf-8') as file:
        file.write(request.text)
def main():
    # 创建会话
    session = requests.Session()
    # 下载验证码到本地
    __VIEWSTATE, __VIEWSTATEGENERATOR = download_code(session)

    login(__VIEWSTATE, __VIEWSTATEGENERATOR,session)
if __name__ == '__main__':
    main()