import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import json
import os

data_file = "database.json"
token_file = "token.txt"
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

@bot.message_handler(commands=["start"])
def start_message(message):
    chat_id = str(message.chat.id)
    if chat_id not in chat_data:
        chat_data[chat_id] = {
            "username": "",
            "vpn_allowed": False,
            "start_date": "",
            "end_date": "",
            "state": "waiting_login",
            "link": ""
        }
        save_data()

    bot.send_message(
        message.chat.id,
        f"Приветствую тебя в сервисе GilimVPN!\n\nДля старта напиши логин, который тебе выдал админ:\n\nЧтобы его получить обратитесь за помощью по кнопке",
        reply_markup=get_main_keyboard()
    )

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton("Помощь"))
    return keyboard

@bot.message_handler(func=lambda message: True)

def message_handler(message):
    global waiting_config

    if message.chat.id == admin_id and waiting_config is not None:
        link = message.text
        chat_data[waiting_config]["state"] = "active"
        chat_data[waiting_config]["link"] = link
        chat_data[waiting_config]["vpn_allowed"] = True
        save_data()

        bot.send_message(
            int(waiting_config),
            f"Скопируйте ссылку и вставьте ее в установленный VPN-клиент. (Happ)\n\n {link}"
        )

        waiting_config = None

        bot.send_message(
            admin_id,
            f"Конфигурация успешно отправлена пользователю!"
        )
        return

    elif message.chat.id == admin_id:
        return

    elif message.text == "Помощь":
            chat_id = str(message.chat.id)
            bot.send_message(
                message.chat.id,
                "За помощью или обратной связью сюда: @fancutedora",
                reply_markup=get_main_keyboard()
            )

    else:
        chat_id = str(message.chat.id)
        if chat_data[chat_id]["state"] == "waiting_approval":
            bot.send_message(
                message.chat.id,
                f"Ты уже зарегестрирован! Но аккаунт не подтвержден админом! Обратитесь в тех поддержку"
            )
        elif chat_data[chat_id]["state"] == "active":
            bot.send_message(
                message.chat.id,
                f"Ты уже успешно зарегестрирован!"
            )
        elif chat_data[chat_id]["state"] == "waiting_login":
            chat_data[chat_id]["username"] = message.text
            chat_data[chat_id]["state"] = "waiting_approval"
            save_data()
            send_username(message, chat_id)
            bot.send_message(
                message.chat.id,
                f"Вы успешно зарегестрированы!\nАдмин скоро подтвердит ваш профиль!"
            )

def send_username(message, chat_id):
    bot.send_message(
        admin_id,
        f"{message.text} - этот user хочет добавиться к нам. Нажми кнопку для подтверждения",
        reply_markup=get_approve_keyboard(chat_id)
    )

def get_approve_keyboard(chat_id):
    callback_data = f"approve_{chat_id}"
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("Подтверждаю", callback_data=callback_data)
    )
    return keyboard

@bot.callback_query_handler(func=lambda call: True)



def callback_handler(call):

    if call.data.startswith("approve_"):
        chat_id = call.data.split("_")[1]

        if chat_data[chat_id]["state"] == "active":
            bot.send_message(
                admin_id,
                "Пользователь уже подтвержден!"
            )
            return

        global waiting_config
        chat_data[chat_id]["state"] = "active"
        waiting_config = chat_id
        save_data()

        bot.edit_message_text(
            chat_id = call.message.chat.id,
            message_id = call.message.message_id,
            text = f"Пользователь {chat_data[chat_id]['username']} подтвержден!\n\nОтправь сюда конфигурацию!\n\nСЛЕДУЮЩЕЕ СООБЩЕНИЕ БУДЕТ ПЕРЕСЛАНО ПОЛЬЗОВАТЕЛЮ!"
        )

        bot.send_message(
            chat_id,
            "Админ одобрил вашу заявку!\n\nСовсем скоро пришлём конфигурацию для настройки VPN"
        )

        bot.answer_callback_query(call.id)

bot.infinity_polling()