x`#!/usr/bin/python

from __future__ import print_function

import sys
import socket
import json
import time
import numpy as np
from random import randint as random


# ~~~~~============== CONFIGURATION  ==============~~~~~
team_name="FLASHBOYS"
test_mode = False

test_exchange_index=0
prod_exchange_hostname="production"

port=25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname
# ~~~~~============== NETWORKING CODE ==============~~~~~
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((exchange_hostname, port))
    return s.makefile('rw', 1)

def write_to_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read_from_exchange(exchange):
    return json.loads(exchange.readline())

# ~~~~~============== MAIN LOOP ==============~~~~~
exchange = connect()

def main():
    write_to_exchange(exchange,{"type": "hello", "team": "FLASHBOYS"})
    
    com_prices = np.empty(5)
   
    def buy(name, price, size):
        write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": name, "dir": "BUY", "price": price, "size": size})

    def sell(name, price, size):
        write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": name, "dir": "SELL", "price": price, "size": size})

    buy_switch = {0 : buy('XLF', least_price - 1, random(1,10)) ,
              1 : buy('GS', least_price - 1, random(1,10) )
              2 : buy('MS', least_price - 1, random(1,10) )
              3 : buy('WFC', least_price - 1, random(1,10) 
              4 : buy('BOND', least_price - 1, random(1,10) )) }
    
    def buy_switcher(i):
        buy_switch[i]

    sell_switch = {0 : buy('XLF', most_price + 1, random(1,10)) ,
              1 : buy('GS', most_price + 1, random(1,10) )
              2 : buy('MS', most_price + 1, random(1,10) )
              3 : buy('WFC', most_price + 1, random(1,10) 
              4 : buy('BOND', most_price + 1, random(1,10) )) }
    
    def sell_switcher(i):
        sell_switch[i]



    while True:
        dic = read_from_exchange(exchange)

        
        if dic['type'] == 'trade' :
            if dic['symbol'] == 'XLF':
                com_prices[0] = dic['price']
            elif dic['symbol'] == 'GS'  :
                com_prices[1] = dic['price']
            elif dic['symbol'] == 'MS'  :
                com_prices[2] = dic['price']
            elif dic['symbol'] == 'WFC'  :
                com_prices[3] = dic['price']
            elif dic['symbol'] == 'BOND'  :
                com_prices[4] = dic['price']

                    

        

       least_price = np.amin(com_prices)
       least_index_in_arr = ((np.where(com_prices == least_price))[0])[0]
       most_price = np.amax(com_prices)
       most_index_in_arr = ((np.where(com_prices == least_price))[0])[0]

       if com_prices.size == 5:
           sell_switcher(most_index_in_arr)
           buy_switcher(least_index_in_arr)

if __name__ == "__main__":
    main()
