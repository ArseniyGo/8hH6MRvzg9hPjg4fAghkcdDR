import requests
import json
import telebot
import time
import traceback
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
bot = telebot.TeleBot("592804892:AAGPnvbvCRRlMv0AuyD_F0THfk7UMBtgU64")
address = [i.rstrip().split() for i in open('Adresses.txt', 'r')] #Получение адресов из файла
addresses = {}
for i in address:
    if len(i) == 2:
        addresses[i[0]] = i[1]
    else:
        addresses[i[0]] = ''
while True:
        xx = int(open('lp.txt', 'r').readline())
        if int(time.time()) - xx >= 86400:
            bintok = [line.rstrip().split() for line in open('binancetokens.txt', 'r')]
            bintok0 = ''
            bintok1 = ''
            for sym in bintok[0]:
                bintok0 += sym + ' '
            for sym in bintok[1]:
                bintok1 += sym + ' '
            ssu = [int(i.rstrip()) for i in open('24hb.txt', 'r')]
            su = [0] * len(ssu)
            balreq = ['https://blockchain.info/ru/balance?active=', 'https://blockchain.info/ru/balance?active=']
            cnt = 0
            for addr in addresses:
                balreq[cnt // 100] += addr + '|'
                cnt += 1
            balreq[0] = requests.get(balreq[0][:-1]).json()
            balreq[1] = requests.get(balreq[1][:-1]).json()
            bals = {}
            for f in balreq[0]:
                bals[f] = balreq[0][f]
            for f in balreq[1]:
                bals[f] = balreq[1][f]
            for f in bals:
                su[0] += bals[f]['final_balance'] // 10 ** 8
            bot.send_message('-1001362959453', 'Баланс топ 100 кошельков и горячих кошельков бирж: *' + ('+' * (su[0] >= ssu[0])) + str(su[0] - ssu[0]) + ' BTC*' +
                             (len(bintok0) != 0) * '\r\nТокены ERC-20, которые скинули с горячих кошельков Binance на холодный: *' + bintok0 +
                             (len(bintok1) != 0) * '\r\nТокены ERC-20, которые скинули с холодного кошелька Binance на горячие: *' + bintok1 + '\r\n#24hChange', parse_mode='Markdown')
            ssu = open('24hb.txt', 'w')
            for dfh in su:
                ssu.write(str(dfh) + '\n')
            ssu.close()
            xx = open('lp.txt', 'w')
            xx.write(str(int(time.time())))
            xx.close()
            xx = open('binancetokens.txt', 'w')
            xx.write('\n\n\n')
            xx.close()
