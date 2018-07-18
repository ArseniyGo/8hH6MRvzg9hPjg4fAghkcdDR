import requests
from bs4 import BeautifulSoup
import cfscrape
import time
import traceback
def send(m): #Функция для отправки сообщений
    print(m)
while True:
        if int(time.time()) % 60 == 0:
            bals = {}
            richlist = BeautifulSoup(cfscrape.create_scraper().get('https://wallet.tether.to/richlist').content, 'lxml').find('div', {'id': 'richlist'}).find('tbody').find_all('tr', {'class': 'tr-border'})
            for i in richlist:
                addr = i.find('td').find('a').text
                balancel = i.find('td', {'class':'balance'}).text.split(',')
                balance = ''
                for razr in balancel:
                    balance += razr
                balance = int(balance)
                bals[addr] = balance
            wr = open('TetherBalances.txt', 'w')
            for i in bals:
                wr.write(i + ' ' + str(bals[i]) + '\n')
            wr.close()
