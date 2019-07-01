#!/usr/bin/python

# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py; sleep 1; done

from __future__ import print_function

import numpy as np
import sys
import socket
import json
import time
from random import randint as random

# ~~~~~============== CONFIGURATION  ==============~~~~~
# replace REPLACEME with your team name!
team_name="FLASHBOYS"
# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
test_mode = False

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
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

# if ((10*ETF) - (3*BONDS + 2*GS + 3*MS + 2*WCF) >=10):


# def max_demanded_commodity(x, max_demand_sofar):
#     stock_to_sell = ""
#     total_demand = 0
#     if 'book' in x :
#         for each_entry in x['buy']:
#             total_demand = total_demand + each_entry[1]
#             if total_demand > max_demand_sofar:
#                 max_demand_sofar = total_demand      
#                 stock_to_sell = x['symbol']
#     return(stock_to_sell)

# def max_supply_commodity(x, max_supply_sofar):

    # stock_to_buy = ""       
    # total_supply = 0
 
    # if 'book' in x:
    #     for each_entry in x['sell']:
    #         total_supply = total_supply + each_entry[1]
    #         if total_supply > max_supply_sofar:
    #             max_supply_sofar = total_supply      
    #             stock_to_buy = x['symbol']
 
    # return(stock_to_buy)

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







    
    
        
    
    #     if XLF_price :

    #         write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "XLF", "dir": "SELL", "price": random(XLF_price + 1000, XLF_price + 100000), "size": 10})
        
    #     if BOND_price :    
    #         write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "BOND", "dir": "BUY", "price": random(BOND_price - 1000, BOND_price - 100), "size": 3})
        
    #     if MS_price :    
    #         write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "MS", "dir": "BUY", "price": random(MS_price - 1000, MS_price - 100), "size": 3})

    #     if GS_price:    
    #         write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "GS", "dir": "BUY", "price": random(GS_price - 1000, GS_price - 100), "size": 2})
        
    #     if WFC_price:    
    #         write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "WFC", "dir": "BUY", "price": random(WFC_price - 1000, WFC_price - 100), "size": 2})
            
            

        
    #     if XLF_price :
    #         write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "XLF", "dir": "BUY", "price": random(XLF_price - 1000, XLF_price - 100) , "size": 10})
        
    #     if BOND_price:   
    #         write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "BOND", "dir": "SELL", "price": random(BOND_price + 1000, BOND_price + 10000), "size": 3})
        
    #     if MS_price:    
    #         write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "MS", "dir": "SELL", "price": random(MS_price + 100, MS_price + 10000), "size": 3})
        
    #     if GS_price:    
    #         write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "GS", "dir": "SELL", "price": random(GS_price + 100, GS_price + 10000), "size": 2})
        
    #     if WFC_price:    
    #         write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "WFC", "dir": "SELL", "price": random(WFC_price + 100, WFC_price + 10000), "size": 2})
            
    #         print("Trade 2 requested")
    
    

if __name__ == "__main__":
    main()
