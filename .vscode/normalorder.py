#!/usr/bin/env python
"""self explaining"""

import time
import threading
import random

class Order:
    def __init__(self, price ,amount):
        self.price = price
        self.amount = amount

STOP_SELL_1 = Order(95, 3)
STOP_SELL_2 = Order(93, 1)
STOP_SELL_3 = Order(94, 2)

SELL_1 = Order(104, 1)
SELL_2 = Order(110, 0.5)
SELL_3 = Order(102, 3)
SELL_4 = Order(107, 2)

STOP_BUY_1 = Order(104, 200)
STOP_BUY_2 = Order(106, 240)
STOP_BUY_3 = Order(102, 120)

BUY_1 = Order(95, 300)
BUY_2 = Order(91, 500)
BUY_3 = Order(92, 900)
BUY_4 = Order(90, 1300)

STOP_ORDERS = [STOP_SELL_1, STOP_SELL_2, STOP_SELL_3]
STOP_BUY_ORDERS = [STOP_BUY_1, STOP_BUY_2, STOP_BUY_3]
BUY_ORDERS_QUEUE = [BUY_1, BUY_2, BUY_3, BUY_4]
SELL_ORDERS_QUEUE = [SELL_1, SELL_2, SELL_3, SELL_4]

STOP_ORDERS.sort(key=lambda x: x.price, reverse=True)
STOP_BUY_ORDERS.sort(key=lambda x: x.price, reverse=False)