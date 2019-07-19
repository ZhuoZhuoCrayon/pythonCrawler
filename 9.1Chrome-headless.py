"""
PhantomJS 无界面浏览器
selenium+phantomjs 爬虫解决方案
下拉滚动条到底部
    豆瓣电影下拉
图片加载
    图片懒加载问题
        在下拉到底部后，对比获取的page1 和 page2 
        可以发现 src2全部变为src1
    
"""
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
import time
"""
使用pip show selenium显示默认安装的是3.1.3版本
目前使用新版selenium调用PhantomJS是会报这样的错: UserWarning: Selenium support for PhantomJS has been deprecated, 
please use headless versions of Chrome or Firefox instead warnings.warn('Selenium support for PhantomJS has been deprecated, please use headless
如果还想继续用PhantomJS的话只能使用旧版的selenium，卸载之后重新pip install selenium==2.48.0安装成功。
但其实更好的选择，我们可以使用firefox或chrome的headlesss模式,无需重装selenium
只需要添加以下代码：
"""
path = r'E:\Program Files\chrome-driver\chromedriver.exe'

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')#上面三行代码就是为了将Chrome不弹出界面，实现无界面爬取
browser = webdriver.Chrome(path,options=chrome_options)

"""
url = 'http://www.baidu.com/'
browser.get(url)
time.sleep(2)
browser.save_screenshot(r'exe_file/baidu.png')

my_input = browser.find_element_by_id('kw')
my_input.send_keys('美女')
time.sleep(2)
browser.save_screenshot('exe_file/meinv.png')

button = browser.find_elements_by_class_name('s_btn')[0]
button.click()
time.sleep(2)
browser.save_screenshot('exe_file/show.png')
time.sleep(2)
browser.quit()
"""

"""
url = 'https://movie.douban.com/typerank?type_name=%E7%88%B1%E6%83%85%E7%89%87&type=13&interval_id=100:90&action='

browser.get(url)
time.sleep(3)
browser.save_screenshot('exe_file/douban.png')
# 模拟滚动条滚动到底部
# 不同，教程是用body，改用documentElement
js = 'document.documentElement.scrollTop=10000'
browser.execute_script(js)
time.sleep(3)
browser.save_screenshot('exe_file/douban_d.png')

# 获取网页代码
html = browser.page_source

# 保存在文件中
with open(r'exe_file/douban.html','w',encoding='utf-8') as f:
    f.write(html)
'''
豆瓣的数据是js动态加载的
两个方法可以获取数据：
    1 直接获取请求接口 -推荐
    2 利用浏览器驱动模拟真正浏览器获取数据，不过这个比较慢
''''
browser.quit()

"""

url = 'http://sc.chinaz.com/tupian/'
browser.get(url)
time.sleep(5)
with open(r'exe_file/szchina_page_1.html','w',encoding='utf-8') as fp:
    fp.write(browser.page_source)

# 下拉到底部后再获取图片
js = 'document.documentElement.scrollTop=10000'
browser.execute_script(js)
time.sleep(5)

with open(r'exe_file/szchina_page_2.html','w',encoding='utf-8') as fp:
    fp.write(browser.page_source)
browser.quit()