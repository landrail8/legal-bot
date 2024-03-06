import telebot
from telebot import types
import sqlite3
from telebot.types import ReplyKeyboardRemove
# bot_token = "6342689121:AAHP-iNYCgICjCsQo6mpbMvhdBBKABvJYYc" # PROD
bot_token = "7174920362:AAHGyz8DH0PDBI2UYxW4en7qee5UsgJq2X0" # DEV
bot = telebot.TeleBot(bot_token)

# Словарь с идентификаторами для категорий и опций
id_mapping = {
    "cat1": {
        "name": "Доверенности",
        "options": {
            "opt1": "Я хочу получить доверенность",
            "opt2": "Я хочу переоформить доверенность"
        }
    },
    "cat2": {
        "name": "Учредительные документы и документы о Компании",
        "options": {
            "opt1": "Что такое учредительные документы",
            "opt2": "Что входит в пакет учредительных документов ИП",
            "opt3": "Что входит в пакет учредительных документов Юридического лица",
            "opt4": "Какие документы я обязательно должен получить от контрагента для заключения Договора",
            "opt5": "Где я могу учредительные документы iFCM Group",
            "opt6": "Где я могу получить нотариально-заверенные копии учредительных документов",
            "opt7": "Я хочу получить корпоративную информацию о компании",
            "opt8": "Я хочу получить карточку компании",
            "opt9": "Что такое ЕГРЮЛ и зачем нужна выписка оттуда",
            "opt10": "Где и как я могу получить выписку из ЕГРН",
            "opt11": "Что такое ЕГРН и зачем нужна выписка оттуда"
        }
    },
    "cat3": {
        "name": "Договоры",
        "options": {
            "opt1": "Мне нужен шаблон Договора",
            "opt2": "Шаблоны Клиентских Договоров",
            "opt3": "Шаблоны Закупочных Договоров",
            "opt4": "Как мне согласовать Клиентский Договор",
            "opt5": "Как мне согласовать Дополнительное соглашение к Клиентскому Договору",
            "opt6": "Как мне согласовать Закупочный Договор",
            "opt7": "Как мне согласовать Дополнительное соглашение к Закупочному Договору"
        }
    },
    "cat4": {
        "name": "Работа с Договором. Протокол разногласий.",
        "options": {
            "opt1": "Сторона не согласна с Договором – мне нужен протокол разногласий",
            "opt2": "Почему все шаблоны заблокированы от правок. Кто может изменить шаблон",
            "opt3": "Где я могу найти скан-копию Договора"
        }
    },
    "cat5": {
        "name": "Страхование",
        "options": {
            "opt1": "IFCM застраховано? Что застраховано в IFCM",
            "opt2": "Заказчик прислал нам анкету на заполнение. Кто должен ее заполнять"
        }
    },
    "cat6": {
        "name": "Юридические заключения",
        "options": {
            "opt1": "Я хочу получить юридическое заключение по вопросу"
        }
    },
    "cat7": {
        "name": "Претензии",
        "options": {
            "opt1": "Мне пришла претензия от Клиента, что делать",
            "opt2": "Мне пришла претензия от Поставщика, что делать",
            "opt3": "Мне нужно составить претензию Клиенту, как это сделать",
            "opt4": "Мне нужно составить претензию Поставщику, как это сделать"
        }
    },
    "cat8": {
        "name": "Перевод документов",
        "options": {
            "opt1": "У меня двуязычный Договор, кто должен переводить?",
            "opt2": "У меня нет доступа в 1С ДО, Битрикс",
            "opt3": "Кому из работников ЮД направлять запрос"
        }
    }
}

# Словарь с ответами на каждую опцию
option_responses = {
    "cat1": {
        "opt1": "Оформление доверенности осуществляется самостоятельно, через систему 1С ДО.",
        "opt2": "Вам необходимо САМОСТОЯТЕЛЬНО отслеживать срок действия своей Доверенности и в случае её окончания, запустить доверенность на новый срок через систему 1С ДО. Процесс запуска Доверенности описан в п.1.1 L/I-001: LEGAL FAQ."
    },
    "cat2": {
        "opt1": "Документы, на основании которых действует Юридическое лицо.",
        "opt2": "1. Паспорт физического лица;\n\
2. Свидетельство о государственной регистрации физического лица в качестве индивидуального предпринимателя; \n\
3. Выписка из Единого Государственного Реестра индивидуальных предпринимателей (ЕГРИП); \n\
4. Уведомление о постановке на учет физического лица в налоговом органе. ",
        "opt3": "1. выписка из ЕГРЮЛ;\n\
2. устав\n\
3. свидетельство о государственной регистрации юридического лица (свидетельство ОГРН); \n\
4. свидетельство о постановке на учет в налоговом органе и о присвоении идентификационного номера налогоплательщика (свидетельство ИНН); \n\
5. протокол о назначении генерального директора/решения о назначении генерального директора/протокола о продлении полномочий; \n\
6. в случае подписания Договора лицом, действующим на основании доверенности – доверенность; \n\
7. иные документы. ",
        "opt4": "Учредительные документы. Лицензия (если услуга/работа лицензируется). Согласие на обработку персональных данных (при заключении Договора с ИП). Иные документы.",
        "opt5": "Скан-копии учредительных документов находятся в 1С ДО, в закладке Главное – Файлы - Legal в папке Учредительные документы",
        "opt6": "Инициатор запроса обязан уточнить у Контрагента возможность предоставления копий учредительных документов, заверенных Руководителем компании (их подготовкой Инициатор занимается самостоятельно). \n\
В случае необходимости предоставления именно нотариально-заверенных копий учредительных документов, Инициатор запроса, обязан заблаговременно (за 3 рабочих дня) до даты их предоставления, направить в ЮД запрос об их подготовке.",
        "opt7": "iFCM Group (integrated Facility and Catering Management Group) – компания, стартовавшая на российском рынке в 1993 году как представительство Sodexo. До 2002 года деятельность Компании осуществлялась через ЗАО «Содексо АО», а с 2002 года, через ООО «Содексо ЕвроАзия». С 4 мая 2022 года, Решением Единственного участника ООО «Содексо ЕвроАзия», произошло переименование Компании на Общество с ограниченной ответственностью «АЙЭФСИЭМ ГРУПП». \n\
Информация по бенефициарам Компании, находится в 1С ДО в закладке Главное – Файлы – Legal – Учредительные документы",
        "opt8": "Карточка компании находится в 1С ДО в закладке Главное – Файлы – Legal – Учредительные документы.",
        "opt9": "Выписка из ЕГРЮЛ/ ЕГРИП (Единый Государственный Реестр Юридических Лиц/Индивидуальных Предпринимателей) — это документ, в котором указана достоверная информация о юр.лице или ИП из реестра. ",
        "opt10": "Выписку из ЕГРН можно получить в Росреестре или через портал госуслуг.",
        "opt11": "Выписка из Единого государственного реестра недвижимости (ЕГРН), содержит информацию о собственнике и характеристиках объекта, наличии или отсутствии ограничений, обременений и другие полезные сведения об объекте недвижимости. В случае, направления на согласование в ЮД договора аренды недвижимого имущества, в обязательном порядке предоставлять Выписку из ЕГРН на актуальную дату. Срок действия выписки 30 календарных дней."
    },
    "cat3": {
        "opt1": "Перечень согласованных Договоров находится в 1С ДО в закладке Главное – Файлы – Шаблоны файлов – Договорные документы, доверенности.",
        "opt2": "1С ДО в закладке Главное – Файлы – Шаблоны файлов – Договорные документы, доверенности - Договоры с Клиентами",
        "opt3": "1С ДО в закладке Главное – Файлы – Шаблоны файлов – Договорные документы, доверенности - Закупочные договорные документы",
        "opt4": "Согласование всех документов Компании (Договор, Дополнительное соглашение, Приложение и т.п.) осуществляется через систему 1С ДО. Для этого в системе 1С ДО заполняется карточка документа. Инструкция пользователя по работе с договорными документами находится в 1С ДО, в закладке Главное – Файлы.",
        "opt5": "Согласование всех документов Компании (Договор, Дополнительное соглашение, Приложение и т.п.) осуществляется через систему 1С ДО. Для этого в системе 1С ДО заполняется карточка документа. Инструкция пользователя по работе с договорными документами находится в 1С ДО, в закладке Главное – Файлы.",
        "opt6": "Согласование всех документов Компании (Договор, Дополнительное соглашение, Приложение и т.п.) осуществляется через систему 1С ДО. Для этого в системе 1С ДО заполняется карточка документа. Инструкция пользователя по работе с договорными документами находится в 1С ДО, в закладке Главное – Файлы",
        "opt7": "Согласование всех документов Компании (Договор, Дополнительное соглашение, Приложение и т.п.) осуществляется через систему 1С ДО. Для этого в системе 1С ДО заполняется карточка документа. Инструкция пользователя по работе с договорными документами находится в 1С ДО, в закладке Главное – Файлы."
    },
    "cat4": {
        "opt1": "В случае, если переговоры и изменение текста Договора невозможны – используется Протокол разногласий. В нем отражаются редакции договорных пунктов, приемлемых в конечном итоге, для обеих Сторон. \n\
Владельцем процесса в подготовке Протокола разногласий по проектам, в части заполнения преамбулы, внесения реквизитов, даты и других условий является Инициатор. \n\
ЮД предоставляет описание юридически значимых рисков проекта, которые Инициатор вносит в Протокол разногласий самостоятельно. \n\
Проект Протокола разногласий находится в 1С ДО в закладке Главное – Файлы – Шаблоны файлов – Договорные документы, Доверенности.",
        "opt2": "Типовые шаблоны Договоров разблокировке не подлежат. Изменения в шаблон вносятся через Протокол разногласий. В случае, вы столкнетесь с «непреодолимыми» разногласиями с контрагентами (клиентами), по поводу внесения изменений в тело Договора, а не составления Протокола, то Договор может быть разблокирован только в режиме правок.",
        "opt3": "Скан копия Договора должна быть запрошена у менеджера соответствующего проекта. Также скан-копии Договора находится в 1С ДО в карточке Договора."
    },
        "cat5": {
        "opt1": "Гражданская ответственность ООО «АЙЭФСИЭМ ГРУПП» застрахована на территории РФ. Сертификат страхования находится в 1С ДО, в закладке Главное – Файлы - Legal в папке Учредительные документы.",
        "opt2": "Анкета контрагента заполняется самостоятельно Инициатором, основные данные для Анкеты берутся из Карточки ООО «АЙЭФСИЭМ ГРУПП», из документа Выписка из ЕГРЮЛ."
    },
    "cat6": {   
        "opt1": "Прежде чем направить запрос в ЮД, на предоставление юридического заключения, Вам необходимо проверить наличие заключения по Вашему запросу на Битрикс. Если такого нет – Ваш Руководитель направляет запрос в ЮД."
    },
    "cat7": {
        "opt1": "Проанализировать её содержание, составить проект ответа со ссылками на описание изложенного в претензии видения со своей стороны. Согласовать со своим Руководителем. Направить ответ Клиенту в срок, указанный в претензии/или Договоре.",
        "opt2": "Проанализировать её содержание, составить проект ответа со ссылками на описание изложенного в претензии видения со своей стороны. Согласовать со своим Руководителем. Направить ответ Поставщику в срок, указанный в претензии/или Договоре.",
        "opt3": "Форма типовой претензии находится в 1С ДО в закладке Главное – Файлы – Шаблоны файлов – Договорные документы, Доверенности.\n\
Недостающая информация по тексту Претензии заполняется самостоятельно Инициатором. \n\
При этом, необходимо учитывать порядок направления требований, указанный в Договоре с контрагентом.",
        "opt4": "Форма типовой претензии находится в 1С ДО в закладке Главное – Файлы – Шаблоны файлов – Договорные документы, Доверенности.\n\
Недостающая информация по тексту Претензии заполняется самостоятельно Инициатором. \n\
При этом, необходимо учитывать порядок направления требований, указанный в Договоре с контрагентом."
    },
    "cat8": {
        "opt1": "ЮД предоставляет правки на языке исходной версии. \n\
В случае, если документ представляет собой двуязычную форму, ЮД, предоставляет правки на языке, превалирующей редакции документа.\n\
Держателем процесса перевода на язык необходимой редакции, является Инициатор (при помощи собственных ресурсов или сторонних - обращение в агентство переводов).",
        "opt2": "В случае, если у вас отсутствует доступ к 1С ДО, Битрикс вам нужно обратиться в HelpDesk.",
        "opt3": "Любой запрос в Юридический департамент направляется только на общий адрес департамента: legaldepartment@ifcmgroup.ru. \n\
Для запросов Operations - только с указанием ответственного операционного директора кластера в теме письма. \n\
Запросы без указания ответственного операционного директора кластера не рассматриваются."
    }

}

def init_db():
    conn = sqlite3.connect('/Users/viacheslavpetrov/Desktop/code2/users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            is_authorized INTEGER DEFAULT 0
        );
    ''')
    conn.commit()
    conn.close()




# Добавление или обновление пользователя в базе данных
def add_or_update_user(chat_id):
    print("Let's fix it!")
    # conn = sqlite3.connect('/Users/viacheslavpetrov/Desktop/code2/users.db')
    # cursor = conn.cursor()
    # try:
    #     # Использование плейсхолдеров для username и password
    #     cursor.execute("INSERT OR IGNORE INTO users (chat_id, username, password, is_authorized) VALUES (?, '', '', 0)", (chat_id,))
    #     conn.commit()
    #     print("User added/updated successfully")
    # except Exception as e:
    #     print(f"Error adding/updating user: {e}")
    # finally:
    #     conn.close()



# Функция авторизации пользователя
def authorize_user(username, password, chat_id):
    print("Let's fix it!")
    # conn = sqlite3.connect('/Users/viacheslavpetrov/Desktop/code2/users.db')
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    # user = cursor.fetchone()
    # if user:
    #     cursor.execute("UPDATE users SET chat_id = ?, is_authorized = 1 WHERE username = ?", (chat_id, username))
    #     conn.commit()
    #     result = True
    # else:
    #     result = False
    # conn.close()
    # return result
    return True

# Проверка, авторизован ли пользователь
def is_user_authorized(chat_id):
    # conn = sqlite3.connect('/Users/viacheslavpetrov/Desktop/code2/users.db')
    # cursor = conn.cursor()
    # cursor.execute("SELECT is_authorized FROM users WHERE chat_id = ?", (chat_id,))
    # result = cursor.fetchone()
    # conn.close()
    # return result[0] == 1 if result else False
    return True

def add_or_update_user_phone_and_username(chat_id, phone_number):
    print("Let's fix it!")
    # conn = sqlite3.connect('/Users/viacheslavpetrov/Desktop/code2/users.db')
    # cursor = conn.cursor()
    # # Обновляем username, phone_number и устанавливаем пароль 1111 для данного chat_id
    # cursor.execute("""
    #     UPDATE users 
    #     SET phone_number = ?, username = ?, password = '1111'
    #     WHERE chat_id = ?""", (phone_number, phone_number, chat_id))
    # conn.commit()
    # conn.close()



# Функция для генерации клавиатуры с категориями
def generate_categories_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    for cat_id, cat_data in id_mapping.items():
        markup.add(types.InlineKeyboardButton(cat_data["name"], callback_data=f"cat_{cat_id}"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    add_or_update_user(chat_id)  # Добавляем пользователя при первом обращении
    welcome_text = "Добро пожаловать! Чат-бот активирован. \nДля продолжения работы нажмите на кнопку \"Инструкция\" \nВ инструкции вы найдёте описание шагов для регистрации и работы в чат-боте Eagle."
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton("Инструкция")
    markup.add(button1)
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)
   

@bot.message_handler(func=lambda message: message.text.lower() == "привет")
def greet(message):
    send_welcome(message)

@bot.message_handler(content_types=['contact']) #func=lambda message: message.text == "Авторизация")
# def request_login(message):
#     msg = bot.send_message(message.chat.id, "Введите ваш логин и пароль через пробел.", reply_markup=ReplyKeyboardRemove())
#     bot.register_next_step_handler(msg, process_login_password)
def process_login_password(message):
    try:
        # username, password = message.text.split(" ", 1)
        # if authorize_user(username, password, message.chat.id):
            # bot.send_message(message.chat.id, "Вы успешно авторизованы.")
            # Создаем клавиатуру после успешной авторизации
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            button4 = types.KeyboardButton("Инструкция по пользованию")
            button1 = types.KeyboardButton("Вопросы")
            button3 = types.KeyboardButton("Поддержка")
            markup.add(button1, button3, button4)
            bot.send_message(message.chat.id, "Выберите один из пунктов меню:", reply_markup=markup)
        # else:
        #     bot.send_message(message.chat.id, "Неверный логин или пароль. Пожалуйста, попробуйте снова.")
        #     # Запрашиваем логин и пароль заново
        #     msg = bot.send_message(message.chat.id, "Введите ваш логин и пароль через пробел.")
        #     bot.register_next_step_handler(msg, process_login_password)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите логин и пароль корректно.")
        # Запрашиваем логин и пароль заново
        msg = bot.send_message(message.chat.id, "Введите ваш логин и пароль через пробел.")
        bot.register_next_step_handler(msg, process_login_password)



@bot.message_handler(func=lambda message: message.text == "Вопросы")
def show_questions(message):
    if is_user_authorized(message.chat.id):
        bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=generate_categories_keyboard())
    else:
        bot.send_message(message.chat.id, "Эта функция доступна только после авторизации. Используйте кнопку 'Авторизация'.")
    
@bot.message_handler(func=lambda message: message.text == "Инструкция")
def request_phone(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = types.KeyboardButton("Отправить номер телефона", request_contact=True)
    markup.add(btn)
    bot.send_message(message.chat.id, "Нажмите на кнопку \"Отправить номер телефона\". \nЭто предоставит чат-боту возможность предложить авторизовать вас.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Инструкция по пользованию")
def send_message(message):
    msg = bot.send_message(message.chat.id, "Вот базовая инструкция.")

@bot.message_handler(func=lambda message: message.text == "Поддержка")
def send_message(message):
    msg = bot.send_message(message.chat.id, "Функция еще дорабатывается.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("cat_"))
def category_callback(call):
    cat_id = call.data.split("_")[1]
    markup = types.InlineKeyboardMarkup()
    options = id_mapping[cat_id]["options"]
    for opt_id, opt_name in options.items():
        markup.add(types.InlineKeyboardButton(opt_name, callback_data=f"opt_{cat_id}_{opt_id}"))
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back_to_categories"))
    bot.edit_message_text("Выберите опцию:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


# @bot.message_handler(content_types=['contact'])
# def contact_handler(message):
#     phone_number = message.contact.phone_number
#     chat_id = message.chat.id
#     # add_or_update_user_phone_and_username(chat_id, phone_number)
#     bot.send_message(chat_id, "Отлично! Теперь вам необходимо авторизоваться, \n\
# Это предоставит Вам возможность полноценно пользоваться функционалом чат-бота. \n\
# Для прохождения авторизации, нажмите «Авторизация» и введите в поле сообщения ваш логин: \n\
# – это ваш номер телефона без + в начале, и пароль, который вы получили в информационном письме на адрес вашей корпоративной электронной почте. ")
#     markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
#     button2 = types.KeyboardButton("Авторизация")
#     markup.add(button2)
#     bot.send_message(message.chat.id, "Теперь пройдите авторизацию, для этого нажмите на кнопку \"Авторизация\"", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "back_to_categories")
def back_to_categories(call):
    bot.edit_message_text("Выберите категорию:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=generate_categories_keyboard())

@bot.callback_query_handler(func=lambda call: call.data.startswith("opt_"))
def option_callback(call):
    _, cat_id, opt_id = call.data.split("_")
    # Получаем ответ, соответствующий выбранной опции
    response = option_responses[cat_id][opt_id]
    bot.edit_message_text(text=response, chat_id=call.message.chat.id, message_id=call.message.message_id)

# init_db()

bot.polling(none_stop=True)
