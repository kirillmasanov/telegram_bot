from emoji import emojize
from telegram import KeyboardButton, ReplyKeyboardMarkup

from random import choice

from settings import USER_EMOJI


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
