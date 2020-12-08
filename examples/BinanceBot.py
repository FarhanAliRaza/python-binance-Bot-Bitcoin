
from binance.client import Client
import time
import matplotlib
from decimal import *
from matplotlib import cm
import matplotlib.pyplot as plt
from binance.enums import *
import save_historical_data_Roibal
from BinanceKeys import BinanceKey1
import pandas as pd

api_key = BinanceKey1['api_key']
api_secret = BinanceKey1['api_secret']
import json
client = Client(api_key, api_secret)

# get a deposit address for BTC
address = client.get_deposit_address(asset='BTC')

def run():
    # get system status
    #Create List of Crypto Pairs to Watch
    list_of_symbols = ['BTCUSDT']
    # list_of_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT','BNBBTC', 'ETHBTC', 'LTCBTC']

    # print("\n\n---------------------------------------------------------\n\n")
    # print("Hello and Welcome to the Crypto Trader Bot Python Script\n")
    # print("A quick 'run-through' will be performed to introduce you to the functionality of this bot")
    # time.sleep(1)
    # try:
    #     pass
        #Example Visualizations of Coins
        # save_historical_data_Roibal.save_historic_klines_csv('BTCUSDT', "1 hours ago UTC", "now UTC", Client.KLINE_INTERVAL_1MINUTE)
        # save_historical_data_Roibal.save_historic_klines_csv('BTCUSDT', "12 months ago UTC", "now UTC", Client.KLINE_INTERVAL_1WEEK)


    # except():
    #     pass
    #Get Status of Exchange & Account
    try:
        status = client.get_system_status()
        print("\nExchange Status: ", status)

        #Account Withdrawal History Info
        # withdraws = client.get_withdraw_history()
        # print("\nClient Withdraw History: ", withdraws)

        #get Exchange Info
        # info = client.get_exchange_info()
        # print("\nExchange Info (Limits): ", info)
    except():
        pass

    # place a test market buy order, to place an actual order use the create_order function
    # if '1000 ms ahead of server time' error encountered, visit https://github.com/sammchardy/python-binance/issues/249
    try:
        order = client.create_test_order(
            symbol='BTCUSDT',
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=100)
    except:
        print("\n \n \nATTENTION: NON-VALID CONNECTION WITH BINANCE \n \n \n")

    #Get Info about Coins in Watch List
    # coin_prices(list_of_symbols)
    # coin_tickers(list_of_symbols)
    candles = save_historical_data_Roibal.candles('BTCUSDT', "1 hours ago UTC", "now UTC", Client.KLINE_INTERVAL_1MINUTE)
    pre_high = candles[-1][3]
    write_file(pre_high)
    #profit percentage
    PROFIT = 5
    # new_write_file()
    while True:
        time.sleep(10)

        candles = get_data()
        print(candles)
        if is_red_candle(candles[-1][1], candles[-1][2]):
            print("red")
            red_candle(candles[-1][3])

        else:
            print("Green")
            green_candle(candles, PROFIT)


        create_summary()





def get_data():
    candles = save_historical_data_Roibal.candles('BTCUSDT', "1 hours ago UTC", "now UTC", Client.KLINE_INTERVAL_1MINUTE)
    return candles
def is_red_candle(open, close):
    if close < open:
        print("Red Candle")
        return True
def red_candle(high):
    pre_high = read_file()
    pre_high = Decimal(pre_high)
    print(pre_high)
    if high<pre_high:
        try:
            cancel_previous_orders()
        except:
            pass
        write_file(high)

        return print("Creating New order with new red candle high")
def cancel_previous_orders():
    try:
        orders = client.get_open_orders(symbol='BTCUSDT')
    except Exception as e:
        print(e)
    if not orders:
        data = read_buy_file()
        if data:
            data[-1]['is_filled']=True
        write_buy_file(data)
        return print("No Previous_orders")
    for order in orders:
        client.cancel_order(symbol='BTCUSDT', orderId = order['orderId'])


def green_candle(candles, p):
    if check_profit(p):
        sell_order()
    return print("Profit margin not met")




def check_profit(p):
    orders = read_buy_file()
    if not orders:
        return False

    total_price = 0
    counter = 0
    for order in orders:
        print(order)
        if order['is_filled']==True:
            total_price += order['price']
            counter += 1
    mean_price = total_price/counter
    try:
        avg_price = client.get_avg_price(symbol="BTCUSDT")
    except Exception as e:
        print(e)
    if (mean_price/avg_price)*100 < p:
        print("Not required profit")
        return False
    return True


def read_file():
    with open('pre_high.txt') as json_file:
        data = json.load(json_file)
        return data['pre_high']


def write_file(h):
    data = {}
    data['pre_high'] = f'{h}'
    with open('pre_high.txt', 'w') as outfile:
        json.dump(data, outfile)
def new_write_file():
    data = []
    with open('buy.txt', 'w') as outfile:
        json.dump(data, outfile)
def read_buy_file():
    with open('buy.txt') as json_file:
        data = json.load(json_file)
        return data
def write_buy_file(data):
    with open('buy.txt', 'w') as outfile:
        json.dump(data, outfile)

def sell_order():
    balance = client.get_asset_balance(asset='BTC')
    try:
        if balance is None:
            return print("Not bought yet")
        client.order_market_sell(symbol='BTCUSDT', quantity=balance)
    except Exception as e:
        return print(e)


def create_buy_order(high):
    high = Decimal(high)
    quantity = high/5
    try:
        order = client.order_limit_buy(
                symbol='BTCUSDT',
                quantity=quantity,
                price=high)
        order = {"quantity":quantity,
                "price" : high,
                 'is_filled':False}
        orders = read_buy_file()
        orders.append(order)
        write_buy_file(orders)
    except Exception as e:
        print(e)
def create_summary():
    orders = client.get_all_orders(symbol='BTCUSDT')
    if orders:
        import csv
        keys = orders[0].keys()
        with open('summary.csv', 'w', newline='')  as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(orders)

def create_test_buy_order(high):
    high = Decimal(high)
    quantity = high/5
    try:
        order = client.create_test_order(
                symbol='BTCUSDT',
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_LIMIT,
                quantity=quantity,
                timeInForce = client.TIME_IN_FORCE_GTC,
                newClientOrderId='myorder1',
                price= high)
    except Exception as e:
        print(e)
    orders = client.get_open_orders(symbol='BTCUSDT')
    print(orders)



def convert_time_binance(gt):
    #Converts from Binance Time Format (milliseconds) to time-struct
    #From Binance-Trader Comment Section Code
    #gt = client.get_server_time()
    print("Binance Time: ", gt)
    print(time.localtime())
    aa = str(gt)
    bb = aa.replace("{'serverTime': ","")
    aa = bb.replace("}","")
    gg=int(aa)
    ff=gg-10799260
    uu=ff/1000
    yy=int(uu)
    tt=time.localtime(yy)
    #print(tt)
    return tt


def market_depth(sym, num_entries=20):
    #Get market depth
    #Retrieve and format market depth (order book) including time-stamp
    i=0     #Used as a counter for number of entries
    print("Order Book: ", convert_time_binance(client.get_server_time()))
    depth = client.get_order_book(symbol=sym)
    print(depth)
    print(depth['asks'][0])
    ask_tot=0.0
    ask_price =[]
    ask_quantity = []
    bid_price = []
    bid_quantity = []
    bid_tot = 0.0
    place_order_ask_price = 0
    place_order_bid_price = 0
    max_order_ask = 0
    max_order_bid = 0
    print("\n", sym, "\nDepth     ASKS:\n")
    print("Price     Amount")
    for ask in depth['asks']:
        if i<num_entries:
            if float(ask[1])>float(max_order_ask):
                #Determine Price to place ask order based on highest volume
                max_order_ask=ask[1]
                place_order_ask_price=round(float(ask[0]),5)-0.0001
            #ask_list.append([ask[0], ask[1]])
            ask_price.append(float(ask[0]))
            ask_tot+=float(ask[1])
            ask_quantity.append(ask_tot)
            #print(ask)
            i+=1
    j=0     #Secondary Counter for Bids
    print("\n", sym, "\nDepth     BIDS:\n")
    print("Price     Amount")
    for bid in depth['bids']:
        if j<num_entries:
            if float(bid[1])>float(max_order_bid):
                #Determine Price to place ask order based on highest volume
                max_order_bid=bid[1]
                place_order_bid_price=round(float(bid[0]),5)+0.0001
            bid_price.append(float(bid[0]))
            bid_tot += float(bid[1])
            bid_quantity.append(bid_tot)
            #print(bid)
            j+=1
    return ask_price, ask_quantity, bid_price, bid_quantity, place_order_ask_price, place_order_bid_price
    #Plot Data


def visualize_market_depth(wait_time_sec='1', tot_time='1', sym='BTCUSDT', precision=5):
    cycles = int(tot_time)/int(wait_time_sec)
    start_time = time.asctime()
    fig, ax = plt.subplots()
    for i in range(1,int(cycles)+1):
        ask_pri, ask_quan, bid_pri, bid_quan, ask_order, bid_order = market_depth(sym)

        #print(ask_price)
        plt.plot(ask_pri, ask_quan, color = 'red', label='asks-cycle: {}'.format(i))
        plt.plot(bid_pri, bid_quan, color = 'blue', label = 'bids-cycle: {}'.format(i))

        #ax.plot(depth['bids'][0], depth['bids'][1])
        max_bid = max(bid_pri)
        min_ask = min(ask_pri)
        max_quant = max(ask_quan[-1], bid_quan[-1])
        spread = round(((min_ask-max_bid)/min_ask)*100,5)   #Spread based on market
        proj_order_spread = round(((ask_order-bid_order)/ask_order)*100, precision)
        price=round(((max_bid+min_ask)/2), precision)
        plt.plot([price, price],[0, max_quant], color = 'green', label = 'Price - Cycle: {}'.format(i)) #Vertical Line for Price
        plt.plot([ask_order, ask_order],[0, max_quant], color = 'black', label = 'Ask - Cycle: {}'.format(i))
        plt.plot([bid_order, bid_order],[0, max_quant], color = 'black', label = 'Buy - Cycle: {}'.format(i))
        #plt.plot([min_ask, min_ask],[0, max_quant], color = 'grey', label = 'Min Ask - Cycle: {}'.format(i))
        #plt.plot([max_bid, max_bid],[0, max_quant], color = 'grey', label = 'Max Buy - Cycle: {}'.format(i))
        ax.annotate("Max Bid: {} \nMin Ask: {}\nSpread: {} %\nCycle: {}\nPrice: {}"
                    "\nPlace Bid: {} \nPlace Ask: {}\n Projected Spread: {} %".format(max_bid, min_ask, spread, i, price, bid_order, ask_order, proj_order_spread),
                    xy=(max_bid, ask_quan[-1]), xytext=(max_bid, ask_quan[0]))
        if i==(cycles+1):
            break
        else:
            time.sleep(int(wait_time_sec))
    #end_time = time.asctime()
    ax.set(xlabel='Price', ylabel='Quantity',
       title='Binance Order Book: {} \n {}\n Cycle Time: {} seconds - Num Cycles: {}'.format(sym, start_time, wait_time_sec, cycles))
    plt.legend()
    plt.show()
    return ask_pri, ask_quan, bid_pri, bid_quan, ask_order, bid_order, spread, proj_order_spread, max_bid, min_ask


def coin_prices(watch_list):
    #Will print to screen, prices of coins on 'watch list'
    #returns all prices
    prices = client.get_all_tickers()
    print("\nSelected (watch list) Ticker Prices: ")
    for price in prices:
        if price['symbol'] in watch_list:
            print(price)
    return prices


def coin_tickers(watch_list):
    # Prints to screen tickers for 'watch list' coins
    # Returns list of all price tickers
    tickers = client.get_orderbook_tickers()
    print("\nWatch List Order Tickers: \n")
    for tick in tickers:
        if tick['symbol'] in watch_list:
            print(tick)
    return tickers


#Place Limit Order
"""
order = client.order_limit_buy(
    symbol='BNBBTC',
    quantity=100,
    price='0.00001')

order = client.order_limit_sell(
    symbol='BNBBTC',
    quantity=100,
    price='0.00001')
"""





#place an order on Binance
"""
order = client.create_order(
    symbol='BNBBTC',
    side=SIDE_BUY,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=100,
    price='0.00001')
"""

if __name__ == "__main__":
    run()
