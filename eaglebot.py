import os, time, json
from dotenv import load_dotenv, find_dotenv
import telebot
from telebot import types
import sqlite3
from telebot.types import ReplyKeyboardRemove
import sys
sys.path.append('data')
from dialog import get_path_file_to_send, files_to_sending

load_dotenv(find_dotenv())
bot_token = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(bot_token)

current_dir = os.path.dirname(os.path.abspath(__file__))
relative_path_ui_json = os.path.join(current_dir, 'data', 'ui.json')
with open(relative_path_ui_json) as uifile:
    ui_data = json.load(uifile)


database_file = '/var/lib/sqlite/data/eaglebot.db'
def init_db():
  # Check if the database file exists
  if not os.path.exists(database_file):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_request_date TIMESTAMP,
        request_counter INTEGER DEFAULT 1
      );
    ''')
    conn.commit()
    conn.close()
    print("Database file created successfully.")
  else:
    print("Database file already exists.")


# Добавление или обновление пользователя в базе данных
def add_or_update_user(user_id):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    try:
        # Использование плейсхолдеров для username и password
        cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        print("User added/updated successfully")

        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        print("users in the database:")
        for row in rows:
          print(row)

    except Exception as e:
        print(f"Error adding/updating user: {e}")
    finally:
        conn.close()


# счетчик запросов:
def write_request_counter(user_id):
  conn = sqlite3.connect(database_file)
  cursor = conn.cursor()
  try:
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    if user:
      cursor.execute("UPDATE users SET last_request_date = CURRENT_TIMESTAMP, request_counter = request_counter + 1 WHERE user_id = ?", (user_id,))
      conn.commit()

  except Exception as e:
    print(f"Error write_request_counter: {e}")
  finally:
    conn.close()


def generate_categories_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    categories = ui_data.get("categories", {}).items()
    for cat_id, cat_data in categories:
      markup.add(types.InlineKeyboardButton(cat_data["name"], callback_data=f"cat_{cat_id}"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    categories = ui_data['categories']
    if call.data == "back_to_categories":
        markup = generate_categories_keyboard()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите категорию:", reply_markup=markup)
    elif call.data.startswith("cat_"):
        cat_id = call.data.split("_")[1]
        markup = types.InlineKeyboardMarkup()
        for opt_key, opt_value in categories[f"{cat_id}"]["options"].items():
            opt_question = opt_value["question"]
            markup.add(types.InlineKeyboardButton(opt_question, callback_data=f"opt_{cat_id}_{opt_key}"))
        markup.add(types.InlineKeyboardButton("Назад", callback_data="back_to_categories"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите опцию:", reply_markup=markup)
    elif call.data.startswith("opt_"):

        user_id = call.from_user.id
        write_request_counter(user_id)

        _, cat_id, opt_id = call.data.split("_")
        opt_value = categories[f"{cat_id}"]["options"][f"{opt_id}"]
        if "file" in opt_value:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            send_file(opt_value["file"], call)
        else:
            response = categories[f"{cat_id}"]["options"][f"{opt_id}"]["response"]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response, reply_markup=None)


# Отправка файла пользователю
def send_file(doc_path, call):
    try:
        with open(get_path_file_to_send(files_to_sending[doc_path]["filename"]), 'rb') as doc:
            bot.send_document(call.message.chat.id, doc)
        bot.answer_callback_query(call.id, "Документ отправлен.")
    except FileNotFoundError:
        bot.answer_callback_query(call.id, "Файл не найден.")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    add_or_update_user(user_id)  # Добавляем если надо пользователя при первом обращении

    markup = generate_main_keyboard()
    bot.send_message(message.chat.id, "Все готово к работе!", reply_markup=markup)
   

def generate_main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button4 = types.KeyboardButton("Помощь")
    button1 = types.KeyboardButton("Разделы")
    markup.add(button1, button4)
    return markup

@bot.message_handler(func=lambda message: message.text == "Разделы")
def show_questions(message):
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=generate_categories_keyboard())
    
@bot.message_handler(func=lambda message: message.text == "Помощь")
def send_instruction_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton(ui_data['manual']['name'])
    btn2 = types.KeyboardButton(ui_data['support']['name'])
    btn_back = types.KeyboardButton("Назад")
    markup.add(btn1, btn2, btn_back)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)
   

@bot.message_handler(func=lambda message: message.text == ui_data['manual']['name'])
def handle_instruction(message):
    markup = generate_main_keyboard()
    bot.send_message(message.chat.id, ui_data['manual']['resp'], reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == ui_data['support']['name'])
def handle_support(message):
    markup = generate_main_keyboard()
    bot.send_message(message.chat.id, ui_data['support']['resp'], reply_markup=markup)
   
@bot.message_handler(func=lambda message: message.text == "Назад")
def handle_back(message):
    markup = generate_main_keyboard()
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)


init_db()
# init_files_to_sending_dir()

#bot.polling(none_stop=True) # dev variant

# prod variant
if __name__=='__main__':
    while True:
        try:
            bot.polling(non_stop=True, interval=0)
        except Exception as e:
            print(e)
            time.sleep(5)
            continue