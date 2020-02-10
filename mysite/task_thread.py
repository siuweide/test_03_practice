from time import ctime, sleep
import threading



def move(name):
    print("i was see the movices %s! %s" %(name,ctime()))
    sleep(2)


threads = []
t1 = threading.Thread(target=move, args=('钢铁侠',))
threads.append(t1)
t2 = threading.Thread(target=move, args=('蜘蛛侠',))
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("all over %s" %ctime())