| |Detailed analysis of each line| |


////Importing the necessary libraries////

import telebot
from telebot import types
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import random
import requests

//
telebot: The main library for interacting with the Telegram API.
types from telebot: A module for working with various types of messages and a keyboard.
datetime: A module for working with date and time.
BackgroundScheduler from apscheduler.schedulers.background: A library for scheduling tasks.
logging: A module for logging.
random: A module for generating random numbers.
requests: A module for sending HTTP requests (used to download images from Yandex.Disk).


////Settings and initialization////

# Insert your BotFather token here
TOKEN = 'YOUR_BOT_TOKEN'

# Creating a bot object
bot = telebot.TeleBot(TOKEN)

//
TOKEN: A string constant containing the token received from BotFather.
bot = telebot.TeleBot(TOKEN): Creates a TeleBot object that is used to interact with the Telegram API.


////Logging////

# Setting up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

//
basicConfig: Sets the logging format and logging level (INFO).
getLogger: Gets the logger object for future use.


////Creator information and feedback////

# List of authors
AUTHORS = [
    ('Author 1', '@author1'),
('Author 2', '@author2'),
('Author 3', '@author3')
]

GITHUB_LINK = 'https://github.com/your-repo/memebot'
FEEDBACK_CONTACT = '@feedback_contact'

//
AUTHORS: A list of tuples with the names and nicknames of the authors.
GITHUB_LINK: A link to the bot's source code repository.
FEEDBACK_CONTACT: Contact for feedback.


////List of users and links to photos////

# List of users to whom memes will be sent
users = set()

# List of links to photos from Yandex.Disk
photos_urls = [
    'https://yadi.sk/i/link_1.jpg',
    'https://yadi.sk/i/link_2.jpg',
    'https://yadi.sk/i/link_3.jpg',
    # Add your links to the photos
]

//
users: A set for storing user IDs that will start communicating with the bot.
photos_urls: A list of URLs of images that will be sent to users.


////Welcome team and creation of the main menu////

# Function for greeting and displaying the main menu
@bot.message_handler(commands=['start'])
def send_welcome(message):
users.add(message.chat.id ) # Adding the user to the list
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
itembtn1 = types.KeyboardButton('How it works')
itembtn2 = types.KeyboardButton('Creators')
    itembtn3 = types.KeyboardButton('Feedback')
    markup.add(itembtn1, itembtn2, itembtn3)
    
    bot.send_message(message.chat.id ,
f"Hello! I'm an idiot. What would you like to know?",
reply_markup=markup)

//
@bot.message_handler(commands=['start']): Decorates the send_welcome function to process the /start command.
users.add(message.chat.id ): Adds the user's ID to the users set.
ReplyKeyboardMarkup: Creates a keyboard object.
itembtn1, itembtn2, itembtn3: Buttons for the main menu.
markup.add(...): Adds buttons to the keyboard.
bot.send_message(...): Sends a welcome message with the keyboard.


////Processing of the main menu commands////

# Main keyboard command handler
@bot.message_handler(func=lambda message: True)
def handle_menu_buttons(message):
if message.text == 'How it works':
bot.send_message(message.chat.id "This bot is designed to delight you with cat memes every Monday morning!")
show_back_button(message)
        
    elif message.text == 'Creators':
authors_text = '\n'.join([f'{author[0]} - {author[1]}' for author in AUTHORS])
        bot.send_message(message.chat.id f' The authors of this wonderful bot:\n\n{authors_text}')
bot.send_message(message.chat.id , f'code is available here: {GITHUB_LINK}')
show_back_button(message)
        
    elif message.text == 'Feedback':
        bot.send_message(message.chat.id , f' For any questions, please contact @{FEEDBACK_CONTACT}')
show_back_button(message)

    elif message.text == 'Get back':
        main_menu(message)

//
@bot.message_handler(func=lambda message: True): Handles all incoming messages.
if message.text == ...: Checks the text of the message and performs the appropriate action.
show_back_button(message): Calls a function to display the Back button.
elif message.text == 'Back': main_menu(message): Returns the user to the main menu.


////Displaying the "Back" button////

# Showing the Back button
def show_back_button(message):
markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
itembtn_back = types.KeyboardButton('Back')
markup.add(itembtn_back)
    bot.send_message(message.chat.id 'Do you want to return to the main menu?', reply_markup=markup)

//
ReplyKeyboardMarkup: Creates a new keyboard.
itembtn_back: The "Back" button.
markup.add(itembtn_back): Adds a button to the keyboard.
bot.send_message(...): Sends a message asking you to return to the main menu.


////Return to the main menu////

# Main menu
def main_menu(message):
markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
itembtn1 = types.KeyboardButton('How it works')
itembtn2 = types.KeyboardButton('Creators')
    itembtn3 = types.KeyboardButton('Feedback')
markup.add(itembtn1, itembtn2, itembtn3)
    
    bot.send_message(message.chat.id ,
f"What would you like to know?",
reply_markup=markup)

//
ReplyKeyboardMarkup: Creates a new keyboard.
itembtn1, itembtn2, itembtn3: Buttons for the main menu.
markup.add(...): Adds buttons to the keyboard.
bot.send_message(...): Sends a message with the main menu.


////Sending memes on a schedule////

# Sending memes with cats according to the schedule
def send_memes():
logger.info ("Sending memes...")
# Choose a random photo
    selected_url = random.choice(photos_urls)
    
    for chat_id in users:
        try:
            # Sending the photo via the link
            bot.send_photo(chat_id, selected_url)
        except Exception as e:
            logger.error(f"Failed to send meme to chat {chat_id}: {e})

//
logger.info ("Sending memes..."): An entry in the log about the start of sending memes.
selected_url = random.choice(photos_urls): Selects a random image URL from the list.
for chat_id in users:: Going through the list of users.
try/except: An attempt to send an image. In case of an error, write to the log.


////Configuring the Task Scheduler////

# Task scheduler
scheduler = BackgroundScheduler()

# The task for sending memes is on Monday at 8:00
scheduler.add_job(send_memes, 'cron', day_of_week='mon', hour=8, minute=0)

# New task for sending memes on Friday at 3 p.m.
scheduler.add_job(send_memes, 'cron', day_of_week='fri', hour=15, minute=0)

scheduler.start()

//
BackgroundScheduler: Creating an instance of the scheduler.
.add_job(...): Add tasks to send memes on the specified days and times.
scheduler.start(): Starts the scheduler.


////Launching the bot////

# Launching the bot
if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    finally:
        scheduler.shutdown(wait=False)

//
if __name__ == '__main__':: Is executed only when the script is run directly.
bot.polling(none_stop=True): Constantly polls the Telegram server for new messages.
finally: scheduler.shutdown(wait=False): Stops the scheduler before the program ends.