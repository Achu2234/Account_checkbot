from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ( CommandHandler, Filters, MessageHandler, Updater)
from message import Editmessage, Sendmessage, logger
from Check.Altbalaji import altbalaji_helper
from Check.hotstar import hot_helper
from Check.voot import Voot_helper
from Miscellaneous.scope import pastebin, text_scraper, throwbin
import os


bot_token = os.environ.get('BOT_TOKEN')
#'1471969838:AAHaftsfpwcIUSGMUldTmdxDwemzPVAAzAI'
startmessage = [[
		InlineKeyboardButton(
			"Telegraph 📝",
			url='https://telegra.ph/Instructions-to-Use-This-Bot-12-25'
		),
        InlineKeyboardButton(
			"DEV 👷🏻",
			url='https://t.me/pseudo_monk'
		)
        ]]

def combos_spilt(combos):
    split = combos.split('\n')
    return split


def start(update, context):
    info = update.effective_user
    print(info)
    chat_id = info.id
    userid= info['username']
    text = f'Welcome @{userid}, To Account Check Bot, to know more use /help or read the telegraph below. This bot is provided for educational use only, any misuse then you should be responsible'
    Sendmessage(chat_id, text, reply_markup=InlineKeyboardMarkup(startmessage))
    return

def help(update, context):
    chat_id = update.message.chat_id
    text = "<b>Available Sites:\n!alt~space~combo* - to check Altbalaji accounts\n!hot~space~combo* - to check Hotstar accounts\n!voo~space~combo* - to check Voot accounts\nMiscellaneous:-\n!pst~space~title|text - to paste text on Throwbin.io and get paste link</b>\n\n*combo here means Email:password combination,':' is important."
    markup = [[InlineKeyboardButton(
			"Developer",
			url='https://t.me/pseudo_monk'
		)]]
    Sendmessage(chat_id, text, reply_markup= InlineKeyboardMarkup(markup))

def duty(update, context):
    chat_id = update.message.chat_id
    text =  update.message.text.split(' ', 1)
    if text[0] == '!alt':
        if '\n' in text[1]:
            simple = combos_spilt(text[1])
            for i in simple:
                altbalaji_helper(chat_id, i)
            Sendmessage(chat_id, 'Completed')
        else:
            altbalaji_helper(chat_id, text[1])
    elif text[0] == '!voo':
        if '\n' in text[1]:
            simple = combos_spilt(text[1])
            for i in simple:
                Voot_helper(chat_id, i)
            Sendmessage(chat_id, 'Completed')
        else:
            Voot_helper(chat_id, text[1])
    elif text[0] == '!hot':
        if '\n' in text[1]:
            simple = combos_spilt(text[1])
            for i in simple:
                hot_helper(chat_id, i)
            Sendmessage(chat_id, 'Completed')
        else:
            hot_helper(chat_id, text[1])
    elif text[0] == '!pst':
            try:
                throwbin(chat_id, text[1])
            except IndexError:
                Sendmessage(chat_id, "<i>Somethings wrong with your format!</i>")
    else:
        logger.info('Unknown Command')


def scraperdfnc(update, context):
    msg = update.message.text
    status_msg = update.message
    chat_id = status_msg.chat_id
    try:
        if 'pastebin' in msg:
            link = msg.split(' ')[1]
            pastebin(chat_id,link)
        else:
            scrape_text = status_msg['reply_to_message']['text']
            text_scraper(chat_id, scrape_text)
    except:
        Sendmessage(chat_id, 'Only Supports pastebin, please check if you send paste bin link')

def main():
    updater = Updater(
        bot_token,
        use_context=True
    )
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, duty))
    dp.add_handler(CommandHandler("scrape", scraperdfnc))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    logger.info("Bot Started!!!")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()