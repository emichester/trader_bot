# trader_bot
This is a simple api to get information of stocks at stock market. Custom price notifications given high and low thresholds.

## Setup

1. Create your telegram bot. Follow [instructions](https://core.telegram.org/bots#3-how-do-i-create-a-bot).
2. Get you [telegram chat id](https://docs.influxdata.com/kapacitor/v1.5/event_handlers/telegram/#get-your-telegram-chat-id).

```bash
$ git clone https://github.com/emichester/trader_API.git
$ cd trader_API
$ mkdir config && touch config/data.py && touch config/stock_list.py && touch config/RPi_utils.py && touch config/crypto_list.py
$ echo "
TOKEN = 'your-bot-token'
MI_CHAT_ID = you-chat-id ### int format e.g. 123456789
" > config/data.py
$ echo "
RPi_relax_time = 10.0
# you have a limit of 2000 requests/hour or 48000 requests/day (market open 9 h/day)
# time_h >= Nºstock * 3600 / 2000 --------> per hour
# time_d >= Nºstock * 3600 * 9 / 48000 ---> per day
# 
# RPi_relax_time = max(time_h,time_d)

CRYPTO_time = 10.0

NOTIFICATION_TIME = 5.0*60
" > config/RPi_utils.py # if you overpass the limit you won't get the web actualized
$ chmod +x simple_telegram_advisor.py
```

Install _requirements.txt_

```bash
$ pip3 install -r requirements.txt
```

If you don't have pip install it (python3-pip).

## Usage of stock notifications

Open _"config/stock_list.py"_ and modify the dictionary as you want. For example:

```python
stocks = {
    "GME" : {'high' : 225.0 , 'low' : 170.0 },
    "AMC" : {'high' : 14.0 , 'low' : 9.0},
    "PLUG" : {'high' : 40.0 , 'low' : 30.0},
}
```

Finally run the bot with the following comand.

```bash
$ ./simple_telegram_advisor.py
```

Change the `RPi_relax_time` in the file _"config/RPi_utils.py"_ deppending on the CPU usage you want to be used and if you need very high precision use `RPi_relax_time = 0.0` (if you use a regular PC use `0.0` also).

**IMPORTANT!!!** if you overpass the requests limit you won't get the web actualized.

## Usage of crypto notifications

Open _"config/crypto_list.py"_ and modify the dictionary as you want. For example:

```python
cryptos = {
	"DOGE-USD" : {'high' : 0.45 , 'low' : 0.33},
    "BTC-USD" : {'high' : 70000.0 , 'low' : 60000.0},
}
```

Finally run the bot with the following comand.

```bash
$ ./simple_telegram_advisor_cryptos.py
```

Change the `CRYPTO_time` in the file _"config/RPi_utils.py"_ deppending on the CPU usage you want to be used and if you need very high precision use `CRYPTO_time = 10` (if you use a regular PC use `0.0` also).

**IMPORTANT!!!** if you overpass the requests limit you won't get the web actualized.

## ToDo
- [x] Buy notice
- [x] Sell notice
- [ ] After-hours and pre-market report and analysis
- [x] Threaded version


[//]: # "https://stackoverflow.com/questions/20975400/get-div-from-html-with-python"
[//]: # "https://stackoverflow.com/questions/40333267/extracting-content-within-multiple-span-tags-in-beautifulsoup"
[//]: # "https://stackoverflow.com/questions/62007674/multi-thread-requests-python3"
[//]: # "https://stackoverflow.com/questions/53648211/attributeerror-module-concurrent-has-no-attribute-futures-when-i-try-parall"
[//]: # "https://stackoverflow.com/questions/11029717/how-do-i-disable-log-messages-from-the-requests-library"
[//]: # "https://stackoverflow.com/questions/8113782/split-string-on-whitespace-in-python"
