import logging
from telegram import Update
from telegram.ext import CallbackContext

from utils import get_keyboard, get_user_emo


def greet_user(update: Update, context: CallbackContext):
    emo = get_user_emo(context.user_data)
    text = f'Привет!{emo}'
    logging.info(text)
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
