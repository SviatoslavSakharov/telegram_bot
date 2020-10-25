import telebot
from functions import get_crypto_data, buy_or_sell
import time

class Worker:
    to_work = False
    chat_id = ""

users = {}

#token = '1318199756:AAFCsYqmlV6o_-PwSvLPTQC7i6ekSqWvMnY'
bot = telebot.TeleBot(token)

@bot.message_handler(commands = ['chart'])
def command_handler(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('BTC 1H', 'ETH 1D') 
    msg = bot.reply_to(message, 'Choose a cryptocurrency', reply_markup=markup)
    bot.register_next_step_handler(msg, process_step)

@bot.message_handler(commands = ['start'])  
def starter(message):
    chat_id = message.chat.id
    eth_counter = 24
    users[chat_id] = True
    bot.send_message(chat_id, 'Start working')
    while True:
        if users[chat_id] == False:
            break
        if eth_counter == 24:
            btc_action, btc_stop, btc_img,  eth_action, eth_stop, eth_img = buy_or_sell(True)
            eth_counter = 0
        else :
            btc_action, btc_stop, btc_img,  eth_action, eth_stop, eth_img = buy_or_sell(False)
            eth_counter+=1

        if btc_action!='':
             bot.send_message(chat_id, 'Bitcoin:' + btc_action + '! With stop loss ' + str(btc_stop) + 'USDT' )
             bot.send_photo(chat_id, btc_img)
        
        if eth_action!='':
             bot.send_message(chat_id, 'Ethereum:' + eth_action + '! With stop loss ' + str(eth_stop) + 'USDT' )
             bot.send_photo(chat_id, eth_img) 
        
        time.sleep(3600)

@bot.message_handler(commands = ['stop'])  
def stoper(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Stop working')
    users[chat_id] = False

@bot.message_handler(commands = ['status'])  
def status(message):
    chat_id = message.chat.id
    if users[chat_id] : 
        bot.send_message(chat_id, 'Bot is working')
        print(users)
    else :
        bot.send_message(chat_id, 'Bot is not working')
        print(users)
    
def process_step(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Loading image...')
    if message.text=='BTC 1H':
        _, _, _, img = get_crypto_data('BTC/USDT', '1h', 90, 0)
        bot.send_photo(chat_id, img)
    else:
        _, _, _, img = get_crypto_data('ETH/USDT', '1d', 10, 0)
        bot.send_photo(chat_id, img)




    

bot.polling(timeout=60)
