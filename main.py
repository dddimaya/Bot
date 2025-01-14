import telebot
from telebot import types
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import random
import requests

# Вставьте сюда ваш токен от BotFather
TOKEN = 'YOUR_BOT_TOKEN'

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Настраиваем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Список авторов
AUTHORS = [
    ('Автор 1', '@author1'),
    ('Автор 2', '@author2'),
    ('Автор 3', '@author3')
]

GITHUB_LINK = 'https://github.com/your-repo/memebot'
FEEDBACK_CONTACT = '@feedback_contact'

# Список пользователей, которым будут отправлены мемы
users = set()

# Список ссылок на фотографии с Яндекс.Диска
photos_urls = [
    'https://yadi.sk/i/link_1.jpg',
    'https://yadi.sk/i/link_2.jpg',
    'https://yadi.sk/i/link_3.jpg',
    # Добавьте свои ссылки на фотографии
]

# Функция для приветствия и отображения главного меню
@bot.message_handler(commands=['start'])
def send_welcome(message):
    users.add(message.chat.id)  # Добавляем пользователя в список
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Как это работает')
    itembtn2 = types.KeyboardButton('Создатели')
    itembtn3 = types.KeyboardButton('Обратная связь')
    markup.add(itembtn1, itembtn2, itembtn3)
    
    bot.send_message(message.chat.id,
                     f"Привет! Я МемБот. Что бы ты хотел узнать?",
                     reply_markup=markup)

# Обработчик команд главной клавиатуры
@bot.message_handler(func=lambda message: True)
def handle_menu_buttons(message):
    if message.text == 'Как это работает':
        bot.send_message(message.chat.id, "Этот бот создан для того, чтобы радовать вас мемами с котиками каждое утро понедельника!")
        show_back_button(message)
        
    elif message.text == 'Создатели':
        authors_text = '\n'.join([f'{author[0]} - {author[1]}' for author in AUTHORS])
        bot.send_message(message.chat.id, f'Авторы этого замечательного бота:\n\n{authors_text}')
        bot.send_message(message.chat.id, f'Код доступен тут: {GITHUB_LINK}')
        show_back_button(message)
        
    elif message.text == 'Обратная связь':
        bot.send_message(message.chat.id, f'По всем вопросам обращайтесь к @{FEEDBACK_CONTACT}')
        show_back_button(message)

    elif message.text == 'Назад':
        main_menu(message)

# Показываем кнопку "Назад"
def show_back_button(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    itembtn_back = types.KeyboardButton('Назад')
    markup.add(itembtn_back)
    bot.send_message(message.chat.id, 'Хотите вернуться в главное меню?', reply_markup=markup)

# Главное меню
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Как это работает')
    itembtn2 = types.KeyboardButton('Создатели')
    itembtn3 = types.KeyboardButton('Обратная связь')
    markup.add(itembtn1, itembtn2, itembtn3)
    
    bot.send_message(message.chat.id,
                     f"Что бы ты хотел узнать?",
                     reply_markup=markup)

# Отправка мемов с котиками по расписанию
def send_memes():
    logger.info("Отправляем мемы...")
    # Выбираем случайную фотографию
    selected_url = random.choice(photos_urls)
    
    for chat_id in users:
        try:
            # Отправляем фотографию по ссылке
            bot.send_photo(chat_id, selected_url)
        except Exception as e:
            logger.error(f"Не удалось отправить мем в чат {chat_id}: {e}")

# Планировщик задач
scheduler = BackgroundScheduler()

# Задание для отправки мемов в понедельник в 8:00
scheduler.add_job(send_memes, 'cron', day_of_week='mon', hour=8, minute=0)

# Новое задание для отправки мемов в пятницу в 15:00
scheduler.add_job(send_memes, 'cron', day_of_week='fri', hour=15, minute=0)

scheduler.start()

# Запускаем бота
if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    finally:
        scheduler.shutdown(wait=False)