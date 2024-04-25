# Словарь с идентификаторами для категорий и опций
id_mapping = {
     "cat9": {
        "name": "Запрос в ЮД",
        "options":{
            "opt1": "Как направить запрос в ЮД?"
        }

    },

     "cat2": {
        "name": "Учредительные документы (УД)",
        "options": {
            "opt1": "Что такое учредительные документы?",
            "opt2": "Что входит в пакет УД ИП?",
            "opt3": "Что входит в пакет УД ЮЛ?",
            "opt4": "Обязательные документы от контрагента",
            "opt5": "Перечень УД iFCM Group",
            "opt6": "Где получить НЗК УД"
        }
     },
     "cat3": {
        "name": "Договоры",
        "options": {
            "opt1": "Шаблоны Договоров",
            "opt2": "Шаблоны Клиентских Договоров (КД)",
            "opt3": "Инструкция по запуску КД",
            "opt4": "Шаблоны Закупочных Договоров (ДЗ)",
            "opt5": "Согласование КД",
            "opt6": "Согласование ДС к КД",
            "opt7": "Согласование ДЗ",
            "opt8": "Согласование ДС к ДЗ",
        }
    },
    "cat4": {
        "name": "Работа с Договором. Разногласия.",
        "options": {
            "opt1": "Сторона не согласна с договором",
            "opt2": "Внесение изменений в шаблон",
            "opt3": "Где найти скан-копию Договора",
            "opt4": "Клиент прислал нам анкету на заполнение. Кто должен ее заполнять"
        }
    },
    "cat1": {
        "name": "Доверенности",
        "options": {
            "opt1": "Получение доверенности",
            "opt5": "Инструкция по получению доверенности",
            "opt2": "Перевыпуск доверенности",
            "opt3": "МЧД (машиночитаемая доверенность)",
            "opt4": "Сертификат ЭЦП"
            
        }
    },
   "cat7": {
        "name": "Претензии",
        "options": {
            "opt1": "Претензия от Клиента, что делать",
            "opt2": "Шаблон претензии Клиенту",
            "opt3": "Претензия от Поставщика, что делать",
            "opt4": "Составление претензии для Клиента",
            "opt5": "Составление претензии для Поставщика"
        }
    },
    

    
    
    "cat5": {
        "name": "Страхование",
        "options": {
            "opt1": "Что застраховано в IFCM?",
            "opt2": "Наступление страхового случая",
            "opt3": "Сертификат о страховании",
            "opt4": "Форма наступления страхового случая"
        }
    },
    "cat6": {
        "name": "Юридические заключения",
        "options": {
            "opt1": "Запрет заемного труда",
            "opt2": "Договоры аренды и оказания услуг",
            "opt3": "Посторонний предмет в пище",
            "opt4": "Аутсорсинг и аутстаффинг",
            "opt5": "Подписание договора «задним числом»",
            "opt6": "ЮЗ нет в списке"
        }
    },
    "cat11": {
        "name": "Лицензии",
        "options": {
            "opt1": "Лицензия на перевозки",
            "opt2": "Лицензия на обслуживание противопожарного оборудования",
            "opt3": "Иная лицензия"
        }
    },
    "cat8": {
        "name": "Перевод документов",
        "options": {
            "opt1": "Перевод двуязычного договора",
        }
    },
    "cat12": {
        "name": "Другое",
        "options": {
            "opt1": "У меня нет доступа в 1С ДО, Битрикс",
            "opt2": "Кому из работников ЮД направлять запрос",
            "opt3": "Корпоративная информация о компании",
            "opt4": "Карточка компании",
            "opt5": "Где взять выписку ЕГРЮЛ",
            "opt6": "Где взять выписку ЕГРН"
        }
    }
}

# Словарь с ответами на каждую опцию
option_responses = {
    "cat2": {
        "opt1": "Документы, на основании которых действует Юридическое лицо.",
        "opt2": "1. Паспорт физического лица;\n\
2. Свидетельство о государственной регистрации физического лица в качестве индивидуального предпринимателя;\n\
3. Выписка из Единого Государственного Реестра индивидуальных предпринимателей (ЕГРИП); \n\
4. Уведомление о постановке на учет физического лица в налоговом органе. ",
        "opt3": "1. выписка из ЕГРЮЛ;\n\
2. Устав\n\
3. Свидетельство о государственной регистрации юридического лица (свидетельство ОГРН); \n\
4. Свидетельство о постановке на учет в налоговом органе и о присвоении идентификационного номера налогоплательщика (свидетельство ИНН); \n\
5. Протокол о назначении генерального директора/решения о назначении генерального директора/протокола о продлении полномочий; \n\
6. В случае подписания Договора лицом, действующим на основании доверенности – доверенность; \n\
7. Иные документы. ",
        "opt4": "Учредительные документы. Лицензия (если услуга/работа лицензируется). Согласие на обработку персональных данных (при заключении Договора с ИП). Иные документы.",
        "opt5": "Скан-копии учредительных документов находятся в 1С ДО, в закладке Главное – Файлы - Legal в папке Учредительные документы",
        "opt6": "Инициатор запроса обязан уточнить у Контрагента возможность предоставления копий учредительных документов, заверенных Руководителем компании (их подготовкой Инициатор занимается самостоятельно). \n\
В случае необходимости предоставления именно нотариально-заверенных копий учредительных документов, Инициатор запроса, обязан заблаговременно (за 3 рабочих дня) до даты их предоставления, направить в ЮД запрос об их подготовке.",


    },
    "cat4": {
        "opt1": "В случае если переговоры и изменение текста Договора невозможны, используется Протокол разногласий,\n\
в котором отражаются редакции договорных пунктов, приемлемых в конечном итоге для обеих Сторон.\n\
Владельцем процесса в подготовке Протокола разногласий по проектам в части заполнения преамбулы, внесения реквизитов, даты и других условий является Инициатор. \n\
ЮД предоставляет описание юридически значимых рисков проекта, которые Инициатор вносит в Протокол разногласий самостоятельно. \n\
Проект Протокола разногласий находится в 1С ДО в закладке Главное – Файлы – Шаблоны файлов – Договорные документы, Доверенности",
        "opt2": "Типовые шаблоны Договоров разблокировке не подлежат. Изменения в шаблон вносятся через Протокол разногласий. В случае вы столкнетесь с «непреодолимыми» разногласиями контрагентов (клиентов) по поводу внесения изменений в \"тело\" Договора, а не составления Протокола, то Договор может быть разблокирован только в режиме правок.",
        "opt3": "Скан-копия Договора должна быть запрошена у менеджера соответствующего проекта. Также скан-копии Договора находятся в 1С ДО в карточке Договора.",
        "opt4": "Анкета контрагента заполняется самостоятельно Инициатором, основные данные для Анкеты берутся из Карточки ООО «АЙЭФСИЭМ ГРУПП», а также из документа Выписка из ЕГРЮЛ."
    },
    "cat8": {
        "opt1": "ЮД предоставляет правки на языке исходной версии. \n\
В случае, если документ представляет собой двуязычную форму, ЮД предоставляет правки на языке превалирующей редакции документа.\n\
Держателем процесса перевода на язык необходимой редакции является Инициатор (при помощи собственных ресурсов или сторонних - обращение в агентство переводов).",
          },

    "cat9": {
        "opt1": "Любой запрос в Юридический департамент направляется только на общий адрес департамента: legaldepartment@ifcmgroup.ru.\n\
Для запросов Operations - только с указанием ответственного операционного директора кластера в теме письма.\n\
Запросы без указания ответственного операционного директора кластера не рассматриваются"
    },

    "cat7": {
        "opt1": "Проанализировать её содержание, составить проект ответа со ссылками на описание изложенного в претензии видения со своей стороны. Согласовать со своим Руководителем. Направить ответ Клиенту в срок, указанный в претензии/или Договоре.",
        "opt2": "Типовая форма Претензии Клиенту за неоплату услуг iFCM находится в процессе \"Исходящая претензия\", который запускается через \"Создание внутреннего документа\" в 1С ДО. Инструкция по запуску процесса находится в разделе Главное - Файлы - Инструкции - Документы ЮД",
        "opt3": "Проанализировать её содержание, составить проект ответа со ссылками на описание изложенного в претензии видения со своей стороны. Согласовать со своим Руководителем. Направить ответ Поставщику в срок, указанный в претензии/или Договоре",
        "opt4": "Форма типовой претензии находится в 1С ДО в закладке Главное – Файлы – Шаблоны файлов – Договорные документы, Доверенности.\n\
Недостающая информация по тексту Претензии заполняется самостоятельно Инициатором. \n\
При этом, необходимо учитывать порядок направления требований, указанный в Договоре с контрагентом",
        "opt5": "Форма типовой претензии находится в 1С ДО в закладке Главное – Файлы – Шаблоны файлов – Договорные документы, Доверенности.\n\
Недостающая информация по тексту Претензии заполняется самостоятельно Инициатором. \n\
При этом, необходимо учитывать порядок направления требований, указанный в Договоре с контрагентом",
    },
    
    "cat12": {
        "opt1": "В случае, если у вас отсутствует доступ к 1С ДО, Битрикс вам нужно обратиться HelpDesk",
        "opt2": "Любой запрос в Юридический департамент направляется только на общий адрес департамента: legaldepartment@ifcmgroup.ru.\n\
Для запросов Operations - только с указанием ответственного Операционного директора Кластера в теме письма.\n\
Запросы без указания ответственного операционного директора кластера не рассматриваются",
        "opt3": "iFCM Group (integrated Facility and Catering Management Group) – компания, \n\
        стартовавшая на российском рынке в 1993 году как представительство Sodexo. До \n\
        2002 года деятельность Компании осуществлялась через ЗАО «Содексо АО», а с \n\
        2002 года, через ООО «Содексо ЕвроАзия». С 4 мая 2022 года, Решением \n\
        Единственного участника ООО «Содексо ЕвроАзия», произошло переименование Компании на Общество с ограниченной ответственностью «АЙЭФСИЭМ ГРУПП». \n\
        Информация по бенефициарам Компании, находится в 1С ДО в закладке Главное – Файлы – Legal – Учредительные документы",
        "opt4": "Карточка компании находится в 1С ДО в закладке Главное – Файлы – Legal – Учредительные документы.",
        "opt5": "Выписка из ЕГРЮЛ/ ЕГРИП (Единый Государственный Реестр Юридических Лиц/Индивидуальных Предпринимателей) — это документ, в котором указана достоверная информация о юр.лице или ИП из реестра налогового органа. Выписки можно получить в открытом источнике https://egrul.nalog.ru/index.html. ",
        "opt6": "Выписка из Единого государственного реестра недвижимости (ЕГРН), содержит информацию о собственнике и характеристиках объекта, наличии или отсутствии ограничений, обременений и другие полезные сведения об объекте недвижимости. В случае, направления на согласование в ЮД договора аренды недвижимого имущества, в обязательном порядке предоставлять Выписку из ЕГРН на актуальную дату. Срок действия выписки 30 календарных дней. Собственник недвижимого имущества может запросить выписку из ЕГРН онлайн бесплатно. Несобственник может получить сведения о чужом объекте недвижимости с персональными данными правообладателя, запросив у него:\n\
- цифровую онлайн-выписку, подлинность которой можно проверить\n\
- согласие на предоставление данных о недвижимости другим людям и организациям, чтобы получить выписку самостоятельно\n\
- бумажную выписку, заверенную печатью"}

}


files_to_sending = {
  "Outsourcing_and_outstaffing": {
    "name": "Аутсорсинг и аутстаффинг",
    "filename": "Аутсорсинг и аутстаффинг.doc"
  },
  "Instruction_get_power_of_attorney": {
    "name": "Инструкция по получению доверенности",
    "filename": "Инструкция по получению доверенности.pdf"
  },
  "Prohibition_of_agency_labor": {
    "name": "Запрет заемного труда",
    "filename": "Запрет заемного труда.doc"
  },
  "Transportation_license": {
    "name": "Лицензия на перевозки",
    "filename": "Лицензия на перевозки.pdf"
  },
  "License_for_maintenance_of_fire_fighting_equipment": {
    "name": "Лицензия_на_обслуживание_противопожарного_оборудования",
    "filename": "Лицензия_на_обслуживание_противопожарного_оборудования.pdf"
  },
  "Signing_the_agreement_backdated": {
    "name": "Подписание_договора_задним_числом",
    "filename": "Подписание_договора_задним_числом.doc"
  },
  "Foreign_object_in_food": {
    "name": "Посторонний предмет в пище",
    "filename": "Посторонний предмет в пище.doc"
  },
  "Distinction_between_Lease_Agreements_and_Provision_of_Services": {
    "name": "Разграничение_договоров_аренды_и_оказания_услуг",
    "filename": "Разграничение_договоров_аренды_и_оказания_услуг.doc"
  },
  "Certificate_of_Insurance": {
    "name": "Сертификат о страховании",
    "filename": "Сертификат о страховании.pdf"
  },
  "Form_of_notification_about_occurrence_of_an_insured_event": {
    "name": "Форма_уведомления_о_наступлении_страхового_случая",
    "filename": "Форма_уведомления_о_наступлении_страхового_случая.doc"
  },
}




def get_path_file_to_send(filepath):
  return files_to_sending_dir + "/" + filepath

files_to_sending_dir = '/workdir/data/files' # '/var/lib/sqlite/data/files'
# def init_files_to_sending_dir():
#   # Check if the file exists
#   if not os.path.exists(files_to_sending_dir):
#     os.mkdir(files_to_sending_dir)
#     print("files_to_sending_dir created successfully.")
#   else:
#     print("files_to_sending_dir already exists.")
