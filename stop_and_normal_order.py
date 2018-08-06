#!/usr/bin/env python
"""self explaining"""

import time
import threading
import random
import matplotlib.pyplot as plt
import numpy as np

class GeneratePrice(threading.Thread):

    def __init__(self, price, cycle):
        threading.Thread.__init__(self)
        self.cycle = cycle
        self.price = price
        self.direction = 0
        self.flag = True
    def run(self):
        while self.cycle > 0:
            self.price += random.randint(0, 6)
            self.price = self.price - 3 + self.direction
            time.sleep(1/20)
            self.cycle -= 1
            print(self.cycle, " >> ", self.price)
            PRICE_HISTORY.append(self.price)
        self.price = -1
        self.flag = False
        return

class CheckStopOrders(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.flag = True
    def run(self):
        while (STOP_ORDERS or  STOP_BUY_ORDERS) and THREAD_GENERATE_PRICE.price > 0:
            current_price = THREAD_GENERATE_PRICE.price
            if STOP_ORDERS:
                if current_price <= STOP_ORDERS[0].price:
                    SELL_ORDERS_QUEUE.append(STOP_ORDERS[0])
                    SELL_ORDERS_QUEUE.sort(key=lambda x: x.price, reverse=False)
                    STOP_ORDERS.pop(0)
                    print("Stop sell triggered")
            if STOP_BUY_ORDERS:
                if current_price >= STOP_BUY_ORDERS[0].price:
                    BUY_ORDERS_QUEUE.append(STOP_BUY_ORDERS[0])
                    BUY_ORDERS_QUEUE.sort(key=lambda x: x.price, reverse=True)
                    STOP_BUY_ORDERS.pop(0)
                    print("Stop buy triggered")
        self.flag = False
        return

class RunOrders(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.flag = True
    def run(self):
        while THREAD_GENERATE_PRICE.price > 0 and (self.flag or THREAD_CHECK_STOP_ORDERS.flag):
            current_price = THREAD_GENERATE_PRICE.price
            if (not BUY_ORDERS_QUEUE and not SELL_ORDERS_QUEUE) or current_price < 0:
                print("[no more stop order]", current_price)
                self.flag = False
            else:
                if BUY_ORDERS_QUEUE:
                    if current_price <= BUY_ORDERS_QUEUE[0].price:
                        print("[SUCCESS BUY] ", BUY_ORDERS_QUEUE[0].amount/current_price, " bitcoin for ", current_price, " >> ", BUY_ORDERS_QUEUE[0].amount)
                        TRANSACTION_PRICES.append(current_price)
                        TRANSACTION_TIMESTAMP.append(100-THREAD_GENERATE_PRICE.cycle)
                        BUY_ORDERS_QUEUE.pop(0)
                else:
                    THREAD_GENERATE_PRICE.direction += 0.00001
                if SELL_ORDERS_QUEUE:
                    if current_price >= SELL_ORDERS_QUEUE[0].price:
                        print("[SUCCESS SELL] ", SELL_ORDERS_QUEUE[0].amount, " of bitcoin for ", current_price, " >> ", SELL_ORDERS_QUEUE[0].amount*current_price)
                        TRANSACTION_PRICES.append(current_price)
                        TRANSACTION_TIMESTAMP.append(100-THREAD_GENERATE_PRICE.cycle)
                        SELL_ORDERS_QUEUE.pop(0)
                else:
                    THREAD_GENERATE_PRICE.direction -= 0.00001
        print("not running run orders")
        THREAD_GENERATE_PRICE.direction = 0
        self.flag = False
        return

class Order:
    def __init__(self, price, amount):
        self.price = price
        self.amount = amount

STOP_SELL_1 = Order(95, 3)
STOP_SELL_2 = Order(93, 1)
STOP_SELL_3 = Order(94, 2)
STOP_SELL_4 = Order(80, 3)
STOP_SELL_5 = Order(88, 2.3)
STOP_SELL_6 = Order(84, 5)

SELL_1 = Order(104, 1)
SELL_2 = Order(110, 0.5)
SELL_3 = Order(102, 3)
SELL_4 = Order(107, 2)
SELL_5 = Order(120, 2)
SELL_6 = Order(117, 2)

STOP_BUY_1 = Order(104, 200)
STOP_BUY_2 = Order(106, 240)
STOP_BUY_3 = Order(102, 120)
STOP_BUY_4 = Order(110, 200)
STOP_BUY_5 = Order(115, 1000)
STOP_BUY_6 = Order(123, 550)

BUY_1 = Order(95, 300)
BUY_2 = Order(91, 500)
BUY_3 = Order(92, 900)
BUY_4 = Order(90, 1300)
BUY_5 = Order(88, 700)
BUY_6 = Order(86, 250)

STOP_ORDERS = [STOP_SELL_1, STOP_SELL_2, STOP_SELL_3, STOP_SELL_4, STOP_SELL_5, STOP_SELL_6]
STOP_BUY_ORDERS = [STOP_BUY_1, STOP_BUY_2, STOP_BUY_3, STOP_BUY_4, STOP_BUY_5, STOP_BUY_6]
BUY_ORDERS_QUEUE = [BUY_1, BUY_2, BUY_3, BUY_4, BUY_5, BUY_6]
SELL_ORDERS_QUEUE = [SELL_1, SELL_2, SELL_3, SELL_4, SELL_5, SELL_6]

SELL_ORDERS_QUEUE.sort(key=lambda x: x.price, reverse=False)
BUY_ORDERS_QUEUE.sort(key=lambda x: x.price, reverse=True)

STOP_ORDERS.sort(key=lambda x: x.price, reverse=True)
STOP_BUY_ORDERS.sort(key=lambda x: x.price, reverse=False)

print("test >> ", BUY_ORDERS_QUEUE[0].price)
print("test >> ", BUY_ORDERS_QUEUE[1].price)
print("test >> ", BUY_ORDERS_QUEUE[2].price)

TRANSACTION_PRICES = []
PRICE_HISTORY = []
TRANSACTION_TIMESTAMP = []

THREAD_GENERATE_PRICE = GeneratePrice(100, 100)
THREAD_CHECK_STOP_ORDERS = CheckStopOrders()
THREAD_RUN_ORDERS = RunOrders()

THREAD_GENERATE_PRICE.start()
THREAD_CHECK_STOP_ORDERS.start()
THREAD_RUN_ORDERS.start()

THREAD_GENERATE_PRICE.join()
THREAD_CHECK_STOP_ORDERS.join()
THREAD_RUN_ORDERS.join()

y1 = []
for i in range(0, len(TRANSACTION_PRICES)):
    y1.append(TRANSACTION_PRICES[i])

y2 = []
for i in range(0, len(PRICE_HISTORY)):
    y2.append(PRICE_HISTORY[i])
x2 = []
for i in range(0, len(TRANSACTION_TIMESTAMP)):
    x2.append(TRANSACTION_TIMESTAMP[i])

fig, ax = plt.subplots()
ax.plot(x2, y1, 'ro',label='Transaction')
ax.plot(list(range(0,100)),y2,label='Simulated Price movement')

plt.ylabel('Price')
plt.title('Time Series of TX')
legend = ax.legend(loc='best', shadow=True, fontsize='medium')
plt.axis([0, 101, min(PRICE_HISTORY)*0.9, max(PRICE_HISTORY)*1.1])
plt.show()
