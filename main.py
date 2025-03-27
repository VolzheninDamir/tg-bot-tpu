# main.py
import telebot
from config import BOT_TOKEN
from handlers.start_handler import setup_start_handler
from handlers.weather_handler import setup_weather_handlers
from handlers.currency_handler import setup_currency_handlers
from handlers.text_handler import setup_text_handlers
from handlers.wikipedia_handler import setup_wikipedia_handlers

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Словари для хранения данных пользователя
user_data = {}
user_state = {}

# Настройка обработчиков
setup_start_handler(bot)
setup_wikipedia_handlers(bot, user_state)
setup_weather_handlers(bot, user_data, user_state)
setup_currency_handlers(bot, user_data)
setup_text_handlers(bot, user_data, user_state)

# Запуск бота
bot.polling()