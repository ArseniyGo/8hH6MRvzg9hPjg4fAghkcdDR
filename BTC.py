import requests
import telebot
import time
import traceback
bot = telebot.TeleBot("")
def send(m): #Функция для отправки сообщений
    global bot
    bot.send_message('-1001362959453', m, parse_mode = 'Markdown')
    bot.send_message('-1001180648345', m, parse_mode = "Markdown")
address = [i.rstrip().split() for i in open('Adresses.txt', 'r')] #Получение адресов из файла
addresses = {}
addmts = [i.rstrip() + '|' for i in open('MtGoxWallets.txt', 'r')]
summ = ''
for i in addmts:
    summ += i
addmt = summ[:-1]
for i in address:
    if len(i) == 2:
        addresses[i[0]] = i[1]
    else:
        addresses[i[0]] = ''
hashs = {i.rstrip().split()[0]: i.rstrip().split()[1] for i in open('hashs.txt', 'r')} #Получение хэшей последних обработанных транзакций
while True:
    try:
        mtbals = requests.get('https://blockchain.info/ru/balance?active=' + addmt).json()
        mtbal = 0
        for i in mtbals:
            print(i)
            mtbal += int(mtbals[i]['final_balance'] / 10 ** 8)
        if mtbal - int(open('MtBal.txt', 'r').readline()) >= 500:
            send('*-' + str(mtbal - int(open('MtBal.txt', 'r').readline())) + ' Mt. Gox Wallets' + '*' + '\r\n' +
                                    '[View wallets]' + '(https://www.cryptoground.com/mtgox-cold-wallet-monitor/)\r\n#MTGox')
        elif mtbal - int(open('MtBal.txt', 'r').readline()) <= -500:
            send('*+' + str(int(open('MtBal.txt', 'r').readline()) - mtbal) + ' Mt. Gox Wallets' + '*' + '\r\n' +
                                    '[View wallets]' + '(https://www.cryptoground.com/mtgox-cold-wallet-monitor/)\r\n#MTGox')
        mtgoxw = open('MtBal.txt', 'w')
        mtgoxw.write(str(mtbal))
        mtgoxw.close()
        for addr in addresses:
            txs = requests.get('https://blockchain.info/rawaddr/' + addr).json()['txs'] #Получение транзакций адреса
            start = -1
            for tx in range(len(txs)): #Определение количества необработанных транзакций
                if txs[tx]['hash'] == hashs[addr]:
                    start = tx
                    break
            if start == -1:
                start = len(txs)
            txs = txs[:start] #Получение только необработанных транзакций
            txs = txs[::-1]
            for tx in txs:
                if 'prev_out' in tx['inputs'][0].keys(): #Проверка на то, что биткоины отправлены, а не намайнены (Если есть кошелек, откуда были отправлены)
                    f = 1
                    for inp in tx['inputs']:
                        if 'prev_out' in inp and 'addr' in inp['prev_out'] and inp['prev_out']['addr'] == addr and f: #Определение того, отправил или получил адрес биткоины (Если есть в списке входов, то получил)
                            volume = 0
                            for inp in tx['inputs']:
                                if inp['prev_out']['addr'] == addr: #Определение того, сколько биткоинов отправил адрес
                                    volume += int(inp['prev_out']['value']) / 10 ** 8
                            w = {}
                            for out in tx['out']:
                                if 'addr' in out and out['addr'] == addr: #Вычитание биткоинов, отправленных самому себе
                                    volume -= int(out['value']) / 10 ** 8
                                if 'addr' in out and out['addr'] != addr:#Проверка на то, что 1. Адрес-получатель существует. 2. Адрес-получатель не совпадает с нашим адресом.
                                    if out['addr'] not in w.keys():
                                        w[out['addr']] = 0 #Словарь, содержащий инрформацию о получателях
                                    w[out['addr']] += int(out['value']) / 10 ** 8
                            for inp in tx['inputs']:
                                inp = inp['prev_out']
                                if inp['addr'] in w and inp['value'] >= 100000000:
                                    w[inp['addr']] -= int(inp['value']) / 10 ** 8
                            if (volume >= 500  and addr != '1Kr6QSydW9bFQG1mXiPNNu6WpJGmUa9i1g') or (volume >= 1000 and addr == '1Kr6QSydW9bFQG1mXiPNNu6WpJGmUa9i1g'): #Если отправлено от 500 биткоинов не с Bitfinex-Hot ли от 1000 с Bitfinex-Hot
                                print(addr)
                                print('out', round(volume))
                                m = '*From:* [' + addresses[addr] * (len(addresses[addr]) != 0) + addr * (len(addresses[addr]) == 0) + '](https://blockchain.info/address/' + addr + ')\r\n*Amount:* -' + str(int(volume)) + ' BTC\r\n\r\n'
                                cnt = 0
                                for out in w:
                                    if w[out] >= 100:
                                        cnt += 1
                                        if out in addresses and len(addresses[out]) != 0:
                                            m += 'To ' + str(cnt) + ': [' + addresses[out] + '](https://blockchain.info/address/' + str(out) + ')\r\nAmount ' + str(cnt) + ':* +' + str(int(w[out])) + ' BTC*\r\n'
                                        else:
                                            m += 'To ' + str(cnt) + ': [' + out + '](https://blockchain.info/address/' + str(out) + ')\r\nAmount ' + str(cnt) + ':* +' + str(int(w[out])) + ' BTC*\r\n'
                                m += '[View Transaction](https://blockchain.info/tx/' + tx['hash'] + ')\r\n#BTCTX'
                                send(m)
                            f = 0
                    if f: #Если биткоины получены
                        volume = 0
                        w = {}
                        for out in tx['out']: #Подсчет кол-ва полученных биткоинов.
                            if 'addr' in out and out['addr'] == addr and int(out['value']) > 100000000:
                                volume += int(out['value']) / 10 ** 8
                        for inp in tx['inputs']:
                            if 'prev_out' in inp:
                                inp = inp['prev_out']
                                if int(inp['value']) >= 100000000 and 'addr' in inp:
                                    if inp['addr'] not in w:
                                        w[inp['addr']] = 0
                                    w[inp['addr']] += int(inp['value']) / 10 ** 8 #Словарь, содержащий инрформацию о отправителях
                        for out in tx['out']:
                            if 'addr' in out and out['addr'] in w and int(out['value']) >= 100000000:
                                w[out['addr']] -= int(out['value']) / 10 ** 8
                        if (volume >= 500  and addr != '1Kr6QSydW9bFQG1mXiPNNu6WpJGmUa9i1g') or (volume >= 1000 and addr == '1Kr6QSydW9bFQG1mXiPNNu6WpJGmUa9i1g'):
                            print(addr)
                            print('in', round(volume))
                            m = '*To:* [' + addresses[addr] * (len(addresses[addr]) != 0) + addr * (len(addresses[addr]) == 0) + '](https://blockchain.info/address/' + addr + ')\r\n*Amount:* +' + str(int(volume)) + ' BTC\r\n\r\n'
                            cnt = 0
                            for out in w:
                                if w[out] >= 100:
                                    cnt += 1
                                    if out in addresses and len(addresses[out]) != 0:
                                        m += 'From ' + str(cnt) + ': [' + addresses[out] + '](https://blockchain.info/address/' + str(out) + ')\r\nAmount ' + str(cnt) + ':* -' + str(int(w[out])) + ' BTC*\r\n'
                                    else:
                                        m += 'From ' + str(cnt) + ': [' + out + '](https://blockchain.info/address/' + str(out) + ')\r\nAmount ' + str(cnt) + ':* -' + str(int(w[out])) + ' BTC*\r\n'
                            print(tx['hash'])
                            m += '[View Transaction](https://blockchain.info/tx/' + tx['hash'] + ')\r\n#BTCTX'
                            m = send(m)
                hashs[addr] = tx['hash']
                sssss = open('hashs.txt', 'w')
                for j in hashs:
                    sssss.write(j + ' ' + hashs[j] + '\n')
                sssss.close()
    except:
        bot.send_message(410821501, traceback.format_exc())
        time.sleep(10)
