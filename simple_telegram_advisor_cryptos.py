#!/usr/bin/env python3
import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time, os
from scipy.signal import savgol_filter, butter, filtfilt
from bs4 import BeautifulSoup
import logging
import threading
import json

from config.data import TOKEN, MI_CHAT_ID
from config.RPi_utils import RPi_relax_time, CRYPTO_time 

## global variables
ongoing = False

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition.
    https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
    """
    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


def telegram_bot_sendtext(bot_message, chat_id):
    
    bot_token = TOKEN
    bot_chatID = str(chat_id)
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def retrieve_crypto_price():
    url = "https://finance.yahoo.com/cryptocurrencies/"
    
    # logging.debug('WEB %s'%str(requests(url).text))
    html = requests.get(url)
    html = html.text

    # read html and look for tables
    df = pd.read_html(html, encoding = 'utf-8', decimal=".", thousands=",")
#     logging.debug("""
# #############################################################################
# #############################################################################
#                                 Dataframe
# #############################################################################
# #############################################################################
# %s
# #############################################################################
# #############################################################################
# """%df)
    df = df[0]

    # symbol, name and price
    return df[['Symbol','Name','Price (Intraday)']]

def get_price(df, symbol):
    # select the ones you want
    return df.loc[ df['Symbol'] == symbol ]['Price (Intraday)'].values[0]

def analyse(vector, delta_t):
    pass

def notify_by_price(df, symbol="DOGE-USD", PRICE_HIGH=25.0, PRICE_LOW=14.0, cont=[0], th=0):
    try:

        price = get_price(df, symbol)

        logging.info("\t----> Th%i %s Precio: %s"%(th,symbol,str(price)))

        if price >= PRICE_HIGH:
            msg = "Vende que %s está a %.2f"%(symbol,price)
            telegram_bot_sendtext(msg, MI_CHAT_ID)
        elif price <= PRICE_LOW:
            msg = "Compra que %s está a %.2f"%(symbol,price)
            telegram_bot_sendtext(msg, MI_CHAT_ID)

    except Exception as e:
        cont[0]+=1
        logging.warning("\tTh%i %s Problemas, excepción %i: %s"%(th,name,cont[0],str(e)))

    cont[0]+=1
    logging.warning("\tTh%i %s Problemas, excepción %i: %s"%(th,name,cont[0],str(e)))
    
def main():
    with open("debug_cryptos.log","w") as f:
        f.write("")

    logging.basicConfig(filename="debug_cryptos.log",level=logging.DEBUG,format="%(asctime)s:%(levelname)s:%(message)s")
    logging.getLogger("urllib3").setLevel(logging.WARNING) # requests DEBUG inf ignored
    
    t = time.localtime()
    logging.debug("\tMain thread ongoing at %d:%d"%(t.tm_hour,t.tm_min))

    import os, concurrent.futures

    global ongoing

    cont = [0]

    while ongoing:
        from config.crypto_list import cryptos
        t = time.time()
        df = retrieve_crypto_price()
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(32, os.cpu_count() + 4)) as executor: # optimally defined number of threads
            res = [executor.submit(notify_by_price,
                df,
                symbol, 
                cryptos[symbol]['high'],
                cryptos[symbol]['low'],
                cont,
                th
                ) for th, symbol in enumerate(cryptos)]
        logging.debug("\tTotal time: %f"%(time.time()-t))
        time.sleep(CRYPTO_time)
    t = time.localtime()
    logging.debug("\tMain thread stoped at %d:%d"%(t.tm_hour,t.tm_min))

if __name__ == "__main__":
    try:
        ongoing = True
        main()
    except KeyboardInterrupt:
        ongoing = False
        logging.warning("Exiting with code 0 on %s"%str(time.ctime()))
        print("\n")
