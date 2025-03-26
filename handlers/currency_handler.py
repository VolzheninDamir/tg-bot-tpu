# handlers/currency_handler.py
from telebot import types
from services.currency_service import convert_currency
from keyboards import get_main_keyboard
from config import CURRENCIES

def setup_currency_handlers(bot, user_data):
    @bot.message_handler(func=lambda message: 'конвертировать валюту' in message.text.lower())
    def start_currency_conversion(message):
        user_data[message.chat.id] = {'step': 'amount'}
        bot.reply_to(message, "Укажите сумму для конвертации.")

    @bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('step') == 'amount')
    def handle_amount(message):
        try:
            amount = float(message.text)
            user_data[message.chat.id]['amount'] = amount
            user_data[message.chat.id]['step'] = 'from_currency'
            markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
            for currency in CURRENCIES:
                markup.add(types.KeyboardButton(currency))
            bot.reply_to(message, "Выберите исходную валюту:", reply_markup=markup)
        except ValueError:
            bot.reply_to(message, "Пожалуйста, введите корректную сумму.")

    @bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('step') == 'from_currency')
    def handle_from_currency(message):
        if message.text.upper() in CURRENCIES:
            user_data[message.chat.id]['from_currency'] = message.text.upper()
            user_data[message.chat.id]['step'] = 'to_currency'
            markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
            for currency in CURRENCIES:
                markup.add(types.KeyboardButton(currency))
            bot.reply_to(message, "Выберите валюту для конвертации:", reply_markup=markup)
        else:
            bot.reply_to(message, "Пожалуйста, выберите валюту из списка.")

    @bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('step') == 'to_currency')
    def handle_to_currency(message):
        if message.text.upper() in CURRENCIES:
            user_data[message.chat.id]['to_currency'] = message.text.upper()
            amount = user_data[message.chat.id]['amount']
            from_currency = user_data[message.chat.id]['from_currency']
            to_currency = user_data[message.chat.id]['to_currency']
            converted_amount = convert_currency(amount, from_currency, to_currency)
            if converted_amount:
                response = f"{amount} {from_currency} = {converted_amount} {to_currency}"
            else:
                response = "Не удалось выполнить конвертацию. Проверьте валюты."
            del user_data[message.chat.id]
            bot.reply_to(message, response, reply_markup=get_main_keyboard())
        else:
            bot.reply_to(message, "Пожалуйста, выберите валюту из списка.")