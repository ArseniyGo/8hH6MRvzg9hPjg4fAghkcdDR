import telebot
import time
bot = telebot.TeleBot("569705808:AAGZ-dEfUdPugzl-dUPi2ZmFt_6PcB4Adso")
@bot.message_handler(content_types=['text'])
def action(m):
    lines = m.text.split('\n')
    print(lines)
    op = open(lines[0], 'w')
    op.write(lines[0])
    for i in lines[1:]:
        op.write(i + '\n')
    op.close()
while True:
    try:
        bot.polling(none_stop=True)
    except:
        time.sleep(1)
