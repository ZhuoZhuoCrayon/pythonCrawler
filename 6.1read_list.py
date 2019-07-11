
file = open('exe_file/hello.txt','r',encoding='utf8')
string = file.read()
file.close()

lt = eval(string)
print(lt[0]['name'])

# out：
# 宫本武藏
# 小田纯一郎