# handlers/weather_handler.py
from telebot import types
from datetime import datetime
from services.weather_service import get_weather_and_hourly_forecast
from keyboards import get_main_keyboard, get_weather_keyboard

def setup_weather_handlers(bot, user_data, user_state):
    @bot.message_handler(func=lambda message: message.text.lower() == 'узнать погоду')
    def ask_for_city(message):
        user_state[message.chat.id] = 'waiting_for_city'
        bot.reply_to(message, "Введите название города, чтобы узнать погоду.")

    @bot.message_handler(func=lambda message: user_state.get(message.chat.id) == 'waiting_for_city')
    def handle_city_input(message):
        city = message.text.strip()
        user_data[message.chat.id] = {'city': city}
        user_state[message.chat.id] = 'waiting_for_weather_type'
        bot.reply_to(message, "Выберите тип погоды:", reply_markup=get_weather_keyboard())

    @bot.message_handler(func=lambda message: user_state.get(message.chat.id) == 'waiting_for_weather_type')
    def handle_weather_type(message):
        city = user_data[message.chat.id]['city']
        weather_data = get_weather_and_hourly_forecast(city)
        
        if weather_data:
            location = weather_data['location']['name']
            current = weather_data['current']
            forecast_hours = weather_data['forecast']['forecastday'][0]['hour']

            if message.text.lower() == 'погода сейчас':
                condition_now = current['condition']['text']
                temperature_now = current['temp_c']
                bot.reply_to(
                    message,
                    f"Погода в {location} сейчас:\n"
                    f"Состояние: {condition_now}\n"
                    f"Температура: {temperature_now}°C",
                    reply_markup=get_main_keyboard()
                )
            elif message.text.lower() == 'погода сегодня':
                hourly_forecast = [
                    f"{datetime.strptime(hour['time'], '%Y-%m-%d %H:%M').strftime('%H:%M')}: "
                    f"{hour['temp_c']}°C, {hour['condition']['text']}"
                    for hour in forecast_hours
                ]
                bot.reply_to(
                    message,
                    f"Почасовой прогноз на сегодня в {location}:\n" + "\n".join(hourly_forecast),
                    reply_markup=get_main_keyboard()
                )
        else:
            # Возвращаем главную клавиатуру при ошибке
            bot.reply_to(
                message,
                "Извините, не удалось получить данные о погоде. Убедитесь, что вы ввели корректное название города.",
                reply_markup=get_main_keyboard()
            )
        
        # Сбрасываем состояние пользователя
        user_state.pop(message.chat.id, None)
        user_data.pop(message.chat.id, None)