| |Подробный разбор каждой строки| |


////Импортируем необходимые библиотеки////

import telebot
from telebot import types
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import random
import requests

//
telebot: Основная библиотека для взаимодействия с Telegram API.
types из telebot: Модуль для работы с различными типами сообщений и клавиатурой.
datetime: Модуль для работы с датой и временем.
BackgroundScheduler из apscheduler.schedulers.background: Библиотека для планирования задач.
logging: Модуль для ведения логов.
random: Модуль для генерации случайных чисел.
requests: Модуль для отправки HTTP-запросов (используется для загрузки изображений с Яндекс.Диска).


////Настройки и инициализация////

# Вставьте сюда ваш токен от BotFather
TOKEN = 'YOUR_BOT_TOKEN'

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

//
TOKEN: Строковая константа, содержащая токен, полученный у BotFather.
bot = telebot.TeleBot(TOKEN): Создает объект TeleBot, который используется для взаимодействия с Telegram API.


////Логирование////

# Настраиваем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

//
basicConfig: Устанавливает формат записи логов и уровень логирования (INFO).
getLogger: Получает объект логгера для использования в дальнейшем.


////Данные о создателях и обратная связь////

# Список авторов
AUTHORS = [
    ('Автор 1', '@author1'),
    ('Автор 2', '@author2'),
    ('Автор 3', '@author3')
]

GITHUB_LINK = 'https://github.com/your-repo/memebot'
FEEDBACK_CONTACT = '@feedback_contact'

//
AUTHORS: Список кортежей с именами и никнеймами авторов.
GITHUB_LINK: Ссылка на репозиторий с исходным кодом бота.
FEEDBACK_CONTACT: Контакт для обратной связи.


////Список пользователей и ссылок на фотографии////

# Список пользователей, которым будут отправлены мемы
users = set()

# Список ссылок на фотографии с Яндекс.Диска
photos_urls = [
    'https://yadi.sk/i/link_1.jpg',
    'https://yadi.sk/i/link_2.jpg',
    'https://yadi.sk/i/link_3.jpg',
    # Добавьте свои ссылки на фотографии
]

//
users: Множество для хранения идентификаторов пользователей, которые начнут общение с ботом.
photos_urls: Список URL изображений, которые будут отправляться пользователям.


////Приветственная команда и создание главного меню////

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

//
@bot.message_handler(commands=['start']): Декорирует функцию send_welcome для обработки команды /start.
users.add(message.chat.id): Добавляет ID пользователя в множество users.
ReplyKeyboardMarkup: Создает объект клавиатуры.
itembtn1, itembtn2, itembtn3: Кнопки для главного меню.
markup.add(...): Добавляет кнопки в клавиатуру.
bot.send_message(...): Отправляет приветственное сообщение с клавиатурой.


////Обработка команд главного меню////

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

//
@bot.message_handler(func=lambda message: True): Обрабатывает все входящие сообщения.
if message.text == ...: Проверяет текст сообщения и выполняет соответствующее действие.
show_back_button(message): Вызывает функцию для отображения кнопки "Назад".
elif message.text == 'Назад': main_menu(message): Возвращает пользователя в главное меню.


////Отображение кнопки "Назад"////

# Показываем кнопку "Назад"
def show_back_button(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    itembtn_back = types.KeyboardButton('Назад')
    markup.add(itembtn_back)
    bot.send_message(message.chat.id, 'Хотите вернуться в главное меню?', reply_markup=markup)

//
ReplyKeyboardMarkup: Создает новую клавиатуру.
itembtn_back: Кнопка "Назад".
markup.add(itembtn_back): Добавляет кнопку в клавиатуру.
bot.send_message(...): Отправляет сообщение с предложением вернуться в главное меню.


////Возврат в главное меню////

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

//
ReplyKeyboardMarkup: Создает новую клавиатуру.
itembtn1, itembtn2, itembtn3: Кнопки для главного меню.
markup.add(...): Добавляет кнопки в клавиатуру.
bot.send_message(...): Отправляет сообщение с главным меню.


////Отправка мемов по расписанию////

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
            logger.error(f"Не удалось отправить мем в чат {chat_id}: {e})

//
logger.info("Отправляем мемы..."): Запись в лог о начале отправки мемов.
selected_url = random.choice(photos_urls): Выбор случайного URL изображения из списка.
for chat_id in users:: Проход по списку пользователей.
try/except: Попытка отправить изображение. В случае ошибки запись в лог.


////Настройка планировщика задач////

# Планировщик задач
scheduler = BackgroundScheduler()

# Задание для отправки мемов в понедельник в 8:00
scheduler.add_job(send_memes, 'cron', day_of_week='mon', hour=8, minute=0)

# Новое задание для отправки мемов в пятницу в 15:00
scheduler.add_job(send_memes, 'cron', day_of_week='fri', hour=15, minute=0)

scheduler.start()

//
BackgroundScheduler: Создание экземпляра планировщика.
.add_job(...): Добавление заданий для отправки мемов в указанные дни и время.
scheduler.start(): Запуск планировщика.


////Запуск бота////

# Запускаем бота
if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    finally:
        scheduler.shutdown(wait=False)

//
if __name__ == '__main__':: Выполняется только при прямом запуске скрипта.
bot.polling(none_stop=True): Постоянный опрос сервера Telegram на наличие новых сообщений.
finally: scheduler.shutdown(wait=False): Остановка планировщика перед завершением программы.
