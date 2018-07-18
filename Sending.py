import requests
import telebot
import time
import traceback
bot = telebot.TeleBot("592804892:AAGPnvbvCRRlMv0AuyD_F0THfk7UMBtgU64")
address = [i.rstrip().split() for i in open('Adresses.txt', 'r')] #Получение адресов из файла
addresses = {}
for i in address:
    if len(i) == 2:
        addresses[i[0]] = i[1]
    else:
        addresses[i[0]] = ''
while True:
    try:
        s = {float(i.rstrip().split()[0]): [int(i.rstrip().split()[1]), int(i.rstrip().split()[2]), i.rstrip().split()[3:]] for i in open('Sendings.txt', 'r')}
        i = 0
        while i < len(s):
            if int(time.time()) - s[list(s.keys())[i]][1] >= 7200:
                s.pop(list(s.keys())[i])
            else:
                i += 1
        hashs = {i.rstrip().split()[0]: i.rstrip().split()[1] for i in open('Sendinghashs.txt', 'r')}
        for addr in addresses:
            txs = requests.get('https://chain.api.btc.com/v3/address/' + addr + '/tx').json()['data']['list'] #Получение транзакций адреса
            start = len(txs)
            for tx in range(len(txs)): #Определение количества необработанных транзакций
                if txs[tx]['hash'] == hashs[addr]:
                    start = tx
                    break
            txs = txs[:start]
            txs = txs[::-1]
            for tx in txs:
                hashs[addr] = tx['hash']
                tx = tx['outputs']
                for out in tx:
                    if addr in out['addresses']:
                        if out['value'] / 10 ** 8 not in s and out['value'] / 10 ** 8 < 0.001:
                            s[out['value'] / 10 ** 8] = [0, int(time.time()), []]
                        if out['value'] / 10 ** 8 < 0.001 and addr not in s[out['value'] / 10 ** 8][2]:
                            s[out['value'] / 10 ** 8][0] += 1
                            s[out['value'] / 10 ** 8][2].append(addr)
            time.sleep(1)
        msgs = {float(i.rstrip().split()[0]): [[i.rstrip().split()[1], i.rstrip().split()[2]], int(i.rstrip().split()[3])] for i in open('msgs.txt', 'r')}
        i = 0
        while i < len(msgs):
            if list(msgs.keys())[i] not in s:
                msgs.pop(list(msgs.keys())[i])
            else:
                i += 1
        for se in s:
            if s[se][0] >= 4 and (se not in msgs or s[se][0] - msgs[se][1] >= 1):
                c = s[se][0]
                m = '#Рассылка *' + '{0:.8f}'.format(se) + ' BTC на ' + str(c)
                if 4 >= c % 10 >= 2 and (c < 10 or c > 20):
                    m += ' кошелька*\r\n*Получатели:*\r\n'
                elif 20 >= c >= 10 or c % 10 != 1:
                    m += ' кошельков*\r\n*Получатели:*\r\n'
                elif c % 10 == 1:
                    m += ' кошелек*\r\n*Получатели:*\r\n'
                for i in s[se][2]:
                    if len(addresses[i]):
                        m += '[' + addresses[i] + '](https://www.blockchain.com/ru/btc/address/' + i + ')\r\n'
                    else:
                        m += '[' + i + '](https://www.blockchain.com/ru/btc/address/' + i + ')\r\n'
                if se in msgs:
                    msgs[se][1] = s[se][0]
                    bot.edit_message_text(chat_id = '-1001362959453', message_id = int(msgs[se][0][0]), text = m, parse_mode = "Markdown")
                    bot.edit_message_text(chat_id = '-1001180648345', message_id = int(msgs[se][0][1]), text = m, parse_mode = "Markdown")
                    time.sleep(1)
                else:
                    m1 = bot.send_message('-1001362959453', m, parse_mode = "Markdown")
                    m2 = bot.send_message('-1001180648345', m, parse_mode = "Markdown")
                    msgs[se] = [[str(m1.message_id), str(m2.message_id)], str(s[se][0])]
        op = open('msgs.txt', 'w')
        for m in msgs:
            op.write('{0:.8f}'.format(m) + ' ' + str(msgs[m][0][0]) + ' ' + str(msgs[m][0][1]) + ' ' + str(msgs[m][1]) + '\n')
        op.close()
        op = open('Sendings.txt', 'w')
        for se in s:
            op.write('{0:.8f}'.format(se) + ' ' + str(s[se][0]) + ' ' + str(s[se][1]) + ' ')
            for i in s[se][2]:
                op.write(i + ' ')
            op.write('\n')
        op.close()
        h = open('Sendinghashs.txt', 'w')
        for i in hashs:
            h.write(i + ' ' + hashs[i] + '\n')
        h.close()
    except:
        time.sleep(1)
        bot.send_message(410821501, traceback.format_exc())
        time.sleep(5)
