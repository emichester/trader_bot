# trader_API
This is a simple api to get information of stock at stock market

## Setup

1. Create your telegram bot. Follow [instructions](https://core.telegram.org/bots#3-how-do-i-create-a-bot).
2. Get you [telegram chat id](https://docs.influxdata.com/kapacitor/v1.5/event_handlers/telegram/#get-your-telegram-chat-id).

```bash
$ git clone https://github.com/emichester/trader_API.git
$ cd trader_API
$ mkdir config && touch config/data.py
$ echo "
TOKEN = 'your-bot-token'
MI_CHAT_ID = you-chat-id ### int format e.g. 123456789
" > config/data.py
$ chmod +x simple_telegram_advisor.py
```

Install _requirements.txt_

```bash
$ pip3 install -r requirements.txt
```

If you don't have pip install it (python3-pip).

## Usage

In the main function change the following lines. For example:

```python
    price = {
        "GME" : 220.0,
        "AMC" : 14.0,
        "PLUG" : 39.0,
    }

    cont = 0

    while True:
        cont = see_price("GME", price["GME"], cont)
        cont = see_price("AMC", price["AMC"], cont)
        cont = see_price("PLUG", price["PLUG"], cont)
        logging
        time.sleep(1)
```

Finally run the bot with the following comand.

```bash
$ ./simple_telegram_advisor.py
```
[//]: # "https://stackoverflow.com/questions/20975400/get-div-from-html-with-python"
[//]: # "https://stackoverflow.com/questions/40333267/extracting-content-within-multiple-span-tags-in-beautifulsoup"