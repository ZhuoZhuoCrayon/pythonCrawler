"""
浏览器自动化测试框架
是一个python的第三方库，对外提供接口可以操作浏览器
让浏览器完成自动化操作
使用selenium
    1 安装 pip install selenium
    2 如何操作谷歌浏览器，首先必须有谷歌浏览器的一个驱动
    3
        驱动与谷歌浏览器的版本映射关系
        https://blog.csdn.net/fox990152806/article/details/91881361
        谷歌驱动下载
        http://npm.taobao.org/mirrors/chromedriver/
    4 代码操作
        find_element_by_id              id
        find_element_by_name            name
        find_element_by_xpath           xpath
        find_element_by_tag_name        标签名
        find_element_by_class_name      class名称
        find_element_by_css_selector    选择器查找
        find_element_by_link_text       根据链接内容
        
        get\set_keys\click
    
"""

# 简单selenium操作
from selenium import webdriver
import  time

# 模拟创建浏览器对象,通过对象操作浏览器
path = r'E:\Program Files\chrome-driver\chromedriver.exe'
browser = webdriver.Chrome(executable_path=path)
# print(browser)

# 打开百度
url = 'http://www.baidu.com/'
browser.get(url)

# 中间有内容请求，发送响应的过程，需要停顿
time.sleep(2)

# 向百度搜索框中填入关键字
my_input = browser.find_element_by_id('kw') # 对应百度搜索框的id
my_input.send_keys('美女')

time.sleep(2)
# 查找搜索按钮s
# ..s：返回一个列表
# bg s_btn 不行
button = browser.find_elements_by_class_name('s_btn')[0]
button.click()  # 点击
# 页面停顿
time.sleep(2)


# 坑：百度已将该图片链接设置为动态，故无法点击
page_url = browser.find_elements_by_class_name('op-img-address-hover')[0]
page_url.click()

time.sleep(5)

# 关闭浏览器
browser.quit()


from selenium import webdriver
import  time

# 模拟创建浏览器对象,通过对象操作浏览器
path = r'E:\Program Files\chrome-driver\chromedriver.exe'
browser = webdriver.Chrome(executable_path=path)
# print(browser)

# 打开百度
url = 'http://www.baidu.com/'
browser.get(url)

browser.find_elements_by_link_text('设置')[0].click()
time.sleep(3)

browser.find_elements_by_link_text(r'搜索设置')[0].click()
time.sleep(2)

m = browser.find_element_by_id('nr')
time.sleep(2)

# 每页搜索50条
m.find_element_by_xpath('//*[@id="nr"]/option[3]').click()
time.sleep(2)

# 确认更改
browser.find_elements_by_class_name("prefpanelgo")[0].click()
time.sleep(2)

# 处理弹窗
browser.switch_to_alert().accept()
time.sleep(2)

# 进行搜索
browser.find_element_by_id('kw').send_keys('美女')
time.sleep(2)

# 确认
browser.find_element_by_id('su').click()
time.sleep(2)

# 进入该搜索项
browser.find_elements_by_link_text('美女_百度图片')[0].click()
time.sleep(3)


# 关闭浏览器
browser.quit()
