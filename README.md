# Telegram Assistant Bot 🤖

Умный бот-ассистент с широким функционалом. Умеет отвечать на вопросы, показывать погоду, конвертировать валюты и многое другое.

## 🌟 Основные функции

### 🔍 Поиск в Википедии
- `"Поиск в Википедии"` → Ищет информацию по вашему запросу

### 🕒 Время и дата
- `"Который час?"` → Показывает текущее время
- `"Какая сегодня дата?"` → Выводит дату

### 🌤️ Погода
- `"Погода в Москве"` → Прогноз для указанного города
- `"Какая погода?"` → Запрашивает город и показывает погоду

### 💱 Конвертер валют
- `"Конвертировать валюту"` → Запускает процесс конвертации
- `"Сколько будет 100 USD в RUB?"` → Конвертирует сумму

### 💬 Общение
- `"Как дела?"` → Отвечает на вопросы о настроении
- `"Что делаешь?"` → Рассказывает о своей деятельности
- `"Кто ты?"` → Представляет бота

### 🏁 Прощание
- `"Пока"` → Корректно завершает диалог

## 🛠️ Установка и запуск

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/VolzheninDamir/tg-bot-tpu.git
    cd tg-bot-tpu
2. Установите зависимости:
    ```bash
    pip install -r requirements.txt
3. Создайте файл config.py на основе примера:
    ```bash
    BOT_TOKEN = "ваш_токен_бота"
    # Другие настройки...
4. Запустите бота:
    ```bash
    python main.py

## ⚙️ Технологии
- Python 3.9+
- python-telegram-bot
- Requests (для API запросов)
- Wikipedia API (для поиска информации)

## 📌 Примеры команд

| Команда                     | Ответ                                |
|-----------------------------|--------------------------------------|
| "Сколько времени?"          | "Сейчас 14:25:30"                    |
| "Какое сегодня число?"      | "Сегодня 2023-11-15"                 |
| "Как дела?"                 | "У меня все отлично! А у тебя?"      |
| "Погода в Сочи"             | (показывает погоду)                  |
| "Конвертировать 50 EUR в USD" | (результат конвертации)            |
