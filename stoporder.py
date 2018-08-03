import time
import threading
import random

class GenerateRandomPrice(threading.Thread):
    def __init__(self, price, count):
        threading.Thread.__init__(self)
        self.price = price
        self.count = count
    def run(self):
        while self.count > 0:
            self.price += random.randint(0,6)
            self.price -= 3
            print(self.price)
            self.count -= 1
        return

class CheckStopOrders(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.flag = True
    def run(self):
        while(self.flag):
            currentPrice = THREAD1.price
            if not STOP_ORDERS and not STOP_BUY_ORDERS:
                print("habis")
                self.flag = False
            else:
                if STOP_ORDERS:
                    price = currentPrice
                    if price <= STOP_ORDERS[0].price:
                        print("selling ", STOP_ORDERS[0].amount, " bitcoin for", price)
                        #ASSUMPTION: the stop order is smaller than current offer
                        STOP_ORDERS.pop(0)
                if STOP_BUY_ORDERS:
                    price = currentPrice
                    if price >= STOP_BUY_ORDERS[0].price:
                        print("buying ", STOP_BUY_ORDERS[0].amount/price, " bitcoin for", price)
                        STOP_BUY_ORDERS.pop(0)
        return
class StopOrder:
    def __init__(self, price, amount):
        self.price = price
        self.amount = amount


STOP_SELL_1 = StopOrder(95, 3)
STOP_SELL_2 = StopOrder(93, 1)
STOP_SELL_3 = StopOrder(94, 2)

STOP_BUY_1 = StopOrder(104, 200)
STOP_BUY_2 = StopOrder(106, 240)
STOP_BUY_3 = StopOrder(102, 120)

STOP_ORDERS = [STOP_SELL_1, STOP_SELL_2, STOP_SELL_3]
STOP_BUY_ORDERS = [STOP_BUY_1, STOP_BUY_2, STOP_BUY_3]

STOP_ORDERS.sort(key=lambda x: x.price, reverse=True)
STOP_BUY_ORDERS.sort(key=lambda x: x.price, reverse=False)

THREAD1 = GenerateRandomPrice(100, 100)
THREAD2 = CheckStopOrders()

THREAD2.start()
THREAD1.start()
