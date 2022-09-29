import os
from dotenv import load_dotenv
import telebot
load_dotenv()

API_KEY = os.environ.get('API_KEY')
#API_KEY = '5790584247:AAEKgvTOGM_BWZ5m8FBNgGkaFnp6iXDjVXI'
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['greet'])

def greet(message):
    bot.reply_to(message, 'Why hello unto you too!!')

bot.infinity_polling()