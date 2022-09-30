import os, sys
from pkgutil import get_data
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

load_dotenv()

#setup token
API_KEY = os.environ.get('API_KEY')
updater = Updater(API_KEY, use_context=True)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}, and welcome to lin_prog_bot; a bot that helps you make the right decisions using linear and integer programming')

#make hello command run the helo function
updater.dispatcher.add_handler(CommandHandler('start', start))

#HELP COMMAND
def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'''
    Here's a list of all the commands you can issue to the bot and thir descriptions.
    ''')

updater.dispatcher.add_handler(CommandHandler('help', help))

def lin_programming(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'You have decided to solve a Linear programming problem. What is the cost of A?')

updater.dispatcher.add_handler(CommandHandler('lin_programming', lin_programming))

def calc(update: Update, context: CallbackContext) -> None:
    vals = update.message.text.split(',')
    if len(vals) == 5:
        try:
            cost_a = float(vals[0])
            profit_a = float(vals[1])
            cost_b = float(vals[2])
            profit_b = float(vals[3])
            budget = float(vals[4])
        except:
            update.message.reply_text('Pleaase type in numbers only. Try dey pay attention!!!')
            sys.exit(1)
        from lin_prog import lin_prog
        x, y, z = lin_prog(cost_a, cost_b, profit_a, profit_b, budget, soln="Maximize")
        update.message.reply_text(f'Number of item  A to buy: {x}\n number of Item B to buy: {y} \n Total profit: {z}')
    else:
        update.message.reply_text('You should type in exactly five numbers separates by commas and no space')

updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, calc))

#connect to Telegram and wait for messages
updater.start_polling()

#keep programming running until interrupted
updater.idle()