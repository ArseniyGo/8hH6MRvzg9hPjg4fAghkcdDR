import requests                                                                                                                                  
import matplotlib                                                                                                                                
matplotlib.use('Agg')                                                                                                                            
import matplotlib.pyplot as plt                                                                                                                  
import time                                                                                                                                      
import telebot                                                                                                                                   
bot = telebot.TeleBot("678797318:AAH6ImhT2dyJf1Y20-kBwFw1MSxezDLoSVg")                                                                           
capbtc = []                                                                                                                                      
capusd = []
capbtch = []
capusdh = []
o = open('caph.txt', 'r')
for i in o:
     capbtch.append(int(float(i.rstrip().split()[0])))
     capusdh.append(int(float(i.rstrip().split()[1])))
caps = requests.get('https://api.coinmarketcap.com/v2/global/?convert=BTC').json()                                                           
capbtch.append(int(caps['data']['quotes']['BTC']['total_market_cap'] * (1 - caps['data']['bitcoin_percentage_of_market_cap'] / 100)))        
capusdh.append(int(caps['data']['quotes']['USD']['total_market_cap'] * (1 - caps['data']['bitcoin_percentage_of_market_cap'] / 100)))
plt.subplot(2, 1, 1)                                                                                                                         
plt.plot(capbtch, color = 'y')                                                                                                                
plt.title('Hour\nCurrent altcoins BTC cap: ' + str(capbtch[-1]) + '\nCurrent altcoins USD cap: ' + str(capusdh[-1]))                         
plt.subplot(2, 1, 2)                                                                                                                         
plt.plot(capusdh, color = 'g')                                                                                                                
plt.savefig('caph.png', dpi = 100)                                                                                                            
plt.clf() 
if len(capusdh) > 3:                 
    try:                                                                                                                                     
        bot.delete_message('@cryptoscanning', int(open('mids1.txt', 'r').readline().rstrip()))                                                
    except:                                                                                                                                  
        time.sleep(0.1)                                                                                                                      
    m = bot.send_photo(chat_id = '@cryptoscanning', photo = open('caph.png', 'rb'))                                                           
    o = open('mids1.txt', 'w')                                                                                                                
    o.write(str(m.message_id))                                                                                                                                          
    o.close()                                                                                                                                
o = open('caph.txt', 'w')                                                                                                                    
for i in range(len(capbtch)):                                                                                                                 
    o.write(str(capbtch[i]) + ' ' + str(capusdh[i]) + '\n')                                                                                    
o.close()     
o = open('cap.txt', 'r')                                                                                                                      
for i in o:                                                                                                    
    capbtc.append(int(float(i.rstrip().split()[0])))                                                                               
    capusd.append(int(float(i.rstrip().split()[1])))                                                                                                  
while True:
    caps = requests.get('https://api.coinmarketcap.com/v2/global/?convert=BTC').json()  
    capbtc.append(int(caps['data']['quotes']['BTC']['total_market_cap'] * (1 - caps['data']['bitcoin_percentage_of_market_cap'] / 100)))
    capusd.append(int(caps['data']['quotes']['USD']['total_market_cap'] * (1 - caps['data']['bitcoin_percentage_of_market_cap'] / 100)))
    plt.subplot(2, 1, 1)                                                                                                                     
    plt.plot(capbtc, color = 'y')  
    plt.title('Minute\nCurrent altcoins BTC cap: ' + str(capbtc[-1]) + '\nCurrent altcoins USD cap: ' + str(capusd[-1]))            
    plt.subplot(2, 1, 2)
    plt.plot(capusd, color = 'g')
    plt.savefig('cap.png', dpi = 100)                                                                                                      
    plt.clf()                                                                                                                                
    if len(capusd) > 3:                                                                                                                      
        try:                                                                                                                                 
            bot.delete_message('@cryptoscanning', int(open('mids.txt', 'r').readline().rstrip()))                                             
        except:                                                                                                                              
            time.sleep(0.1)                                                                                                                  
        m = bot.send_photo(chat_id = '@cryptoscanning', photo = open('cap.png', 'rb'))                                                         
        o = open('mids.txt', 'w')
        o.write(str(m.message_id))                                                                                                               
        o.close()
    o = open('cap.txt', 'w')    
    for i in range(len(capbtc)):
        o.write(str(capbtc[i]) + ' ' + str(capusd[i]) + '\n')
    o.close()
    time.sleep(600)         
