import pytesseract
from PIL import Image
from PIL import ImageEnhance
"""
tesseract 安装及使用
    OCR，即Optical Character Recognition，光学字符识别，是指通过扫描字符，然后通过其形状将其翻译成电子文本的过程。
    对于图形验证码来说，它们都是一些不规则的字符，这些字符确实是由字符稍加扭曲变换得到的内容。
    参考：
        Windows安装Tesseract-OCR 4.00并配置环境变量：https://segmentfault.com/a/1190000014086067
        图像文字识别（三）：Tesseract4.0训练字库，提高正确识别率：https://blog.csdn.net/a745233700/article/details/80175883
PIL可以做很多和图像处理相关的事情:
    图像归档(Image Archives)：
        PIL非常适合于图像归档以及图像的批处理任务。你可以使用PIL创建缩略图，转换图像格式，打印图像等等。
    图像展示(Image Display)：
        PIL较新的版本支持包括Tk PhotoImage，BitmapImage还有Windows DIB等接口。PIL支持众多的GUI框架接口，可以用于图像展示。
    图像处理(Image Processing)：
        PIL包括了基础的图像处理函数，包括对点的处理，使用众多的卷积核(convolution kernels)做过滤(filter),还有颜色空间的转换。
        PIL库同样支持图像的大小转换，图像旋转，以及任意的仿射变换。PIL还有一些直方图的方法，允许你展示图像的一些统计特性。
        这个可以用来实现图像的自动对比度增强，还有全局的统计分析等。
    具体参考：
        PIL介绍：https://www.cnblogs.com/lyrichu/p/9124504.html
        Python图像处理库PIL的ImageEnhance模块介绍：https://blog.csdn.net/icamera0/article/details/50753705
        
    ***python+tesseract 训练和破解验证码：https://zhuanlan.zhihu.com/p/40178190
    ***介绍了命令行的操作形式：超级详细的Tesseract-OCR样本训练方法https://blog.csdn.net/sylsjane/article/details/83751297
    ***tesseract v4.0.0 帮助文档解读：https://blog.csdn.net/qq_32674197/article/details/80744783
    ****tesseract_ocr训练字库、合并字库：https://www.imooc.com/article/32331
"""
img = Image.open('exe_file/11/code1.png')
print(img)

img= img.convert('RGB')
# 颜色调到最暗
enhancer = ImageEnhance.Color(img)
enhancer = enhancer.enhance(0)
# 增加亮度
enhancer = ImageEnhance.Brightness(enhancer)
enhancer = enhancer.enhance(4)
# 增加对比度
enhancer = ImageEnhance.Contrast(enhancer)
enhancer = enhancer.enhance(15)
# 增加图片锐度
enhancer = ImageEnhance.Sharpness(enhancer)
img = enhancer.enhance(25)
# img.show()

# 转成灰度图片
img = img.convert('L')
# img.show()
#二值化处理
threshold = 140
table=[]
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
out = img.point(table,'1')
out.show()
# img = img.convert('RGB')
# out.save('exe_file/11/gushiwen_code/35.png','png')

print(pytesseract.image_to_string(out,lang='gu',config='--psm 7'))