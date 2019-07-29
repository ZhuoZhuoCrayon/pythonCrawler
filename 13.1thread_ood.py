import threading
import time
# 写一个类，继承自threading.Thread
class Singthread(threading.Thread):
    def __init__(self, name, a):
        super().__init__()
        self.name = name
        self.a = a
    def run(self):
        for x in range(1, 6):
            print('I am sing')
            time.sleep(1)

class Dancethread(threading.Thread):
    def __init__(self, name, a):
        super().__init__()
        self.name = name
        self.a = a
    def run(self):
        for x in range(1, 6):
            print('I am dancing')
            time.sleep(1)

def main():
    # create thread
    tsing = Singthread('sing', 'cai')
    tdance = Dancethread('dance', 'crayon')

    # start thread
    tsing.start()
    tdance.start()


    # waiting thread end
    tsing.join()
    tdance.join()


    print('I am Main')


if __name__ == '__main__':
    main()
