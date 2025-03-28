# handlers/text_handler.py
from datetime import datetime
from telebot import types
from keyboards import get_main_keyboard
from services.currency_service import convert_currency
from services.weather_service import get_weather_and_hourly_forecast

def setup_text_handlers(bot, user_data, user_state):
    @bot.message_handler(func=lambda message: True)
    def handle_text(message):
        if isinstance(user_state.get(message.chat.id), dict):
            return
        text = message.text.lower()
        response = []
        now = datetime.now()

        # Обработка запросов на время
        time_keywords = [
            'время', 'час', 'времени', 'сколько времени', 'который час', 'текущее время',
            'сейчас время', 'подскажи время', 'скажи время', 'точное время', 'время сейчас',
            'сколько сейчас', 'который сейчас', 'сколько на часах', 'время узнать'
        ]
        if any(word in text for word in time_keywords):
            response.append(f"Сейчас {now.strftime('%H:%M:%S')}.")

        # Обработка запросов на дату
        date_keywords = [
            'дата', 'число', 'дату', 'какое число', 'какая дата', 'сегодняшняя дата',
            'сегодня число', 'текущая дата', 'подскажи дату', 'скажи дату', 'какое сегодня число',
            'какая сегодня дата', 'дата сегодня', 'число сегодня', 'сегодняшнее число',
            'текущее число', 'текущая дата', 'дата узнать', 'число узнать'
        ]
        if any(word in text for word in date_keywords):
            response.append(f"Сегодня {now.strftime('%Y-%m-%d')}.")

        # Обработка запросов на состояние
        mood_keywords = [
            'дела', 'ты', 'настроение', 'как дела', 'как ты', 'как настроение',
            'как жизнь', 'как сам', 'как поживаешь', 'как ты себя чувствуешь',
            'как твои дела', 'как у тебя дела', 'как твое настроение', 'как ты поживаешь',
            'как ты сегодня', 'как ты себя', 'как твоя жизнь'
        ]
        if any(word in text for word in mood_keywords):
            response.append("У меня все отлично, спасибо! А у тебя?")

        # Обработка запросов на занятость
        activity_keywords = [
            'занимаешься', 'делаешь', 'работаешь', 'что делаешь', 'чем занимаешься',
            'что ты делаешь', 'чем ты занимаешься', 'что сейчас делаешь', 'чем сейчас занимаешься',
            'что ты сейчас делаешь', 'чем ты сейчас занимаешься', 'что делаешь сейчас',
            'чем занимаешься сейчас', 'что ты делаешь сейчас', 'чем ты занимаешься сейчас',
            'что делаешь сегодня', 'чем занимаешься сегодня', 'что ты делаешь сегодня',
            'чем ты занимаешься сегодня'
        ]
        if any(word in text for word in activity_keywords):
            response.append("Я помогаю тебе!)")

        # Обработка запросов на прощание
        goodbye_keywords = [
            'пока', 'до свидания', 'выход', 'завершить', 'прощай', 'до встречи',
            'пока пока', 'до скорого', 'до завтра', 'до следующего раза', 'пока что',
            'завершить работу', 'завершить сеанс', 'завершить общение', 'завершить чат',
            'завершить диалог', 'завершить разговор'
        ]
        if any(word in text for word in goodbye_keywords):
            response.append("До свидания! Если что, я всегда тут.")

        # Обработка запросов на конвертацию валюты
        currency_keywords = [
            'конвертировать валюту', 'перевести валюту', 'обмен валюты', 'курс валют',
            'сколько будет', 'пересчет валюты', 'конвертация валюты'
        ]
        if any(word in text for word in currency_keywords):
            user_data[message.chat.id] = {'step': 'amount'}
            bot.reply_to(message, "Укажите сумму для конвертации.")
            return

        # Обработка запросов на помощь
        help_keywords = [
            'помощь', 'помоги', 'что ты умеешь', 'как пользоваться', 'что ты можешь',
            'какие команды', 'какие функции', 'что ты знаешь', 'что ты делаешь',
            'как работать', 'как использовать', 'как пользоваться ботом'
        ]
        if any(word in text for word in help_keywords):
            response.append(
                "Я умею:\n"
                "- Подсказать текущее время.\n"
                "- Подсказать сегодняшнюю дату.\n"
                "- Рассказать, как у меня дела.\n"
                "- Ответить на вопросы о моей занятости.\n"
                "- Попрощаться с тобой.\n"
                "- Конвертировать валюту.\n"
                "- Показывать погоду.\n"
                "Скоро я научусь ещё больше!"
            )

        # Обработка запросов о боте
        about_keywords = [
            'кто ты', 'что ты', 'расскажи о себе', 'кто такой', 'что такое',
            'как тебя зовут', 'как тебя называть', 'ты кто', 'ты что', 'ты бот',
            'ты человек', 'ты программа', 'ты искусственный интеллект'
        ]
        if any(word in text for word in about_keywords):
            response.append(
                "Я — твой бот-ассистент. Я создан, чтобы помогать тебе с базовыми задачами, "
                "такими как подсказка времени, даты и ответы на простые вопросы. "
                "Я постоянно учусь и улучшаюсь!"
            )

        # Формируем итоговый ответ
        if response:
            bot.reply_to(message, "\n".join(response), reply_markup=get_main_keyboard())
        else:
            bot.reply_to(message, "Извини, я не понял твоего вопроса.", reply_markup=get_main_keyboard())