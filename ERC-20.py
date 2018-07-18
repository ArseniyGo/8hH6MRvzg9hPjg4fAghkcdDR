import requests
import time
import traceback
import telebot
bot = telebot.TeleBot("592804892:AAGPnvbvCRRlMv0AuyD_F0THfk7UMBtgU64")
def send(m): #Функция для отправки сообщений
    global bot
    bot.send_message('-1001362959453', m, parse_mode = 'Markdown')
    bot.send_message('-1001180648345', m, parse_mode = "Markdown")
txids = []
addresses = {i.rstrip().split()[0]: i.rstrip().split()[1] for i in open('ERC-20Addresses.txt', 'r')}
while True:
    try:
        BTCprice = float(requests.get('https://api.coinmarketcap.com/v2/ticker/1/').json()['data']['quotes']['USD']['price'])
        prices = {i['name']: float(i['price']['rate']) / BTCprice for i in requests.get('https://api.ethplorer.io/getTop?apiKey=ethplorer.widget&domain=https%3A%2F%2Fethplorer.io%2Ftop%3Ffrom%3Detop&limit=300&criteria=cap').json()['tokens']}
        if len(txids) >= 1000:
            txids = txids[-1000:]
        txs = requests.get('https://api.ethplorer.io/getTokenHistory?apiKey=ethplorer.widget&type=transfer&domain=https://ethplorer.io/last&limit=1000').json()['operations']
        i = 0
        while i != len(txs) - 1:
            if txs[i]['transactionHash'] == txs[i + 1]['transactionHash']:
                txs.pop(i)
            else:
                 i += 1
        for i in range(len(txs)):
            if txs[i]['transactionHash'] in txids:
                txs = txs[:i]
                break
            else:
                txids.append(txs[i]['transactionHash'])
        for i in txs:
            if i['tokenInfo'] and 'decimals' in i['tokenInfo'] and 'name' in i['tokenInfo'] and i['tokenInfo']['name'] in prices and 'value' in i:
                amount = int(i['value']) // 10 ** int(i['tokenInfo']['decimals'])
                symbol = i['tokenInfo']['symbol']
                price = int(amount * prices[i['tokenInfo']['name']])
                fromw = i['from']
                to = i['to']
                if fromw in addresses:
                    fromw = addresses[fromw]
                if to in addresses:
                    to = addresses[to]
                if fromw == 'Binance-Cold' and to == 'Binance-Hot':
                    bintok = [line.rstrip().split() for line in open('binancetokens.txt', 'r')]
                    bintok[1].append(symbol)
                    bintok[0].append('\n')
                    op = open('binancetokens.txt', 'w')
                    print(*bintok[0], *bintok[1], file = op)
                    op.close()
                    send('*Coin*: #' + symbol + '\r\n' + 
                    '[Binance-Cold](https://etherscan.io/address/' + i['from'] + ')➡️[Binance-Hot](https://etherscan.io/address/' + i['to'] + ')\r\n' +
                    '[View Transaction](https://etherscan.io/tx/' + i['transactionHash'] + ')\r\n' + 
                    '#ERC20TX #BinanceTX')
                if fromw == 'Binance-Hot' and to == 'Binance-Cold':
                    bintok = [line.rstrip().split() for line in open('binancetokens.txt', 'r')]
                    bintok[0].append(symbol)
                    bintok[0].append('\n')
                    op = open('binancetokens.txt', 'w')
                    print(*bintok[0], *bintok[1], file = op)
                    op.close()
                    send('*Coin*: #' + symbol + '\r\n' + 
                    '[Binance-Hot](https://etherscan.io/address/' + i['from'] + ')➡️[Binance-Cold](https://etherscan.io/address/' + i['to'] + ')\r\n' +
                    '[View Transaction](https://etherscan.io/tx/' + i['transactionHash'] + ')\r\n' + 
                    '#ERC20TX #BinanceTX')
                if price >= 100 and len(symbol) and i['tokenInfo'] and i['tokenInfo']['price']:
                    if not to == fromw == 'Binance-Hot':
                        send('*Coin:* #' + symbol + '\r\n' + 
                        '*From:* [' + fromw + '](https://etherscan.io/address/' + i['from'] + ')\r\n' + 
                        '*To:* [' + to + '](https://etherscan.io/address/' + i['to'] + ')\r\n' + 
                        '*Amount:* ' + '{0:,}'.format(amount).replace(',', ' ') + ' *~' + str(price) + ' BTC*\r\n' + '[View Transaction](https://etherscan.io/tx/' + i['transactionHash'] + ')\r\n' +
                        '#ERC20TX')
        time.sleep(5)
    except:
        bot.send_message(410821501, traceback.format_exc())
        time.sleep(1)
