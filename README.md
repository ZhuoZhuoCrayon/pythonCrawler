# pythonCrawler
>## Notice
1. exe_file 是本程序爬取的附录，全部测试、实战读写路径全部指向exe\_file
2. 本爬虫笔记基于b站 [Python爬虫从入门到高级实战【92集】千锋Python高级教程](https://www.bilibili.comvideo/av37027372)
3. 在该教程的基础上对教程中的思路进行实践，对教程出现的错误进行修正，并且另外扩展，**并非教程源码照搬**
4. 由于时间有限，笔记与代码都位于.py文件中，以注释及代码形式存在，对学习过程中会出现的bug以及难点进行分析
5. 由于作者能力有限以及爬虫技术迭代速度快，代码可能会存在bug，如有此情况，欢迎联系我更正或者pull request
6. **更新日志的正确打开方式：**
    - 数字代表每一章，每个数字的第一个py文件是基础知识讲解及简单实践
    - x.x形式的py文件一般是实战内容
    - 例如6.基于xpath...是基础知识，那么6.1就是项目实战内容
    - **所有的py文件都会有思路、踩坑以及知识点的介绍**
    - **人性化设置，md文件的更新日志附属笔记的超链接跳转**
7. 如果笔记对您有用，麻烦Star谢谢
- - -
>## Update log
1. __2019/03-2019/03/12__
    - [1.urllib基础](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/1urllib_base.py)
    - [2.利用ajax的特点构建post请求，及对url异常的处理实例：豆瓣，kfc餐厅，百度贴吧的页面爬取](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/2ajax.py)
    - [3.以百度翻译为例介绍fiddler中json包的解析](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/fillder.py)
    - [4.Handler处理器的应用：设置ip及cookieJar，人人网模拟登陆](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/4handler.py)
    - [5.1.利用正则表达式提取糗图网页面信息](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/5.1%E6%AD%A3%E5%88%99%E7%88%AC%E5%8F%96%E7%B3%97.py)
    - [5.2.正则爬取励志网并建立文章集合页面](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/5.2%E6%AD%A3%E5%88%99%E7%88%AC%E5%8F%96%E5%8A%B1%E5%BF%97%E7%BD%91%E5%B9%B6%E5%BB%BA%E7%AB%8B%E6%96%87%E7%AB%A0%E9%9B%86%E5%90%88%E9%A1%B5%E9%9D%A2.py)
2. __2019/04-__
    - 项目实战：[智联招聘爬虫-通用版：目前已爬取2019年第一季度IT领域招聘信息数据集](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/zhilianCrawler.py)
        + urllib, BeautifulSoup, 正则表达式, 多线程爬取, json获取, csv文件读写
3. __2019/07/10__
    - [6.基于xpath的html页面信息提取](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/6xpath.py)
        + 实例：段子网爬取
4. __2019/07/11__
    - [6.1.读取文件中的列表格式](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/6.1read_list.py)
        + 实例：文本文件中对象的读取
    - [7.基于图片懒加载技术的图片下载](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/7pictureLoad.py)
5. __2019/07/15__
    - [8.基于jsonpath的json文件解析方法](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/8jsonpath.py)
        + 实例：智联招聘，填补之前智联爬虫采用正则表达式解析json文件的繁琐方法
        + b站教程以爬取淘宝评论为例，但现淘宝系统过于难爬，**此处留坑**
6. __2019/07/16__
    - 谷歌浏览器驱动，适配谷歌75版本---在exeFile目录下
7. __2019/07/17__
    - [9.基于selenium的浏览器控制访问](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/9selenium.py)
        + 实例：百度关键字搜索
8. __2019/07/19__
    - [9.1.基于Chrome无界面模式浏览，图片懒加载的特点，异步加载的解决方法](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/9.1Chrome-headless.py)
        + 实例1：豆瓣电影下拉滚动条，懒加载变化解析
        + 实例2：百度图片搜索，无界面模式实践
9. __2019/07/20__
    - **告知：**
        + 为方便实例的各种测试文件的查找，在第10章包括以后，每章的测试文件保存在exe\_file/x/下
        + **x为对应章节，例如第10章，则位于exe\_file/10/**
    - [10.Requests库的基本用法](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/10-Requests.py)
        + 实例：百度搜索，必应翻译，登陆人人网为例介绍post、cookie、get的用法
        + 代理使用
    - [10.1.Requests库实战](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/10.1busPath_Crawler.py)
        + 实例：爬取深圳所有公交路线
        + 运用：json文件读写、Requests库及xpath解析
        + 数据集：[深圳公交线路json文件](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/exe_file/10/bus_line.json)
    - [11.验证码登陆方式](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/11verification_code.py)
        + 实例：利用返回验证码到本地的方法登陆古诗文网
        + 运用：Requests库（创建会话用于支持cookie），美味汤(beautifulSoup)
10. __2019/07/21-2019/07/26__
    - [11.1pytesser介绍](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/11.1pytesser.py)
        + 介绍了pytesser库以及PIL库的基本使用
    - [11.2jTessBoxEditor-tesseract字库训练模式](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/11.2jTessBoxEditor-tesseract.py)
        + 验证码测试脚本
    - **[重点：tesseract训练字库详解](https://github.com/ZhuoZhuoCrayon/pythonCrawler/tree/master/tesseract%E8%AE%AD%E7%BB%83%E6%A8%A1%E5%9E%8B)**
        + 通过建立特征字符库，逐层加入识别错误的验证码进行补充训练，可以在三次扩充样本训练后达到90%以上识别率
11.__2019/07/28__
    - [12.视频爬取](https://github.com/ZhuoZhuoCrayon/pythonCrawler/blob/master/12video.py)
        + 基于xpath, json, chromeDrive-headless的视频爬取方案
---
>## Contributing
>如果你对这个项目感兴趣，非常乐意你可以将.py文件的笔记和代码进行格式加工
>>[版权声明]笔记内容是我原创并且开源到github上的，所有内容仅限于学习，不作商用，欢迎star/download/fork，但务必遵守相关开源协议进行使用，原创不易，请勿copy。在实践时遵守爬虫协议，目的只是为了更好的掌握爬虫知识，如果有所影响，请联系我删除，谢谢！

