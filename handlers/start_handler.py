# handlers/start_handler.py
from telebot import types
from keyboards import get_main_keyboard

def setup_start_handler(bot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "Привет! Я твой бот-ассистент. Чем могу помочь?", reply_markup=get_main_keyboard())