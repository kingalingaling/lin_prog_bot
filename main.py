import os
from dotenv import load_dotenv
import telebot
load_dotenv()

API_KEY = os.environ.get('API_KEY')
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['greet'])

def greet(message):
    bot.reply_to(message, 'Why hello unto you too!!')

bot.infinity_polling()
