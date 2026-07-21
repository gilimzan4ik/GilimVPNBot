import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import json
import os

data_file = "database.json"
token_file = "token_admin.txt"

def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data():
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(chat_data, f, ensure_ascii=False, indent=4)

def read_token():
    with open(token_file, "r", encoding="utf-8") as f:
        return f.readline()

chat_data = load_data()
token = read_token()
bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(
        message.chat.id,
        f"Привет, это админка сервиса GilimVPN.\n\nЕсли ты тут сидишь, значит ты избранный",
        reply_markup=get_main_keyboard()
    )

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton("Пользователи"))
    keyboard.row(KeyboardButton("Статистика"))
    keyboard.row(KeyboardButton("Помощь"))
    return keyboard

@bot.message_handler(func=lambda message: message.text == "Пользователи")
def users_message(message):
    bot.send_message(
        message.chat.id,
        "Тут как-нибудь надо сделать вывод всех пользователей с их ником и со сроком действия подписки"
    )

@bot.message_handler(func=lambda message: message.text == "Пользователи")
def users_message(message):
    bot.send_message(
        message.chat.id,
        "А сюда всю какую никакую статистику написать"
    )

@bot.message_handler(func=lambda message: message.text == "Помощь")
def help_message(message):
    bot.send_message(
        message.chat.id,
        "За помощью или обратной связью сюда: @fancutedora"
    )


bot.infinity_polling()