import requests
import telebot
import time
import traceback
bot = telebot.TeleBot("592804892:AAGPnvbvCRRlMv0AuyD_F0THfk7UMBtgU64")
def send(m): #Функция для отправки сообщений
        global bot
        bot.send_message('-1001362959453', m, parse_mode = 'Markdown')
        bot.send_message('-1001180648345', m, parse_mode = "Markdown")
address = [i.rstrip().split() for i in open('Tether.txt', 'r')]
addresses = {}
for i in address:
    if len(i) == 2:
        addresses[i[0]] = i[1]
    else:
        addresses[i[0]] = ''
while True:
    try:
        bals = {}
        for i in range(1, 6):
            print(i)
            bb = requests.post('https://api.omniexplorer.info/v2/address/addr/', data = {'addr': list(addresses.keys())[(i - 1) * 20:i * 20]}).json()
            for i in bb:
                if i != 'error':
                    bals[i] = bb[i]
            time.sleep(1)
        balances = {}
        for i in bals:
            for j in bals[i]['balance']:
                if j['symbol'] == 'SP31':
                    balances[i] = int(float(j['value']) / 10 ** 8)
        balsprev = {i.rstrip().split()[0]: balances[i.rstrip().split()[0]] - int(i.rstrip().split()[1]) for i in open('TetherBalances.txt', 'r')}
        for i in balsprev:
            if abs(balsprev[i]) >= 2000000:
                send('[' + (addresses[i] == '') * i + addresses[i] + '](https://www.omniexplorer.info/address/' + i + ') *' + '+' * (balsprev[i] >= 0) + '{0:,}'.format(balsprev[i]).replace(',', ' ') + ' USDT*\r\n#TetherTX')
        wr = open('TetherBalances.txt', 'w')
        for i in balances:
            wr.write(i + ' ' + str(balances[i]) + '\n')
        wr.close()
        time.sleep(5)
    except:
        bot.send_message(410821501, traceback.format_exc())
        time.sleep(1)
