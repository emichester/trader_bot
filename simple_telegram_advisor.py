#!/usr/bin/env python3
import requests
import time
from bs4 import BeautifulSoup
import logging
import threading

from config.data import TOKEN, MI_CHAT_ID
from config.RPi_utils import RPi_relax_time

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

def see_price(name="GME", PRICE_HIGH=225.0, PRICE_LOW=170.0, cont=[0], th=0):
    url = 'https://finance.yahoo.com/quote/%s?p=%s'%(name,name)
    
    req = requests.get(url)
    html = req.text

    soup = BeautifulSoup(html, 'html.parser')

    try:
        price = soup.find_all('div',{"class" : "D(ib) Mend(20px)"})
        price = [element.text.strip() for element in price[0]]
        price = float(price[0])
        logging.info("\tTh%i %s Precio: %s"%(th,name,str(price)))
        
        try:
            debug_price_AfHo = soup.find_all('p',{"class" : "Fz(12px) C($tertiaryColor) My(0px) D(ib) Va(b)"})
            price_AfHo = [element.text.strip() for element in debug_price_AfHo]
            if price_AfHo == []:
                price_AfHo = 0
                logging.debug("\tTh%i %s No se encuentra este campo, horas de mercado abierto"%(th,name))
            else:
                price_AfHo = price_AfHo[0].split()
                price_AfHo = float(price_AfHo[0])
                logging.info("\tTh%i %s Precio after hours: %s"%(th,name,str(price_AfHo)))

        except Exception as e:
            logging.warning("\tTh%i %s Problemas, excepción %i: %s"%(th,name,cont[0],str(e)))
            logging.warning("\tTh%i %s price_AfHo = %s"%(th,name,debug_price_AfHo))
            price_AfHo = 0

        if price >= PRICE_HIGH:
            msg = "Vende que %s está a %.2f"%(name,price)
            telegram_bot_sendtext(msg, MI_CHAT_ID)
        elif price <= PRICE_LOW:
            msg = "Compra que %s está a %.2f"%(name,price)
            telegram_bot_sendtext(msg, MI_CHAT_ID)

    except Exception as e:
        cont[0]+=1
        logging.warning("\tTh%i %s Problemas, excepción %i: %s"%(th,name,cont[0],str(e)))

    if cont[0] > 10:
        msg = "OJO con la API que está dando problemas"
        telegram_bot_sendtext(msg, MI_CHAT_ID)
        cont[0] = 0
    
def main():
    with open("debug.log","w") as f:
        f.write("")

    logging.basicConfig(filename="debug.log",level=logging.DEBUG,format="%(asctime)s:%(levelname)s:%(message)s")
    logging.getLogger("urllib3").setLevel(logging.WARNING) # requests DEBUG inf ignored
    
    t = time.localtime()
    logging.debug("\tMain thread ongoing at %d:%d"%(t.tm_hour,t.tm_min))

    import os, concurrent.futures

    cont = [0]

    while ongoing:
        from config.stock_list import stocks
        t = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(32, os.cpu_count() + 4)) as executor: # optimally defined number of threads
            res = [executor.submit(see_price,
                stock, 
                stocks[stock]['high'],
                stocks[stock]['low'],
                cont,
                th
                ) for th, stock in enumerate(stocks)]
        logging.debug("\tTotal time: %f"%(time.time()-t))
        time.sleep(RPi_relax_time)
    t = time.localtime()
    logging.debug("\tMain thread stoped at %d:%d"%(t.tm_hour,t.tm_min))

if __name__ == "__main__":
    try:
        import argparse, time
        parser = argparse.ArgumentParser(description="Stock Market bot")
        parser.add_argument('-p','--programed',action='store_true',
            help="Scheduled start time of the bot")
        args = parser.parse_args()
        if args.programed:
            while True:
                t = time.localtime()
                if ( 14 <= t.tm_hour < 23) and not ongoing:
                    ongoing = True
                    main_thread = StoppableThread(target=main)
                    main_thread.start()
                if (t.tm_hour >= 23 or t.tm_hour < 14):
                    ongoing = False
                    try:
                        if main_thread.is_alive():
                            main_thread.stop()
                    except NameError:
                        pass
                time.sleep(60)
        else:
            ongoing = True
            main()
    except KeyboardInterrupt:
        logging.warning("Exiting with code 0 on %s"%str(time.ctime()))
        print("\n")
