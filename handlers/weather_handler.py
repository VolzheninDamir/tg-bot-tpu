from telebot import types
from datetime import datetime
from services.weather_service import get_weather_and_hourly_forecast
from keyboards import get_main_keyboard, get_weather_keyboard

def setup_weather_handlers(bot, user_data, user_state):
    # Обработчик кнопки и текстового запроса
    @bot.message_handler(func=lambda message: 
        message.text.strip().lower() in ['узнать погоду', 'погода', 'какая погода', 'какая погода?','температура', 'сколько градусов', 'сколько градусов?'])
    def ask_for_city(message):
        user_state[message.chat.id] = {'mode': 'weather_city'}  # Всегда словарь
        bot.reply_to(
            message,
            "Введите название города, чтобы узнать погоду:",
            reply_markup=types.ReplyKeyboardRemove()
        )

    # Обработчик ввода города
    @bot.message_handler(func=lambda message: 
        isinstance(user_state.get(message.chat.id), dict) and
        user_state[message.chat.id].get('mode') == 'weather_city')
    def handle_city_input(message):
        city = message.text.strip()
        if not city:
            bot.reply_to(message, "Название города не может быть пустым.")
            return
            
        user_data[message.chat.id] = {'city': city}
        user_state[message.chat.id]['mode'] = 'weather_type'
        bot.reply_to(
            message,
            "Выберите тип погоды:",
            reply_markup=get_weather_keyboard()
        )

    # Обработчик выбора типа погоды
    @bot.message_handler(func=lambda message: 
        isinstance(user_state.get(message.chat.id), dict) and
        user_state[message.chat.id].get('mode') == 'weather_type')
    def handle_weather_type(message):
        if message.chat.id not in user_data or 'city' not in user_data[message.chat.id]:
            bot.reply_to(message, "Ошибка: город не указан.", reply_markup=get_main_keyboard())
            user_state.pop(message.chat.id, None)
            return
            
        city = user_data[message.chat.id]['city']
        weather_type = message.text.strip().lower()
        
        if weather_type not in ['погода сейчас', 'погода сегодня']:
            bot.reply_to(message, "Пожалуйста, выберите один из предложенных вариантов.")
            return
            
        weather_data = get_weather_and_hourly_forecast(city)
        
        if not weather_data:
            bot.reply_to(
                message,
                "Извините, не удалось получить данные о погоде. Убедитесь, что вы ввели корректное название города.",
                reply_markup=get_main_keyboard()
            )
        else:
            location = weather_data['location']['name']
            current = weather_data['current']
            
            if weather_type == 'погода сейчас':
                response = (
                    f"Погода в {location} сейчас:\n"
                    f"Состояние: {current['condition']['text']}\n"
                    f"Температура: {current['temp_c']}°C\n"
                    f"Ощущается как: {current['feelslike_c']}°C"
                )
            else:
                forecast_hours = weather_data['forecast']['forecastday'][0]['hour']
                hourly_forecast = [
                    f"{datetime.strptime(hour['time'], '%Y-%m-%d %H:%M').strftime('%H:%M')}: "
                    f"{hour['temp_c']}°C, {hour['condition']['text']}"
                    for hour in forecast_hours[datetime.now().hour:][:12]
                ]
                response = f"Почасовой прогноз на сегодня в {location}:\n" + "\n".join(hourly_forecast)
            
            bot.reply_to(message, response, reply_markup=get_main_keyboard())
        
        user_state.pop(message.chat.id, None)
        user_data.pop(message.chat.id, None)