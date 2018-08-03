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
        self.price = -1
        return

class CheckStopOrders(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.flag = True
    def run(self):
        while(self.flag):
            current_price = thread_1.price
            if (not stop_orders and not stop_buy_ORDERS) or current_price < 0:
                print("done")
                self.flag = False
            else:
                if stop_orders:
                    price = current_price
                    if price <= stop_orders[0].price:
                        print("selling ", stop_orders[0].amount, " bitcoin for", price)
                        #ASSUMPTION: the stop order is smaller than current offer
                        stop_orders.pop(0)
                if stop_buy_ORDERS:
                    price = current_price
                    if price >= stop_buy_ORDERS[0].price:
                        print("buying ", stop_buy_ORDERS[0].amount/price, " bitcoin for", price)
                        stop_buy_ORDERS.pop(0)
        return
class StopOrder:
    def __init__(self, price, amount):
        self.price = price
        self.amount = amount


stop_sell_1 = StopOrder(95, 3)
stop_sell_2 = StopOrder(93, 1)
stop_sell_3 = StopOrder(94, 2)

stop_buy_1 = StopOrder(104, 200)
stop_buy_2 = StopOrder(106, 240)
stop_buy_3 = StopOrder(102, 120)

stop_orders = [stop_sell_1, stop_sell_2, stop_sell_3]
stop_buy_ORDERS = [stop_buy_1, stop_buy_2, stop_buy_3]

stop_orders.sort(key=lambda x: x.price, reverse=True)
stop_buy_ORDERS.sort(key=lambda x: x.price, reverse=False)

thread_1 = GenerateRandomPrice(100, 100)
thread_2 = CheckStopOrders()

thread_2.start()
thread_1.start()
