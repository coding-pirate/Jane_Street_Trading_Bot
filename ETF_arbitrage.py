x`#!/usr/bin/python

from __future__ import print_function

import sys
import socket
import json
import time
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
    
    XLF_price = 0
    GS_price = 0
    MS_price = 0
    WFC_price = 0
    BOND_price = 0

    while True:
        dic = read_from_exchange(exchange)
        
        if dic['type'] == 'trade' and dic['symbol'] == 'XLF':
            XLF_price = dic['price']
    
        if dic['type'] == 'trade' and dic['symbol'] == 'GS'  :
            GS_price = dic['price']
    
        if dic['type'] == 'trade' and dic['symbol'] == 'MS'  :
            MS_price = dic['price']
    
        if dic['type'] == 'trade' and dic['symbol'] == 'WFC'  :
            WFC_price = dic['price']
    
        if dic['type'] == 'trade'  and dic['symbol'] == 'BOND'  :
            BOND_price = dic['price']
        
        if ((10*XLF_price) - (3*BOND_price + 2*GS_price + 3*MS_price + 2*WFC_price) >= 10) :

            write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "XLF", "dir": "SELL", "price": XLF_price + 1, "size": 10})
            
            write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "BOND", "dir": "BUY", "price": BOND_price - 1, "size": 3})
            
            write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "MS", "dir": "BUY", "price": MS_price - 1, "size": 3})
            
            write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "GS", "dir": "BUY", "price": GS_price - 1, "size": 2})
            
            write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "WFC", "dir": "BUY", "price": WFC_price - 1, "size": 2})
            
            print("Trade 1 executed")

        if ( (3*BOND_price + 2*GS_price + 3*MS_price + 2*WFC_price) - (10*XLF_price) >= 10) :

            write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "XLF", "dir": "BUY", "price": XLF_price - 1 , "size": 10})
            
            write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "BOND", "dir": "SELL", "price": BOND_price + 1, "size": 3})
            
            write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "MS", "dir": "SELL", "price": MS_price + 1, "size": 3})
            
            write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "GS", "dir": "SELL", "price": GS_price + 1 , "size": 2})
            
            write_to_exchange(exchange, {"type": "add", "order_id": random(100, 400000000000000), "symbol": "WFC", "dir": "SELL", "price": WFC_price + 1, "size": 2})
            
            print("Trade 2 executed")
    
    

if __name__ == "__main__":
    main()
