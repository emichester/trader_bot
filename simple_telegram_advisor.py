"""
mi api:
    https://stackoverflow.com/questions/20975400/get-div-from-html-with-python
    https://stackoverflow.com/questions/40333267/extracting-content-within-multiple-span-tags-in-beautifulsoup
"""
import requests
import time
from bs4 import BeautifulSoup

from config.datos import TOKEN, MI_CHAT_ID

def telegram_bot_sendtext(bot_message, chat_id):
    
    bot_token = TOKEN
    bot_chatID = str(chat_id)
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def see_price(name="GME", PRICE=225.0, cont=0):
    url = 'https://finance.yahoo.com/quote/%s?p=%s'%(name,name)

    req = requests.get(url)
    html = req.text

    soup = BeautifulSoup(html, 'html.parser')

    price = soup.find_all('div',{"class" : "D(ib) Mend(20px)"})
    price = [element.text.strip() for element in price[0]]
    price = float(price[0])

    try:
        price_AfHo = soup.find_all('p',{"class" : "Fz(12px) C($tertiaryColor) My(0px) D(ib) Va(b)"})
        price_AfHo = [element.text.strip() for element in price_AfHo]
        price_AfHo = float(price_AfHo[0][0:6])
    except:
        cont+=1
        price_AfHo = 0

    if price >= PRICE:
        msg = "Vende que GME está a %f"%price
        telegram_bot_sendtext(msg, MI_CHAT_ID)

    if cont > 10:
        msg = "OJO con la API que está dando problemas"
        telegram_bot_sendtext(msg, MI_CHAT_ID)
        cont = 0
    
    return cont
    
def main():

    PRICE = 220.0
    cont = 0

    while True:
        cont = see_price("GME", PRICE, cont)
        time.sleep(1)
        

if __name__ == "__main__":
    main()