#!/usr/bin/env python3
import requests
import time
from bs4 import BeautifulSoup
import logging

from config.data import TOKEN, MI_CHAT_ID

def telegram_bot_sendtext(bot_message, chat_id):
    
    bot_token = TOKEN
    bot_chatID = str(chat_id)
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def see_price(name="GME", PRICE_HIGH=225.0, PRICE_LOW=170.0, cont=0):
    url = 'https://finance.yahoo.com/quote/%s?p=%s'%(name,name)

    req = requests.get(url)
    html = req.text

    soup = BeautifulSoup(html, 'html.parser')

    try:
        price = soup.find_all('div',{"class" : "D(ib) Mend(20px)"})
        price = [element.text.strip() for element in price[0]]
        price = float(price[0])
        logging.info("Precio: %s"%str(price))
        
        try:
            price_AfHo = soup.find_all('p',{"class" : "Fz(12px) C($tertiaryColor) My(0px) D(ib) Va(b)"})
            price_AfHo = [element.text.strip() for element in price_AfHo]
            price_AfHo = float(price_AfHo[0][0:6])
            logging.info("Precio after hours: %s"%str(price_AfHo))

        except Exception as e:
            price_AfHo = 0
            logging.warn("Problemas, excepción %i: %s"%(cont, str(e)))
            logging.warn("Probablemente el mercado esté abierto y no aparezca este campo")

        if price >= PRICE_HIGH:
            msg = "Vende que %s está a %.2f"%(name,price)
            telegram_bot_sendtext(msg, MI_CHAT_ID)
        elif price <= PRICE_LOW:
            msg = "Compra que %s está a %.2f"%(name,price)
            telegram_bot_sendtext(msg, MI_CHAT_ID)

    except Exception as e:
        cont+=1
        logging.warn("Problemas, excepción %i: %s"%(cont, str(e)))

    if cont > 10:
        msg = "OJO con la API que está dando problemas"
        telegram_bot_sendtext(msg, MI_CHAT_ID)
        cont = 0
    
    return cont
    
def main():
    with open("debug.log","w") as f:
        f.write("")

    logging.basicConfig(filename="debug.log",level=logging.DEBUG,format="%(asctime)s:%(levelname)s:%(message)s")

    from config.stock_list import stocks

    cont = 0

    while True:
        for stock in stocks:
            cont = see_price(stock, 
                stocks[stock]['high'],
                stocks[stock]['low'],
                cont)
        time.sleep(1)
        

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('trader_API exited with code 0')
