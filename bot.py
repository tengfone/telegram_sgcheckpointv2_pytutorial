from telegram import ParseMode, ReplyKeyboardMarkup, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler, \
    ConversationHandler
import logging, os, sys, requests
from functools import wraps

# logger
logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# global variable
mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
api_key = os.getenv("API_KEY")
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# the different type of states
MENU, CHOOSING_CAMERA, CHOOSING_RATES, CALCULATE_SG_MY, CALCULATE_MY_SG = range(5)

# different type of custom keyboard
menu_reply_keyboard = [['Camera 📷'], ['Rates 💰'], ['Info ℹ️']]
camera_reply_keyboard = [['Woodlands', 'Tuas'], ['Back']]
rates_reply_keyboard = [['🇸🇬➡️🇲🇾', '🇲🇾➡️🇸🇬'], ['Back']]

# options to run
if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("Error, Ensure Environment Variable is set.")
    sys.exit(1)


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context, *args, **kwargs)

    return command_func


@send_typing_action
def start(update, context):
    """
    This is  what happens when you type /start. It displays a message with a custom keyboard and returns to the state MENU
    """
    update.message.reply_text(
        "Going to 🇲🇾 or coming back 🇸🇬 \nCome, I let you see if got jam anot. \nOr you want exchange rate also can.",
        reply_markup=ReplyKeyboardMarkup(menu_reply_keyboard, one_time_keyboard=True))

    return MENU


@send_typing_action
def camera(update, context):
    """
    Replys with a text and custom keyboard, return state CHOOSING_CAMERA
    """
    update.message.reply_text("Woodlands or Tuas?",
                              reply_markup=ReplyKeyboardMarkup(camera_reply_keyboard, one_time_keyboard=True))
    return CHOOSING_CAMERA


@send_typing_action
def woodlands(update, context):
    response = requests.get('https://api.data.gov.sg/v1/transport/traffic-images').json()
    lta_raw_data = response['items'][0]
    # lta_current_time_stamp = lta_raw_data['timestamp']
    lta_data = lta_raw_data['cameras']  # a list
    for each_dict in lta_data:
        if '2701' in each_dict.values():  # Woodlands Causeway (Towards Johor)
            woodlands_johor = each_dict
        if '2702' in each_dict.values():  # Woodlands Checkpoint (Towards BKE)
            woodlands_bke = each_dict

    woodlands_johor_image = woodlands_johor['image']
    woodlands_johor_timestamp = woodlands_johor['timestamp'].replace('T', ' ')[:-6]
    update.message.reply_photo(woodlands_johor_image, caption=(
            'Woodlands Causeway (Towards Johor)\nLast Updated at ' + woodlands_johor_timestamp))

    woodlands_bke_image = woodlands_bke['image']
    woodlands_bke_timestamp = woodlands_bke['timestamp'].replace('T', ' ')[:-6]
    update.message.reply_photo(woodlands_bke_image, caption=(
            'Woodlands Checkpoint (Towards BKE)\nLast Updated at ' + woodlands_bke_timestamp),
                               reply_markup=ReplyKeyboardMarkup(menu_reply_keyboard, one_time_keyboard=True))

    return MENU


@send_typing_action
def info(update, context):
    useful_info = '<b>Contacting the Singapore Embassy in Malaysia</b>\n\n<i>In Johor Bahru</i>' \
                  '\n\nAddress: Suite 35.02, Level 35, Johor Bahru City Square Office Tower 106-108, ' \
                  'Jalan Wong Ah Fook, 80000\nTel: +607 226 5012 OR +60 19 791 1166 (Emergencies)\nE-Mail:' \
                  ' singcon_jhb@mfa.sg\nOpen from 8.30 am to 1 pm, and 2 pm to 5 pm on weekdays. Closed on ' \
                  'weekends and public holidays (Emergency line still operates).\n\n\n<i>In Kuala Lumpur:</i>' \
                  '\n\nAddress: 209 Jalan Tun Razak, Kuala Lumpur, 50400\nTel: +6(03) 2161-6277 +60 16 661-0400 ' \
                  '(Emergencies)\nEmail: singhc_kul@mfa.sg\nOpen from 8.30 am to 5 pm on weekdays, closed on ' \
                  'weekends and public holidays (emergency line still operates).'
    update.message.reply_text(useful_info, parse_mode=ParseMode.HTML,
                              reply_markup=ReplyKeyboardMarkup(menu_reply_keyboard, one_time_keyboard=True))

    return MENU


@send_typing_action
def tuas(update, context):
    response = requests.get('https://api.data.gov.sg/v1/transport/traffic-images').json()
    lta_raw_data = response['items'][0]
    lta_data = lta_raw_data['cameras']
    for each_dict in lta_data:
        if '4703' in each_dict.values():  # Second Link at Tuas
            tuas_link = each_dict
        if '4713' in each_dict.values():  # Tuas Checkpoint
            tuas_checkpoint = each_dict

    tuas_link_image = tuas_link['image']
    tuas_link_timestamp = tuas_link['timestamp'].replace('T', ' ')[:-6]
    update.message.reply_photo(photo=tuas_link_image,
                               caption=('Second Link at Tuas\nLast Updated at ' + tuas_link_timestamp))

    tuas_checkpoint_image = tuas_checkpoint['image']
    tuas_checkpoint_timestamp = tuas_checkpoint['timestamp'].replace('T', ' ')[:-6]
    update.message.reply_photo(tuas_checkpoint_image,
                               caption=('Tuas Checkpoint\nLast Updated at ' + tuas_checkpoint_timestamp),
                               reply_markup=ReplyKeyboardMarkup(menu_reply_keyboard, one_time_keyboard=True))
    return MENU


@send_typing_action
def rates(update, context):
    try:
        website = 'https://free.currconv.com/api/v7/convert?q=SGD_MYR,MYR_SGD&compact=ultra&apiKey={}'
        currency = requests.get(website.format(api_key)).json()
        sgd_to_myr = currency.get('SGD_MYR')
        myr_to_sgd = currency.get('MYR_SGD')
        context.user_data['rates'] = currency
        update.message.reply_text(
            'The current exchange rate from SGD to MYR is ' + str(sgd_to_myr) + ' and from MYR to SGD is ' + str(
                myr_to_sgd) + '\nNeed to calculate? Press one of the options below.',
            reply_markup=ReplyKeyboardMarkup(rates_reply_keyboard, one_time_keyboard=True))
        return CHOOSING_RATES
    except:  # bad practice but no choice as I do not know what is the error handling function
        update.message.reply_text(
            "Seems like my exchange rate free API have hit more than 200 requests. Paiseh ah, I no money buy the paid "
            "version. Maybe try my exchange rate function later.",
            reply_markup=ReplyKeyboardMarkup(menu_reply_keyboard, one_time_keyboard=True))
        return MENU


@send_typing_action
def ask_rates_sg_my(update, context):
    update.message.reply_text("The amount of SGD you want to convert to RM?")
    return CALCULATE_SG_MY


@send_typing_action
def ask_rates_my_sg(update, context):
    update.message.reply_text("The amount of RM you want to convert to SGD?")
    return CALCULATE_MY_SG


@send_typing_action
def calc_rates_sg_my(update, context):
    text = update.message.text
    text = text.strip().replace(' ', '').replace(',', '.')
    try:
        out_text = text
        text = float(text)
        money_data = context.user_data
        money_data = money_data['rates']
        sgd_myr = money_data.get('SGD_MYR')
        output = round(text * sgd_myr, 2)
        update.message.reply_text("Your S${} converted to {}RM".format(out_text, output),
                                  reply_markup=ReplyKeyboardMarkup(menu_reply_keyboard, one_time_keyboard=True))
        return MENU
    except ValueError:  # this is a good example of error handling
        update.message.reply_text("Huh...why your money got alphabets one ah? Try again!")
        return CALCULATE_SG_MY


@send_typing_action
def calc_rates_my_sg(update, context):
    text = update.message.text
    text = text.strip().replace(' ', '').replace(',', '.')
    try:
        out_text = text
        text = float(text)
        money_data = context.user_data
        money_data = money_data['rates']
        myr_sgd = money_data.get('MYR_SGD')
        output = round(text * myr_sgd, 2)
        update.message.reply_text("Your {}RM converted to S${}".format(out_text, output),
                                  reply_markup=ReplyKeyboardMarkup(menu_reply_keyboard, one_time_keyboard=True))
        return MENU
    except ValueError:
        update.message.reply_text("Huh...why your money got alphabets one ah? Try again!")
        return CALCULATE_MY_SG


@send_typing_action
def aboutMe(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="This bot is written in Python by @tengfone, if you are interested in developing "
                                  "your own, check out my tutorial! \n https://github.com/tengfone?tab=repositories")


@send_typing_action
def unknownCommand(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Invalid command. This bot not so smart yet, click /start if unsure")


@send_typing_action
def unknownText(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Invalid text. This bot not so smart yet, click /start if unsure")


if __name__ == '__main__':
    logger.info("Starting bot")

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [MessageHandler(Filters.regex('^Camera 📷$'), camera, pass_user_data=True),
                   MessageHandler(Filters.regex('^Rates 💰$'), rates, pass_user_data=True),
                   MessageHandler(Filters.regex('^Info ℹ️'), info, pass_chat_data=True)],
            CHOOSING_CAMERA: [MessageHandler(Filters.regex('^Woodlands$'), woodlands, pass_user_data=True),
                              MessageHandler(Filters.regex('^Tuas$'), tuas, pass_user_data=True)],
            CHOOSING_RATES: [MessageHandler(Filters.regex('^🇸🇬➡️🇲🇾$'), ask_rates_sg_my, pass_user_data=True),
                             MessageHandler(Filters.regex('^🇲🇾➡️🇸🇬$'), ask_rates_my_sg, pass_user_data=True)],
            CALCULATE_SG_MY: [MessageHandler(Filters.text, calc_rates_sg_my, pass_user_data=True)],
            CALCULATE_MY_SG: [MessageHandler(Filters.text, calc_rates_my_sg, pass_user_data=True)],
        },
        fallbacks=[MessageHandler(Filters.regex('^Back$'), start, pass_user_data=True)],
        allow_reentry=True  # this line is important as it allows the user to talk to the bot anytime
    )
    dispatcher.add_handler(conv_handler)

    # about me bot
    aboutMe_handler = CommandHandler('about', aboutMe)
    dispatcher.add_handler(aboutMe_handler)

    # unknown commands, must put at the end
    unknown_handler = MessageHandler(Filters.command, unknownCommand)
    dispatcher.add_handler(unknown_handler)

    # unknown messages, must put at the end
    unknown_handler = MessageHandler(Filters.text, unknownText)
    dispatcher.add_handler(unknown_handler)

    run(updater)
