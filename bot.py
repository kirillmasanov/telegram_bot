from pprint import pprint

from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
import logging

from settings import PROXY, TOKEN

log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler('bot.log', 'w', 'utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)


def greet_user(update: Update, context: CallbackContext):
    text = 'Вызван /start'
    logging.info(text)
    update.message.reply_text(text)


def talk_to_me(update: Update, context: CallbackContext):
    user_text = f'Привет, {update.message.chat.first_name}! Ты написал: {update.message.text}'
    logging.info(f'User: {update.message.chat.username}, Chat_id: {update.message.chat_id}, '
                 f'Message: {update.message.text}')
    update.message.reply_text(user_text)


def main():
    mybot = Updater(TOKEN, request_kwargs=PROXY, use_context=True)

    logging.info('Бот запускается')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


main()
