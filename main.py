import os, sys, logging
from pkgutil import get_data
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler

#load .env containing API Key
load_dotenv()

#Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

#setup token
API_KEY = os.environ.get('API_KEY')

SOLN, COST_A, PROFIT_A, COST_B, PROFIT_B, BUDGET = range(6)

var_list = []

def start(update: Update, context: CallbackContext) -> int:
    '''Starts the conversation and prompts user to pick a type of problem to solve'''
    reply_keyboard = [['Minimize', 'Maximize']]

    update.message.reply_text(f'''Hello {update.effective_user.first_name}, and welcome to lin_prog_bot; a bot that helps you make the right decisions using linear and integer programming.\n To start, use any of the buttons below for minimization/maximization problems''',
    reply_markup = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder='Minimize or Maximize?'
        ),
    )

    return SOLN

#HELP COMMAND
def help(update: Update, context: CallbackContext) -> int:
    '''Displays instructions and a list of commands'''
    user = update.message.from_user
    logger.info('User %s used the help command', user.first_name)
    update.message.reply_text(f'''
    Hello {user.first_name}. Here's a list of all the commands you can issue to the bot and their descriptions.
    ''')

    return ConversationHandler.END

def soln(update: Update, context: CallbackContext) -> int:
    '''Stores the value put in the keyboard by user to determine if it is a minimization or maximization problem
        Also asks for the cost of A'''
    try:
        soln = str(update.message.text)
        logger.info('User chose to solve a {} problem'.format(soln))
        var_list.append(soln)
        update.message.reply_text('What\'s the cost of item A?')
        return COST_A  
    except:
        update.message.reply_text('Sorry, you can only solve Minimization/Maximization Problems for now')
        sys.exit(1)  

def cost_a(update: Update, context: CallbackContext) -> int:
    '''Stores value of cost a and asks for the profit to be gotten from A'''
    #user = update.message.from_user
    update.message.reply_text('Interesting!')
    try:
        a_cost = float(update.message.text)
        var_list.append(a_cost)
        logger.info("Cost of item A is {}".format(a_cost))
        update.message.reply_text(
        'Now I\'d love to know how much profit you would gain from making/purchasing this item'
        )
    except:
        update.message.reply_text('Please put in a number')
        sys.exit(1)

    return PROFIT_A

def profit_a(update: Update, context: CallbackContext) -> int:
    '''Stores the profit of A and asks for the cost of item b'''
    #user = update.message.from_user
    update.message.reply_text('Noted! Now let\'s talk about item B')
    try:
        a_profit = float(update.message.text)
        var_list.append(a_profit)
        logger.info("Profit of item A is {}".format(a_profit))
        update.message.reply_text(
        'Well well, Now I need to know how much your other option costs'
        )
    except:
        update.message.reply_text(
            'Please put in a number; the quantity of gain you expect to get from buying item A \n'
            'It could be in numbers, grams, meters, litres, etc. The value of A.')
        #sys.exit(1)

    return COST_B

def cost_b(update: Update, context: CallbackContext) -> int:
    '''Stores the cost of B and asks for the profit/value of item B'''
    try:
        b_cost = float(update.message.text)
        var_list.append(b_cost)
        logger.info("Cost of item B is {}".format(update.message.text))
    except:
        update.message.reply_text(
            'Please put in a number; the amount it would take for you to buy/make item B'
            'It must not be monitary but it should be a number')
        sys.exit(1)
    update.message.reply_text('Noted! Now the value of Item B?')

    return PROFIT_B

def profit_b(update: Update, context: CallbackContext) -> int:
    '''Stores the profit of B and asks for the budget/total amount of resources to be expended'''
    try:
        b_profit = float(update.message.text)
        var_list.append(b_profit)
        logger.info("Profit of item B is {}".format(update.message.text))
        update.message.reply_text('Almost done... What\'s your budget?')
    except:
        update.message.reply_text(
            'Please put in a number; the quantity of gain you expect to get from buying item B \n'
            'It could be in numbers, grams, meters, litres, etc. The value of B.')
        sys.exit(1)

    return BUDGET

def budget(update: Update, contect: CallbackContext) -> int:
    '''Stores the total budget and calculates expressioin. Ends conversation handler'''
    try:
        budget = float(update.message.text)
        var_list.append(budget)
        logger.info("Profit of item B is {}".format(update.message.text))
    except:
        update.message.reply_text(
            'Please put in a number; the total amount of resources you\'re ready to spend overall'
            'It could be an amount of money, grams, meters, litres, etc. The value of B.')
        #sys.exit(1)
    cost_a = var_list[1]
    profit_a = var_list[2]
    cost_b = var_list[3]
    profit_b = var_list[4]
    budget = var_list[5]
    from lin_prog import lin_prog
    x, y, z = lin_prog(cost_a, cost_b, profit_a, profit_b, budget, soln=var_list[0])
    update.message.reply_text('Waku Waku, Nom Nom... One sec')
    update.message.reply_text(f'Number of item  A to buy: {x}\nNumber of Item B to buy: {y} \nTotal profit: {z}')

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    '''Cancels and ends the computation'''
    user = update.message.from_user
    logger.info('User %s canceled the computation.', user.first_name)
    update.message.reply_test('Bye {}. You sly fox you; you calculated it all yourself, didn\'t you?'.format(user.first_name))

    return ConversationHandler.END

def main() -> None:
    '''Run the bot'''
    #create Updater and pass in bot API key
    updater = Updater(API_KEY)
    
    #get dispatcher to register handlers
    dispatcher = updater.dispatcher

    #Add conversation handler with states SOLN, COST_A, PROFIT_A, COST_B, PROFIT_B, BUDGET
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states = {
            SOLN: [MessageHandler(Filters.text, soln)],
            COST_A: [MessageHandler(Filters.text, cost_a)],
            PROFIT_A: [MessageHandler(Filters.text, profit_a)],
            COST_B: [MessageHandler(Filters.text, cost_b)],
            PROFIT_B: [MessageHandler(Filters.text, profit_b)],
            BUDGET: [MessageHandler(Filters.text, budget)],
            #CALC: [MessageHandler(Filters.regex('/^[0-9]+$/'), calc)]
        },
        fallbacks=[CommandHandler('cancel', cancel), CommandHandler('help', help)],
    )

    dispatcher.add_handler(conv_handler)

    #connect to Telegram and wait for messages
    updater.start_polling()
    
    #keep programming running until interrupted
    updater.idle()

if __name__ == '__main__':
    main()

'''def calc(update: Update, context: CallbackContext) -> None:
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
        update.message.reply_text('You should type in exactly five numbers separates by commas and no spaces')
'''

