from telebot import types
from services.wikipedia_service import search_wikipedia
from keyboards import get_main_keyboard

def setup_wikipedia_handlers(bot, user_state):
    @bot.message_handler(func=lambda message: message.text.strip() == 'Поиск в Википедии')
    def handle_wiki_button(message: types.Message):
        # Инициализируем состояние как словарь, если его нет
        if not isinstance(user_state.get(message.chat.id), dict):
            user_state[message.chat.id] = {}
            
        user_state[message.chat.id] = {'mode': 'wiki_query'}  # Полная перезапись состояния
        bot.send_message(
            message.chat.id,
            "🔍 Введите ваш запрос для поиска в Википедии:",
            reply_markup=types.ReplyKeyboardRemove()
        )
    
    @bot.message_handler(func=lambda message: 
        isinstance(user_state.get(message.chat.id), dict) and  # Проверяем что это словарь
        user_state[message.chat.id].get('mode') == 'wiki_query')
    def process_wiki_query(message: types.Message):
        try:
            query = message.text.strip()
            
            if not query:
                bot.send_message(message.chat.id, "Запрос не может быть пустым.", reply_markup=get_main_keyboard())
                user_state.pop(message.chat.id, None)
                return
            
            bot.send_chat_action(message.chat.id, 'typing')
            summary, url = search_wikipedia(query)
            
            response = "📚 Результаты поиска:\n\n"
            if summary:
                response += f"{summary}"
                if url:
                    response += f"\n\n🌐 Подробнее: {url}"
            else:
                response = "❌ По вашему запросу ничего не найдено."
            
            bot.send_message(
                message.chat.id,
                response,
                reply_markup=get_main_keyboard(),
                disable_web_page_preview=True
            )
        finally:
            # Гарантированно очищаем состояние, даже если возникла ошибка
            if message.chat.id in user_state:
                user_state.pop(message.chat.id, None)