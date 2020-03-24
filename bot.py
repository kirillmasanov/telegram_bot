import logging
from random import choice

from emoji import emojize
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters

from settings import PROXY, TOKEN, USER_EMOJI

log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler('bot.log', 'w', 'utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)


def greet_user(update: Update, context: CallbackContext):
    emo = get_user_emo(context.user_data)
    text = f'Привет!{emo}'
    logging.info(text)
    update.message.reply_text(text)


def send_pic(update: Update, context: CallbackContext):
    context.bot.send_photo(chat_id=update.message.chat_id,
                           photo='https://i.pinimg.com/736x/c7/12/43/c712434d2bf453f77513c0de26d3b4d1.jpg')


def talk_to_me(update: Update, context: CallbackContext):
    emo = get_user_emo(context.user_data)
    user_text = f'Привет, {update.message.chat.first_name}! Ты написал: {update.message.text}{emo}'
    logging.info(f'User: {update.message.chat.username}, Chat_id: {update.message.chat_id}, '
                 f'Message: {update.message.text}')
    update.message.reply_text(user_text)


def get_user_emo(user_data):
    """
    Проверяет, присвоен ли эмодзи пользователю
    :param user_data: context.user_data
    :return: user_data['emo']
    """
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(USER_EMOJI), use_aliases=True)
        return user_data['emo']


def main():
    mybot = Updater(TOKEN, request_kwargs=PROXY, use_context=True)

    logging.info('Бот запускается')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('pic', send_pic))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


main()
