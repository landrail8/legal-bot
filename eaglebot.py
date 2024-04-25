import os, time
from dotenv import load_dotenv, find_dotenv
import telebot
from telebot import types
import sqlite3
from telebot.types import ReplyKeyboardRemove
import sys
sys.path.append('data')
from dialog import id_mapping, option_responses, get_path_file_to_send, files_to_sending

load_dotenv(find_dotenv())
bot_token = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(bot_token)


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
    for cat_id, cat_data in id_mapping.items():
        markup.add(types.InlineKeyboardButton(cat_data["name"], callback_data=f"cat_{cat_id}"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "back_to_categories":
        markup = generate_categories_keyboard()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите категорию:", reply_markup=markup)
    elif call.data.startswith("cat_"):
        cat_id = call.data.split("_")[1]
        options = id_mapping[f"{cat_id}"]["options"]
        markup = types.InlineKeyboardMarkup()
        for opt_key, opt_name in options.items():
            markup.add(types.InlineKeyboardButton(opt_name, callback_data=f"opt_{cat_id}_{opt_key}"))
        markup.add(types.InlineKeyboardButton("Назад", callback_data="back_to_categories"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите опцию:", reply_markup=markup)
    elif call.data.startswith("opt_"):

        user_id = call.from_user.id
        write_request_counter(user_id)

        _, cat_id, opt_id = call.data.split("_")
        if cat_id == "cat6":  # Юридические заключения
            send_legal_conclusions(call)
        elif cat_id == "cat11":  # Лицензии
            send_licenses(call)
        elif cat_id == "cat5":
            send_insurance(call)
        elif cat_id == "cat1":
            send_poa(call)
        elif cat_id == "cat3":
            send_agreement(call)
        # elif cat_id == "cat7":
        #     send_claim(call)
        else:
            response = option_responses[f"{cat_id}"][f"{opt_id}"]
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response, reply_markup=None)

# def send_claim(call):
#     _, cat_id, opt_id = call.data.split('_')
#     claim = {
#         "opt5": get_path_file_to_send(files_to_sending["Certificate_of_Insurance"]["filename"])
#     }
#     doc_path = None

#     if opt_id in claim:
#         doc_path = claim[opt_id]

#     if doc_path:
#         try:
#             bot.delete_message(call.message.chat.id, call.message.message_id)
#             with open(doc_path, 'rb') as pdf:
#                 bot.send_document(call.message.chat.id, pdf)
#             bot.answer_callback_query(call.id, "Документ отправлен.")
#         except FileNotFoundError:
#             bot.answer_callback_query(call.id, "Файл не найден.")
#     else:
#         if opt_id == "opt1":
#             # Вывод текстового сообщения для новой опции
#             bot.delete_message(call.message.chat.id, call.message.message_id)
#             bot.send_message(call.message.chat.id, text="Проанализировать её содержание, составить проект ответа со ссылками на описание изложенного в претензии видения со своей стороны. Согласовать со своим Руководителем. Направить ответ Клиенту в срок, указанный в претензии/или Договоре.")
#         elif opt_id == "opt2":
#             bot.delete_message(call.message.chat.id, call.message.message_id)
#             bot.send_message(call.message.chat.id, text="Проанализировать её содержание, составить проект ответа со ссылками на описание изложенного в претензии видения со своей стороны. Согласовать со своим Руководителем. Направить ответ Поставщику в срок, указанный в претензии/или Договоре.")
#         elif opt_id == "opt3":
#             bot.delete_message(call.message.chat.id, call.message.message_id)
#             bot.send_message(call.message.chat.id, text="Форма типовой претензии находится в 1С ДО в закладке Главное – Файлы – Шаблоны файлов – Договорные документы, Доверенности.\n\
# Недостающая информация по тексту Претензии заполняется самостоятельно Инициатором. \n\
# При этом, необходимо учитывать порядок направления требований, указанный в Договоре с контрагентом.")
#         elif opt_id == "opt4":
#             bot.delete_message(call.message.chat.id, call.message.message_id)
#             bot.send_message(call.message.chat.id, text="Форма типовой претензии находится в 1С ДО в закладке Главное – Файлы – Шаблоны файлов – Договорные документы, Доверенности.\n\
# Недостающая информация по тексту Претензии заполняется самостоятельно Инициатором. \n\
# При этом, необходимо учитывать порядок направления требований, указанный в Договоре с контрагентом.")
#         else:
#             bot.answer_callback_query(call.id, "Неверный запрос.")

#         try:
#             bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
#         except telebot.apihelper.ApiTelegramException:
#             print("Не удалось отредактировать сообщение. Возможно, оно уже было удалено или изменено.")


def send_agreement(call):
    _, cat_id, opt_id = call.data.split('_')
    agreement = {
        # "opt8": get_path_file_to_send(files_to_sending["Certificate_of_Insurance"]["filename"]),
    }
    doc_path = None

    if opt_id in agreement:
        doc_path = agreement[opt_id]

    if doc_path:
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            with open(doc_path, 'rb') as pdf:
                bot.send_document(call.message.chat.id, pdf)
            bot.answer_callback_query(call.id, "Документ отправлен.")
        except FileNotFoundError:
            bot.answer_callback_query(call.id, "Файл не найден.")
    else:
        if opt_id == "opt1":
            # Вывод текстового сообщения для новой опции
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, text="Перечень согласованных Договоров находится в 1С ДО в закладке Главное – Файлы – Шаблоны файлов – Договорные документы, доверенности")
        elif opt_id == "opt2":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, text="1С ДО в закладке Главное – Файлы – Шаблоны файлов – Договорные документы, доверенности - Договоры с Клиентами")
        elif opt_id == "opt3":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, text="Инструкция по порядку запуска процесса \"Клиентский договор\" находится в 1С ДО в разделе - Файлы - Инструкции")
        elif opt_id == "opt4":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, text="1С ДО в закладке Главное – Файлы – Шаблоны файлов – Договорные документы, доверенности - Закупочные договорные документы")
        elif opt_id == "opt5":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, text="Согласование всех документов Компании (Договор, Дополнительное соглашение, Приложение и т.п.) осуществляется через систему 1С ДО. Для этого в системе 1С ДО заполняется карточка документа. Инструкция пользователя по работе с договорными документами находится в 1С ДО в закладке Главное – Файлы")
        elif opt_id == "opt6":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, text="Согласование всех документов Компании (Договор, Дополнительное соглашение, Приложение и т.п.) осуществляется через систему 1С ДО. Для этого в системе 1С ДО заполняется карточка документа. Инструкция пользователя по работе с договорными документами находится в 1С ДО в закладке Главное – Файлы")
        elif opt_id == "opt7":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, text="Согласование всех документов Компании (Договор, Дополнительное соглашение, Приложение и т.п.) осуществляется через систему 1С ДО. Для этого в системе 1С ДО заполняется карточка документа. Инструкция пользователя по работе с договорными документами находится в 1С ДО в закладке Главное – Файлы")
        elif opt_id == "opt8":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, text="Согласование всех документов Компании (Договор, Дополнительное соглашение, Приложение и т.п.) осуществляется через систему 1С ДО. Для этого в системе 1С ДО заполняется карточка документа. Инструкция пользователя по работе с договорными документами находится в 1С ДО в закладке Главное – Файлы")
        else:
            bot.answer_callback_query(call.id, "Неверный запрос.")

        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        except telebot.apihelper.ApiTelegramException:
            print("Не удалось отредактировать сообщение. Возможно, оно уже было удалено или изменено.")


def send_poa(call):
    _, cat_id, opt_id = call.data.split('_')
    poa = {
        "opt5": get_path_file_to_send(files_to_sending["Instruction_get_power_of_attorney"]["filename"]),
    }
    doc_path = None

    if opt_id in poa:
        doc_path = poa[opt_id]

    if doc_path:
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            with open(doc_path, 'rb') as pdf:
                bot.send_document(call.message.chat.id, pdf)
            bot.answer_callback_query(call.id, "Документ отправлен.")
        except FileNotFoundError:
            bot.answer_callback_query(call.id, "Файл не найден.")
    else:
        if opt_id == "opt1":
            # Вывод текстового сообщения для новой опции
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, text="Оформление доверенности осуществляется самостоятельно, через систему 1С ДО. Инструкция по запуску Доверенности находится в 1С ДО -  Файлы - Инструкции.")
        elif opt_id == "opt2":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, text="Необходимо САМОСТОЯТЕЛЬНО отслеживать срок действия своей Доверенности и в случае её окончания запустить доверенность на новый срок через систему 1С ДО.")
        elif opt_id == "opt3":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, text="МЧД используется для подписания электронных документов от имени Компании с помощью ЭЦП (электронно-цифровую подпись). \n\
Прежде чем получить ЭЦП на сотрудника должна быть оформлена МЧД. \n\
Для доверенностей запущенных после 01.12.2023 года в 1С ДО настроена автоматическая задача на выпуск МЧД в процессе «Доверенность». Для выпущенных ранее, в карточке доверенности, через кнопку Исполнить направить задачу Ассистенту юридического отдела на выпуск МЧД, с указанием следующей информации, без предоставления сканов: \n\
- ИНН ФЛ: \n\
- СНИЛС:  \n\
- дата рождения: \n\
- гражданство: \n\
- в какой информационной системе будут подписываться документы:\n\
- подтверждение от непосредственного руководителя, не ниже должности Регионального директора: (ДА/НЕТ). \n\
МЧД действует на срок действия доверенности выпущенной в 1С ДО, в случае, если срок действия ЭЦП закончился, а срок действия доверенности продолжает действовать, повторный выпуск МЧД не требуется, запрос направляется только на выпуск ЭЦП Специалисту по документообороту")
        elif opt_id == "opt4":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, text="Для получения сертификата ЭЦП, обратитесь к Светлане Совертковой (svetlana.sovertkova@ifcmgroup.ru) или Екатерине Мелешенко (ekaterina.meleshenko@ifcmgroup.ru)")
        else:
            bot.answer_callback_query(call.id, "Неверный запрос.")

        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        except telebot.apihelper.ApiTelegramException:
            print("Не удалось отредактировать сообщение. Возможно, оно уже было удалено или изменено.")

def send_insurance(call):
    _, cat_id, opt_id = call.data.split('_')
    insurance = {
        "opt3": get_path_file_to_send(files_to_sending["Certificate_of_Insurance"]["filename"]),
        "opt4": get_path_file_to_send(files_to_sending["Form_of_notification_about_occurrence_of_an_insured_event"]["filename"])
    }
    doc_path = None

    if opt_id in insurance:
        doc_path = insurance[opt_id]

    if doc_path:
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            with open(doc_path, 'rb') as pdf:
                bot.send_document(call.message.chat.id, pdf)
            bot.answer_callback_query(call.id, "Документ отправлен.")
        except FileNotFoundError:
            bot.answer_callback_query(call.id, "Файл не найден.")
    else:
        if opt_id == "opt1":
            # Вывод текстового сообщения для новой опции
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, text="Гражданская ответственность ООО «АЙЭФСИЭМ ГРУПП» застрахована на территории РФ. Сертификат страхования находится в 1С ДО, в закладке Главное – Файлы - Legal в папке Учредительные документы")
        elif opt_id == "opt2":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, text="При наступлении страхового случая незамедлительно уведомите ЮД и своего Руководителя об этом. С момента наступления страхового случая у Компании есть только 3 дня на уведомление о произошедшем Страховой компании.")
        else:
            bot.answer_callback_query(call.id, "Неверный запрос.")

        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        except telebot.apihelper.ApiTelegramException:
            print("Не удалось отредактировать сообщение. Возможно, оно уже было удалено или изменено.")       
            
def send_licenses(call):
    _, cat_id, opt_id = call.data.split('_')
    license = {
        "opt1": get_path_file_to_send(files_to_sending["Transportation_license"]["filename"]),
        "opt2": get_path_file_to_send(files_to_sending["License_for_maintenance_of_fire_fighting_equipment"]["filename"]),
    }
    doc_path = None

    if opt_id in license:
        doc_path = license[opt_id]

    if doc_path:
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            with open(doc_path, 'rb') as pdf:
                bot.send_document(call.message.chat.id, pdf)
            bot.answer_callback_query(call.id, "Документ отправлен.")
        except FileNotFoundError:
            bot.answer_callback_query(call.id, "Файл не найден.")
    else:
        if opt_id == "opt3":
            # Вывод текстового сообщения для новой опции
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, text="Для того, чтобы получить иную лицензию, которая может потребоваться вам в работе, прежде всего необходимо обратиться к своему Руководителю.")
        else:
            bot.answer_callback_query(call.id, "Неверный запрос.")

        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        except telebot.apihelper.ApiTelegramException:
            print("Не удалось отредактировать сообщение. Возможно, оно уже было удалено или изменено.")


# Обновленный метод send_legal_conclusions, теперь он обрабатывается в общем callback_query_handler
def send_legal_conclusions(call):
    # Разделяем данные, полученные в call.data, чтобы извлечь opt_id
    _, cat_id, opt_id = call.data.split('_')

    # Словарь с путями к документам
    legal_docs = {
        "opt1": get_path_file_to_send(files_to_sending["Prohibition_of_agency_labor"]["filename"]),
        "opt2": get_path_file_to_send(files_to_sending["Distinction_between_Lease_Agreements_and_Provision_of_Services"]["filename"]),
        "opt3": get_path_file_to_send(files_to_sending["Foreign_object_in_food"]["filename"]),
        "opt4": get_path_file_to_send(files_to_sending["Outsourcing_and_outstaffing"]["filename"]),
        "opt5": get_path_file_to_send(files_to_sending["Signing_the_agreement_backdated"]["filename"])
    }
    doc_path = None  # Значение по умолчанию для doc_path
    
    if opt_id in legal_docs:
        doc_path = legal_docs[opt_id]

    if doc_path:
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            with open(doc_path, 'rb') as doc:
                bot.send_document(call.message.chat.id, doc)
            bot.answer_callback_query(call.id, "Документ отправлен.")
        except FileNotFoundError:
            bot.answer_callback_query(call.id, "Файл не найден.")
    else:
        if opt_id == "opt6":
            # Вывод текстового сообщения для новой опции
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, text="Прежде чем направить запрос в ЮД, на предоставление юридического заключения, Вам необходимо проверить наличие заключения по Вашему запросу на Битрикс. Если такого нет – Ваш Руководитель направляет запрос на предоставление заключения в ЮД.")
        else:
            bot.answer_callback_query(call.id, "Неверный запрос.")

        try:
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        except telebot.apihelper.ApiTelegramException:
            print("Не удалось отредактировать сообщение. Возможно, оно уже было удалено или изменено.")

    


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
    btn1 = types.KeyboardButton("Инструкция")
    btn2 = types.KeyboardButton("Поддержка")
    btn_back = types.KeyboardButton("Назад")
    markup.add(btn1, btn2, btn_back)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)
   

@bot.message_handler(func=lambda message: message.text == "Инструкция")
def handle_instruction(message):
    markup = generate_main_keyboard()
    bot.send_message(message.chat.id, "Если Вам необходима оперативная поддержка в повседневной работе по наиболее часто возникающим юридическим вопросам - то этот чат-бот поможет вам получить ответ в максимально короткий срок. С наилучшими пожеланиями, Команда ЮД iFCM Group!", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Поддержка")
def handle_support(message):
    markup = generate_main_keyboard()
    bot.send_message(message.chat.id, "В случае возникновения технических вопросов по работе чат-бота, пожалуйста, обращайтесь по адресу: legalchatbot@ifcmgroup.ru", reply_markup=markup)
   
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