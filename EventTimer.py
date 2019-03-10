class TimeEventHandler(threading, Thread):
    def __init__(self, *arg, **kwargs):
        threading.Thread.__init__(self)

def run(self):

import time
period=10
points=1
bonus=1
while True:
    while period >0:
        time.sleep(1)
        #print(period)
        period -=1
        if period == 0:
            points += bonus
            print('Punkte:')
            print(points)
            period=10
    #threading einfügen
