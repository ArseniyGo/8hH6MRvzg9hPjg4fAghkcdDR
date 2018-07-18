import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
import telebot
bot = telebot.TeleBot("678797318:AAH6ImhT2dyJf1Y20-kBwFw1MSxezDLoSVg") 
graphu = []
graphb = []
o = open('graphs.txt', 'r')
for i in o:
    graphu.append(int(i.rstrip().split()[0]))
    graphb.append(int(i.rstrip().split()[1]))
while True:
    users = requests.get('https://www.bitmex.com/api/v1/chat/connected').json()
    graphu.append(users['users'])
    graphb.append(users['bots'])
    graphu, graphb = graphu[:2880], graphb[:2880]
    print(users)
    if len(graphu) >= 3:
        plt.subplot(2, 1, 1)
        plt.plot(graphu, color = 'g')
        plt.title('Current users: ' + str(graphu[-1]) + '\nCurrent bots: ' + str(graphb[-1]))

        plt.subplot(2, 1, 2)
        plt.plot(graphb, color = 'b')
        plt.savefig('graph.png', dpi = 100)
        plt.clf()
        if len(graphu) > 3:
            try:
                bot.delete_message('@cryptoscanning', int(open('mid.txt', 'r').readline().rstrip()))    
            except:
                time.sleep(0.1)
        m = bot.send_photo(chat_id = '@cryptoscanning', photo = open('graph.png', 'rb'))    
        o = open('mid.txt', 'w')
        o.write(str(m.message_id))
        o.close()
        o = open('graphs.txt', 'w')
        for i in range(len(graphu)):
            o.write(str(graphu[i]) + ' ' + str(graphb[i]) + '\n')
        o.close()
    time.sleep(30)
