# keyboards.py
from telebot import types

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = ['Узнать время', 'Узнать дату', 'Узнать погоду', 'Помощь', 'Конвертировать валюту']
    for button in buttons:
        markup.add(types.KeyboardButton(button))
    return markup

def get_weather_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = ['Погода сейчас', 'Погода сегодня']
    for button in buttons:
        markup.add(types.KeyboardButton(button))
    return markup