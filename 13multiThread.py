"""
多线程
    面向过程
        t = threading.Thread(target=xxx(函数),name=xxx,args=(xx,xx))
        target :线程启动之后要执行的函数
        name:线程的名字
        获取线程名字：threading.current_thread().name
        args:主线程向子线程传递参数
        t.start():启动线程
        t.join():让主线程等待子线程结束
    面向对象
        定义一个类，继承自threading.Thread，重写一个方法run()，
        需要线程名字、传递参数，重写构造方法，在重写构造方法的时候，主动调用父类的构造方法
    线程同步问题
        线程之间共享全局变量，很容易发生数据紊乱现象
        使用线程锁解决
        抢锁，谁抢到，谁先上锁，谁就先使用
        创建锁
            suo = threading.Lock()
        上锁
            suo = acquire()
        释放锁
            suo.release()
        
        队列(queue)
            下载线程
            解析线程，通过队列进行交互
            q = Queue(size)
            q.put('xxx')-如果队列满，程序卡在这里等待
            q.put(xxx,False)-如果队列满，程序直接报错
            q.put(xxx,True,3)-如果队列满，等待三秒再报错
            
            获取数据
            q.get()
            q.get(False)    队空取元素直接报错
            q.get(True, 3) 队列空，程序等待3s报错
            
            q.empty()   判断队列是否满
            q.full()    判断队列是否已满
            q.qsize()   获取队列长度
"""
import threading
import time
# 一个主线程，一个唱歌，一个跳舞线程

# TypeError: sing() takes 0 positional arguments but 1 was given
# 需要接收参数a
def sing(a):
    print(threading.current_thread().name, a)
    for x in range(1, 6):
        print('I am sing')
        time.sleep(1)
def dance(a):
    print(threading.current_thread().name, a)
    for x in range(1, 6):
        print('I am dancing')
        time.sleep(1)
def main():
    a = 'superman'
    # 创建唱歌线程
    tsing = threading.Thread(target=sing, name="sing", args=(a,))
    # 创建跳舞线程
    tdance = threading.Thread(target=dance, name="dance", args=(a,))
    # 启动线程
    tsing.start()
    tdance.start()
    # 让主线程等待子线程结束之后在结束
    tsing.join()
    tsing.join()
    """
        先让子线程停
        再让主线程停止
    """
    print("I am Main")

if __name__ == '__main__':
    main()