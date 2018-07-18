import numpy as np
import requests
import matplotlib
matplotlib.use('Agg')  
import telebot
import matplotlib.pyplot as plt
bot = telebot.TeleBot('678797318:AAH6ImhT2dyJf1Y20-kBwFw1MSxezDLoSVg')
def ema(a, n):
    ema = [0] * len(a)
    for i in range(len(a)):
        ema[i] = (2 / (n + 1)) *  a[i] + ((n - 1) / (n + 1)) * ema[i - 1]
    return np.array([ema[3 * n]] * (3 * n) + ema[3 * n:])
def rsi(a, n):
    u = ema([max(a[i] - a[i - 1], 0) for i in range(1, len(a))], n)
    d = ema([max(a[i - 1] - a[i], 0) for i in range(1, len(a))], n)
    rs = [u[i] / d[i] for i in range(len(a) - 1)]
    rsi = [100 - (100 / (1 + i)) for i in rs]
    return rsi
def macd(a, s, l, b):
    s = ema(a, s)
    l = ema(a, l)
    b = ema(a, b)
    macd = [(s[i] - l[i]) for i in range(len(a))]
    signal = [(macd[i] * b[i]) for i in range(len(a))]
    diff = [(signal[i] - macd[i]) for i in range(len(a))]
    return [macd, signal, diff]
dt = requests.get('https://min-api.cryptocompare.com/data/histohour?fsym=BTC&tsym=USD&limit=1000&aggregate=4&e=Bitfinex').json()['Data']
data = {'low':np.array([], int), 'high': np.array([], int), 'close': np.array([], int), 'open': np.array([], int)}
for i in dt:
    data['low'] = np.append(data['low'], [i['low']])
    data['high'] = np.append(data['high'], [i['high']])  
    data['open'] = np.append(data['open'], [i['open']])  
    data['close'] = np.append(data['close'], [i['close']])
print(data['close'])
plt.subplot(2, 1, 1)
plt.plot(data['close'])
plt.subplot(2, 1, 2)
plt.plot(macd(data['close'], 12, 26, 9)[1])
plt.savefig('ema.png', dpi = 100)
plt.clf()
bot.send_photo(410821501, photo = open('ema.png', 'rb'))
