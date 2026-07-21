import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import json
import os
from datetime import datetime, timedelta

data_file = "database.json"
token_file = "token_admin.txt"
admin_id_file = "admin_id.txt"
waiting_config = None

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

def admin_id():
    with open(admin_id_file, "r", encoding="utf-8") as f:
        return int(f.readline())

admin_id = admin_id()

chat_data = load_data()

token = read_token()

bot = telebot.TeleBot(token)