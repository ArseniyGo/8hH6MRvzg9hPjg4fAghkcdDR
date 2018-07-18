import requests
import time
import telebot
bot = telebot.TeleBot('678797318:AAH6ImhT2dyJf1Y20-kBwFw1MSxezDLoSVg')
while True:
    book = requests.get('https://api.bitfinex.com/v2/book/tBTCUSD/P1?len=100').json()
    buy = []
    sell = []
    for i in book:
        if i[2] < 0:
            sell.append([i[0], -i[2]])
        else:
            buy.append([i[0], i[2]])
    buy, sell = buy[:50], sell[:50]
    maxb = 0
    for i in buy: 
        if i[1] > maxb: 
            maxb = i[1]
    for i in sell: 
        if i[1] > maxb: 
            maxb = i[1]
    maxb = 70 / maxb
    m = ''
    buy[0][0] = '*' + str(buy[0][0]) + '*'
    for i in sell[::-1]:
        m += str(i[0]) + ' ' + '.' * int(i[1] * maxb) + ' -' + '{0:.2f}'.format(i[1]) + ' BTC\n'
    for i in buy:
        m += str(i[0]) + ' ' + ',' * (int(i[1] * maxb)) + ' ' + '{0:.2f}'.format(i[1]) + ' BTC\n'
    bot.edit_message_text(chat_id = '@cryptoscanning', message_id = 2284, text =  m, parse_mode = "Markdown")
    time.sleep(2)
