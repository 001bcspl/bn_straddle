###############################################################################
###############################################################################
from key import api_k, api_s, access_token
import key
###############################################################################

API_KEY = api_k #enter api_key madan
ACCESS_TOKEN =access_token  #enter madan
###############################################################################

import time
import calendar
import logging
import pandas as pd

from datetime import datetime
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta, TH, WE, MO, TU, FR
from kiteconnect import KiteConnect
from zoneinfo import ZoneInfo

def get_kite():
    kiteObj = KiteConnect(api_key=API_KEY)
    kiteObj.set_access_token(ACCESS_TOKEN)
    return kiteObj


kite = get_kite()
instrumentsList = None

def round_to_multiple(number, multiple):
    return multiple * round(number / multiple)

def getCMP(tradingSymbol):
    quote = kite.quote(tradingSymbol)
    #print(quote)
    #print(quote[tradingSymbol]['last_price'])
    if quote:
        return quote[tradingSymbol]['last_price']
    else:
        return 0


def get_symbols(expiry, name, strike, ins_type):
    global instrumentsList
    print(expiry)
    print(name)
    print(strike)
    print(ins_type)
    #expected ex: 2025-05-29 BANKNIFTY 53500 PE
    if instrumentsList is None:
        instrumentsList = kite.instruments('NFO')

    #print(instrumentsList)
    lst_b = [num for num in instrumentsList if num['expiry'] == expiry and num['strike'] == strike
             and num['instrument_type'] == ins_type and num['name'] == name]
    #print(lst_b)         
    #print(lst_b[0]['tradingsymbol'])
    return lst_b[0]['tradingsymbol']

def place_order(tradingSymbol, price, qty, direction, exchangeType, product, orderType):
    try:
        orderId = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=exchangeType,
            tradingsymbol=tradingSymbol,
            transaction_type=direction,
            quantity=qty,
            price=price,
            product=product,
            order_type=orderType)

        logging.info('Order placed successfully, orderId = %s', orderId)
        return orderId
    except Exception as e:
        logging.info('Order placement failed: %s', e)


def place_order_sl_limit(tradingSymbol, price, qty, direction, exchangeType, product, orderType,tprice):
    try:
        orderId = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=exchangeType,
            tradingsymbol=tradingSymbol,
            transaction_type=direction,
            quantity=qty,
            price=price,
            product=product,
            order_type=orderType,
            trigger_price=tprice)

        logging.info('Order placed successfully, orderId = %s', orderId)
        return orderId
    except Exception as e:
        logging.info('Order placement failed: %s', e)

##### FOR reference ###########################################################################################
def place_limit_order(symbol, buy_sell,quantity,limit_price, exchange="NSE"):
    # Place an intraday market order on NSE
    if buy_sell == "buy":
        t_type=kite.TRANSACTION_TYPE_BUY
    elif buy_sell == "sell":
        t_type=kite.TRANSACTION_TYPE_SELL
    kite.place_order(tradingsymbol=symbol,
                    exchange=exchange,
                    transaction_type=t_type,
                    quantity=quantity,
                    order_type=kite.ORDER_TYPE_LIMIT,
                    product=kite.PRODUCT_MIS,
                    variety=kite.VARIETY_REGULAR,
                    price=limit_price)

def place_sl_limit_order(symbol,buy_sell,quantity, price, trigger_price, exchange="NSE"):
    # Place an intraday market order on NSE
    if buy_sell == "buy":
        t_type=kite.TRANSACTION_TYPE_BUY
    elif buy_sell == "sell":
        t_type=kite.TRANSACTION_TYPE_SELL
    kite.place_order(tradingsymbol=symbol,
                    exchange=exchange,
                    transaction_type=t_type,
                    quantity=quantity,
                    order_type=kite.ORDER_TYPE_SL,
                    product=kite.PRODUCT_MIS,
                    variety=kite.VARIETY_REGULAR,
                    price=price,
                    trigger_price=trigger_price)

def place_sl_market_order(symbol,buy_sell,quantity, trigger_price, exchange="NSE"):
    # Place an intraday market order on NSE
    if buy_sell == "buy":
        t_type=kite.TRANSACTION_TYPE_BUY
    elif buy_sell == "sell":
        t_type=kite.TRANSACTION_TYPE_SELL
    kite.place_order(tradingsymbol=symbol,
                    exchange=exchange,
                    transaction_type=t_type,
                    quantity=quantity,
                    order_type=kite.ORDER_TYPE_SLM,
                    product=kite.PRODUCT_MIS,
                    variety=kite.VARIETY_REGULAR,
                    trigger_price=trigger_price)

# Place market Order
def place_market_order(symbol,buy_sell,quantity,exchange="NSE"):
    # Place an intraday market order on NSE
    if buy_sell == "buy":
        t_type=kite.TRANSACTION_TYPE_BUY
    elif buy_sell == "sell":
        t_type=kite.TRANSACTION_TYPE_SELL
    kite.place_order(tradingsymbol=symbol,
                    exchange=exchange,
                    transaction_type=t_type,
                    quantity=quantity,
                    order_type=kite.ORDER_TYPE_MARKET,
                    product=kite.PRODUCT_MIS,
                    variety=kite.VARIETY_REGULAR)

##### FOR reference ###########################################################################################
#def track_straddle_order()
# for a given strike - get the symbol and hence the price
##### FOR reference ###########################################################################################

def getprice_symbol(atm_strike):
    global t_ltpce,t_ltppe
    global expiry_date

    #today = datetime.datetime.now()
    today = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
    year = today.year
    month = today.month
    print("---test")
    print(today)
    print(year)
    print(month)

    # Get the last Thursday of the month
    cal = calendar.monthcalendar(year, month)
    thursdays = [week[3] for week in cal if week[3] != 0]
    last_thursday = thursdays[-1]
    print(last_thursday)

    # Format the expiry date
    expiry_date = datetime(year, month, last_thursday)
    #expiry_date = datetime(year, month, last_thursday)

    #monthly expiry
    t_symbol_ce = get_symbols(expiry_date.date(), 'BANKNIFTY', atm_strike, 'CE')
    t_symbol_pe = get_symbols(expiry_date.date(), 'BANKNIFTY', atm_strike, 'PE')


    print(t_symbol_ce)
    print(t_symbol_pe)
    t_symbol_cep="NFO:"+t_symbol_ce
    t_symbol_pep="NFO:"+t_symbol_pe

    t_ltpce=getCMP(t_symbol_cep)
    t_ltppe=getCMP(t_symbol_pep)
    print("ltpce=",t_ltpce)
    print("ltppe=",t_ltppe)



if __name__ == '__main__':

    paper_trade=1
    debug = 1

    print("straddle trades - waiting for 9:45AM")
    # wait till 11AM
    while (True):
        if debug == 1:
          break # break test
        now = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
        if(datetime.now(tz=ZoneInfo('Asia/Kolkata')).hour == 9) and (datetime.now(tz=ZoneInfo('Asia/Kolkata')).minute == 45):
            break

    # Create the file name date and time as variable
    now = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
    print("now =", now)
    lfile = now.strftime("./logs/%Y%m%d_rt_0945_bn_straddle.txt")
    day= now.strftime("%Y%m%d")

    print("creating log file --> ", lfile)
    with open(f'{lfile}', 'w', encoding='utf-8') as f:
        f.write('--------------------- starting---------------------------' + '\n')
        f.write(f'{now.strftime(" %d - %m - %Y ::: %H:%M:%S ")}'+ '\n')
        f.write('---------------------------------------------------------' + '\n')

    # Append-adds at last
    file1 = open("./logs/straddle_945am", "a")  # append mode

    papertrade=0
    # Find ATM Strike of Nifty
    # Error atm_strike = round(getCMP('NSE:NIFTY 50'), -2)
    atm_strike= round_to_multiple(getCMP('NSE:NIFTY BANK'), 100)
    print("SPOT nearest 100:", atm_strike)

    print("----------------------------------------------------->")
       # check prices - diff between CE/PE premium, chosse the closest
    getprice_symbol(atm_strike)
    t0_ce=t_ltpce
    t0_pe=t_ltppe
    getprice_symbol(atm_strike+100)
    t1_ce=t_ltpce
    t1_pe=t_ltppe
    getprice_symbol(atm_strike-100)
    t2_ce=t_ltpce
    t2_pe=t_ltppe
    print("------------------")
    print(t0_ce)
    print(t0_pe)

    print(t1_ce)
    print(t1_pe)
    print(t2_ce)
    print(t2_pe)
    diff0=abs(t0_ce-t0_pe)
    diff1=abs(t1_ce-t1_pe)
    diff2=abs(t2_ce-t2_pe)

    if(diff0 < diff1) and (diff0 < diff2):
        f_ltpce=t0_ce
        f_ltppe=t0_pe
        atm_strike=atm_strike

    if(diff1 < diff0) and (diff1 < diff2):
        f_ltpce=t1_ce
        f_ltppe=t1_pe
        atm_strike=atm_strike+100

    if(diff2 < diff0) and (diff2 < diff1):
        f_ltpce=t2_ce
        f_ltppe=t2_pe
        atm_strike=atm_strike-100


    print("------------------")
    print(f_ltpce)
    print(f_ltppe)
    print("------------------")
    print("----------------------------------------------------->")

    #get expiry symbols
    symbol_ce = get_symbols(expiry_date.date(), 'BANKNIFTY', atm_strike, 'CE')
    symbol_pe = get_symbols(expiry_date.date(), 'BANKNIFTY', atm_strike, 'PE')

    #monthly expiry
    #next_thursday_expiry = datetime.today() + relativedelta(weekday=TH(1))
    #symbol_ce = get_symbols(next_thursday_expiry.date(), 'BANKNIFTY', atm_strike, 'CE')
    #symbol_pe = get_symbols(next_thursday_expiry.date(), 'BANKNIFTY', atm_strike, 'PE')


    print(symbol_ce)
    print(symbol_pe)
    if paper_trade != 1:
       place_order(symbol_ce, 0, 30, kite.TRANSACTION_TYPE_SELL, KiteConnect.EXCHANGE_NFO, KiteConnect.PRODUCT_MIS,
                KiteConnect.ORDER_TYPE_MARKET)

    if paper_trade != 1:
       place_order(symbol_pe, 0, 30, kite.TRANSACTION_TYPE_SELL, KiteConnect.EXCHANGE_NFO, KiteConnect.PRODUCT_MIS,
                KiteConnect.ORDER_TYPE_MARKET)



    #SL trades
    symbol_cep="NFO:"+symbol_ce
    symbol_pep="NFO:"+symbol_pe
    #ltpce=getCMP('NFO:NIFTY23AUG19300CE') 
    ltpce=getCMP(symbol_cep)
    ltppe=getCMP(symbol_pep)
    print("ltpce=",ltpce)
    print("ltppe=",ltppe)
    slce=round((round(1.4*ltpce,2)*100)/10,0)/10
    slpe=round((round(1.4*ltppe,2)*100)/10,0)/10
    print("slce=",slce)
    print("slpe=",slpe)
    slce_tprice = slce + 0.5
    slpe_tprice = slpe + 0.5
    print("slce trig price=",slce_tprice)
    print("slpe trig price=",slpe_tprice)

    #SL limit orders 
    if paper_trade != 1:
       place_order_sl_limit(symbol_ce, slce_tprice, 30, kite.TRANSACTION_TYPE_BUY, KiteConnect.EXCHANGE_NFO, KiteConnect.PRODUCT_MIS,
                KiteConnect.ORDER_TYPE_SL,slce)
       print("CE leg triggered")
    if paper_trade != 1:
       place_order_sl_limit(symbol_pe, slpe_tprice, 30, kite.TRANSACTION_TYPE_BUY, KiteConnect.EXCHANGE_NFO, KiteConnect.PRODUCT_MIS,
                KiteConnect.ORDER_TYPE_SL,slpe)
       print("PE leg triggered")

    print("sl limit orders placed") 
       # wait till 3:10PM
    slcehit=0
    slpehit=0
    plmax=0
    plmin=10000
    print("debug")

    while (True):
        time.sleep(1)
        time.sleep(1)
        print("-->");
        now = datetime.now(tz=ZoneInfo('Asia/Kolkata'))
        #check the orders complete and display
        #check the orders pending and display
        #check traded orders has SL ?
        #check positions matching as per the orders
        #check staddle positions every 5minutes and log to file
        pl=0
        ltpce1= getCMP(symbol_cep)
        ltppe1= getCMP(symbol_pep)

        if(ltpce1 > slce):
             slcehit=1

        if(ltppe1 > slpe):
             slpehit=1

        if(slcehit==1):
            ltpce1=slce
        if(slpehit==1):
            ltppe1=slpe

        plce = (ltpce - ltpce1)*30
        plpe = (ltppe - ltppe1)*30

        pl= plce + plpe


        if(pl>plmax):
            plmax=pl
        if(pl<plmin):
            plmin=pl
        hr=datetime.now(tz=ZoneInfo('Asia/Kolkata')).hour
        min=datetime.now(tz=ZoneInfo('Asia/Kolkata')).minute

        ltpce = round(ltpce,2)
        plce = round(plce,2)
        ltppe = round(ltppe,2)
        plpe = round(plpe,2)

        ##--------------------------------------
        ## passed
        ##--------------------------------------
        #import subprocess
        ## Run the command and capture the output 
        ##output = subprocess.check_output("ls", shell=True) # Replace "ls" with your desired command 
        #output = subprocess.check_output("cat temp.txt |awk 'END{print}'|awk -F \":\" '{print $14;}'|awk -F \">\" '{print $2;}'",shell=True)# Convert the output to a string (Python 3.x) 
        #output = output.decode("utf-8")
        #output = float(output)
        ## Print the output 
        #print(output)
        #output=output +1
        #print(output)
        ##-----------------------------------------------------------

        print((f'{day}:{hr}:{min}::{symbol_ce}:{ltpce}:{getCMP(symbol_cep)}:{plce}:{slcehit} - {symbol_pe}:{ltppe}:{getCMP(symbol_pep)}:{plpe}:{slpehit}:-- > {pl}::{plmax}::{plmin}'),file=open(f'{lfile}', 'a'))
        print((f'{day}:{hr}:{min}::{symbol_ce}:{ltpce}:{getCMP(symbol_cep)}:{plce}:{slcehit} - {symbol_pe}:{ltppe}:{getCMP(symbol_pep)}:{plpe}:{slpehit}:-- > {pl}::{plmax}::{plmin}'))



        #exit the logs post the market
        if(datetime.now(tz=ZoneInfo('Asia/Kolkata')).hour == 15) and (datetime.now(tz=ZoneInfo('Asia/Kolkata')).minute == 32):
          print("EOD update writing to file")

          p_apl = 0
          import subprocess
          import random
          #testing purpose set some know value
          #only for test pl=  round(random.uniform(500,1500), 2)
          print(pl)
          #previous PL fetch
          p_apl = subprocess.check_output("cat ./logs/straddle_945am|awk 'END{print}'|awk -F \":\" '{print $19;}'",shell=True)
          # Convert the output to a string (Python 3.x)
          p_apl = p_apl.decode("utf-8")
          print(p_apl)
          #add the current PL to apl
          p_apl = float(p_apl)
          apl = p_apl + pl
          print(p_apl)
          print(pl)
          print(apl)

          file1.write(f'{day}:{hr}:{min}::{symbol_ce}:{ltpce}:{getCMP(symbol_cep)}:{plce}:{slcehit} - {symbol_pe}:{ltppe}:{getCMP(symbol_pep)}:{plpe}:{slpehit}:-- > {pl}::{plmax}::{plmin} -->: {apl}' + '\n')
          file1.close()
          break  
    if(papertrade==0):
        for i in kite.orders():
            if (i['product'] == "MIS"):
                if(i['status']== "COMPLETE"):
                    tdsymbol = i['tradingsymbol']
                    tdprice = i['average_price']
                    tdsymbol1="NFO:"+tdsymbol
                    tdltp=getCMP(tdsymbol)
                    print(tdsymbol,tdprice,tdltp, (tdprice-tdltp)*50)
                    pl=pl+(tdprice-tdltp)*50
        print("outstanding MIS PL --",pl)
        print("-----------------------------------------")

        #outstanding PL as per positions
        b=[]
        b=kite.positions()['net']
        b=pd.DataFrame(b)
        PL=sum(b['pnl'])
        print('\n')
        print(b['tradingsymbol'],b['pnl'])
        print("outstanding PL as per pos:",PL)
        print((f'{day}:{hr}:{min}::{PL}'),file=open(f'{lfile}', 'a'))
        print("-----------------------------------------")

        # waiting for exist

        if(datetime.now(tz=ZoneInfo('Asia/Kolkata')).hour == 14) and (datetime.now(tz=ZoneInfo('Asia/Kolkata')).minute == 55):
            print("exit positions")             
