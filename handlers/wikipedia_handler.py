from telebot import types
from services.wikipedia_service import search_wikipedia
from keyboards import get_main_keyboard

def setup_wikipedia_handlers(bot, user_state):
    # Обработчик кнопки
    @bot.message_handler(func=lambda message: message.text.strip() == 'Поиск в Википедии')
    def handle_wiki_button(message: types.Message):
        # Инициализируем состояние для пользователя, если его нет
        if message.chat.id not in user_state:
            user_state[message.chat.id] = {}
            
        user_state[message.chat.id]['mode'] = 'wiki_query'
        bot.send_message(
            message.chat.id,
            "🔍 Введите ваш запрос для поиска в Википедии:",
            reply_markup=types.ReplyKeyboardRemove()
        )
    
    # Обработчик запроса
    @bot.message_handler(func=lambda message: 
        message.chat.id in user_state and 
        user_state[message.chat.id].get('mode') == 'wiki_query')
    def process_wiki_query(message: types.Message):
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
        user_state.pop(message.chat.id, None)