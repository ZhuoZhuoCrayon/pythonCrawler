from queue import Queue

# create queue
q = Queue(5)
# store data
q.put('c')
q.put('c++')
q.put('python')
q.put('java')
q.put('matlab')
# q.put('markdown', True, 3)
# q.put('markdown', False)
# q.put('markdown')

# get data
# 先进先出
print(q.get())
print(q.get())
print(q.get())
print(q.get())
print(q.get())

print(q.get())  # 队空阻塞
