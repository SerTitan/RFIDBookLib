from telebot import TeleBot, types
import firebase_setup as firedb
from classes import FirebaseDB 

TELEGRAM_TOKEN = '7163938222:AAF7uWZknK9fmLwv0UdjRU_y-VwBnaX8sig'
bot = TeleBot(TELEGRAM_TOKEN)

firebase_db = FirebaseDB(None, None)
firebase_db.admin, firebase_db.app = firedb.initialize_connection()

class UserSession:
    def __init__(self):
        self.isu_number = None
        self.bookshelf = None

# Словарь для хранения сессий
user_sessions = {}


def get_user_session(chat_id):
    if chat_id not in user_sessions:
        user_sessions[chat_id] = UserSession()
    return user_sessions[chat_id]

@bot.message_handler(commands=["start"])
def start(message):
    user_sessions[message.chat.id] = UserSession()  # Reset or start a new session
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    start = types.KeyboardButton('Войти')
    keyboard.add(start)
    bot.send_message(message.chat.id, 'Привет! Необходимо войти.', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'Войти')
def ask_isu_number(message):
    bot.send_message(message.chat.id, "Введите свой номер ису:")
    bot.register_next_step_handler(message, process_isu_number)

def process_isu_number(message):
    session = get_user_session(message.chat.id)
    if message.text.isdigit():
        session.isu_number = int(message.text)
        bot.send_message(message.chat.id, "Введите номер стелажа:")
        bot.register_next_step_handler(message, bookshelf_process)
    else:
        bot.send_message(message.chat.id, "Номер ИСУ должен содержать только цифры. Напишите /start и введите его еще раз.")

def bookshelf_process(message):
    session = get_user_session(message.chat.id)
    if message.text.isdigit():
        session.bookshelf = int(message.text)
        save_user_data(message.chat.id, message.chat.username)
    else:
        bot.send_message(message.chat.id, "Номер стеллажа должен содержать только цифры. Напишите /start и введите его еще раз.")

def save_user_data(chat_id, username):
    session = user_sessions[chat_id]
    if session.isu_number and session.bookshelf:
        ref = firebase_db.admin.reference(f'/library/user_list')
        new_user = {
            'id': chat_id,
            'isu_number': session.isu_number,
            'bookshelf': session.bookshelf
        }
        ref.child(username).set(new_user)
        bot.send_message(chat_id, "Спасибо! Ваши данные успешно сохранены!")

bot.polling()
