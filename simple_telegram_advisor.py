#!/usr/bin/env python3
import requests
import time
from bs4 import BeautifulSoup
import logging

from config.data import TOKEN, MI_CHAT_ID
from config.RPi_utils import RPi_relax_time

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

    import concurrent.futures
    from config.stock_list import stocks

    cont = [0]

    while True:
        t = time.time()
        with concurrent.futures.ThreadPoolExecutor() as executor: # optimally defined number of threads
            res = [executor.submit(see_price,
                stock, 
                stocks[stock]['high'],
                stocks[stock]['low'],
                cont,
                th
                ) for th, stock in enumerate(stocks)]
        logging.debug("\tTotal time: %f"%(time.time()-t))
        time.sleep(RPi_relax_time)
        

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.warning("Exiting with code 0 on %s"%str(time.ctime()))
        print("\n")
