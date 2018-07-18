import re
import time
import requests
from bs4 import BeautifulSoup
from lxml import html
p = 1
s = 0
while True:
    p = 1
    f = 0
    txs = [[i.find_all('span', {'class': 'address-tag'}), int(re.sub(',', '', str(i.find_all('td')[-2]).split('<')[1].split('>')[1].split('Ether')[0]))] for i in BeautifulSoup(requests.get('https://etherscan.io/txs?ps=100&p=' + str(p)).text, 'lxml').find
('tbody').find_all('tr')]
    while s and not f:
        p += 1
        txs.extend([[i.find_all('span', {'class': 'address-tag'}), int(re.sub(',', '', str(i.find_all('td')[-2]).split('<')[1].split('>')[1].split('Ether')[0]))] for i in BeautifulSoup(requests.get('https://etherscan.io/txs?ps=100&p=' + str(p)).text, 'lxml').find('tbody').find_all('tr')])
        for i in range(len(txs)):
            if txs[i][0][0] == ltx:
                f = 1
                print(1)
                txs = txs[:i]
                break
        time.sleep(1)
    if len(txs):
        s = 1
        ltx = txs[0][0][0]
        i = 0
        while i < len(txs):
            if len(txs[i][0]) < 3 or txs[i][1] < 1000:
                txs.pop(i)
            else:
                i += 1
        txs = [[i[0][0].find('a').get('href')[4:], i[0][1].find('a').get('href')[9:], i[0][2].find('a').get('href')[9:], i[1]] for i in txs]
        print(txs)
