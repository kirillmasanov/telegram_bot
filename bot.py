import logging
from random import choice

from emoji import emojize
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, RegexHandler

from settings import PROXY, TOKEN, USER_EMOJI

log = logging.getLogger()
log.setLevel(logging.INFO)
# handler = logging.FileHandler('bot.log', 'w', 'utf-8')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)


def greet_user(update: Update, context: CallbackContext):
    emo = get_user_emo(context.user_data)
    text = f'Привет!{emo}'
    logging.info(text)
    # contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    # location_button = KeyboardButton('Прислать координаты', request_location=True)
    # my_keyboard = ReplyKeyboardMarkup([
    #     ['Прислать котика', 'Сменить смайлик'],
    #     [contact_button, location_button]
    # ], resize_keyboard=True)
    update.message.reply_text(text, reply_markup=get_keyboard())


def send_pic(update: Update, context: CallbackContext):
    context.bot.send_photo(chat_id=update.message.chat_id,
                           photo='https://i.pinimg.com/736x/c7/12/43/c712434d2bf453f77513c0de26d3b4d1.jpg',
                           reply_markup=get_keyboard()
                           )


def talk_to_me(update: Update, context: CallbackContext):
    emo = get_user_emo(context.user_data)
    user_text = f'Привет, {update.message.chat.first_name}! Ты написал: {update.message.text}{emo}'
    logging.info(f'User: {update.message.chat.username}, Chat_id: {update.message.chat_id}, '
                 f'Message: {update.message.text}')
    update.message.reply_text(user_text, reply_markup=get_keyboard())


def get_contact(update: Update, context: CallbackContext):
    print(update.message.contact)
    update.message.reply_text(f'Готово: {get_user_emo(context.user_data)}', reply_markup=get_keyboard())


def get_location(update: Update, context: CallbackContext):
    print(update.message.location)
    update.message.reply_text(f'Готово: {get_user_emo(context.user_data)}', reply_markup=get_keyboard())


def change_user_emo(update: Update, context: CallbackContext):
    if 'emo' in context.user_data:
        del context.user_data['emo']
    emo = get_user_emo(context.user_data)
    update.message.reply_text(f'У вас новый смайлик - {emo}', reply_markup=get_keyboard())


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


def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать координаты', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
        ['Прислать котика', 'Сменить смайлик'],
        [contact_button, location_button]
    ], resize_keyboard=True)
    return my_keyboard

def main():
    mybot = Updater(TOKEN, request_kwargs=PROXY, use_context=True)

    logging.info('Бот запускается')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('pic', send_pic))

    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), send_pic))
    dp.add_handler(MessageHandler(Filters.regex('^(Сменить смайлик)$'), change_user_emo))

    dp.add_handler(MessageHandler(Filters.contact, get_contact))
    dp.add_handler(MessageHandler(Filters.location, get_location))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


main()
