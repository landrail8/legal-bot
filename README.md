# Руководство по развертыванию Telegram бота ifcm
# Предварительные требования
\Чистый сервер с Ubuntu
Python версии 3.6 или выше

# Шаг 1: Подготовка сервера
Обновите пакеты вашего сервера, выполнив следующие команды:
sudo apt update
sudo apt upgrade


# Шаг 2: Установка Python и PIP
Установите Python и менеджер пакетов PIP, если они еще не установлены:
sudo apt install python3 python3-pip


# Шаг 4: Установка библиотек
Установите необходимые библиотеки через PIP:
pip install pyTelegramBotAPI
pip install sqlite3
Примечание: sqlite3 обычно предустановлен с Python, но убедитесь, что он доступен в вашей системе.

# Шаг 5: Загрузка кода бота
Загрузите код вашего бота на сервер. Это можно сделать через git, если ваш код находится в репозитории, или любым другим удобным способом.

# Шаг 5.1: Установка Git
Первым делом убедитесь, что на вашем сервере установлен git. Если нет, установите его, используя пакетный менеджер apt:
sudo apt update
sudo apt install git


# Шаг 5.2: Клонирование репозитория
Перед клонированием репозитория определитесь с директорией, куда будете клонировать проект. Перейдите в эту директорию:

cd /путь/к/директории
Теперь клонируйте репозиторий, используя команду git clone, и URL вашего репозитория. Например:

git clone https://github.com/ваш_пользователь/репозиторий_бота.git
После выполнения команды в указанной директории появится папка с именем вашего репозитория, содержащая все файлы проекта.

# Шаг 5.3: Переход в директорию проекта
После клонирования перейдите в директорию вашего проекта:
cd репозиторий_бота

# Шаг 6: Использование системы управления процессами systemd
# Шаг 6.1: Определение пользователя в системе
Первым делом необходимо определить, под каким пользователем будет запускаться бот. Это может быть ваш текущий пользователь или специально созданный пользователь для бота. Для примера используем текущего пользователя. Вы можете узнать свое имя пользователя в системе с помощью команды whoami в терминале.

# Шаг 6.2: Создание файла службы systemd
Откройте терминал и используйте текстовый редактор для создания файла службы. Например, используем nano:
sudo nano /etc/systemd/system/my_telegram_bot.service

Вставьте следующий шаблон в открывшийся текстовый редактор, заменив <your_user> на вашего пользователя системы и /path/to/your/bot.py на абсолютный путь к файлу вашего бота. Например, если ваш файл бота находится в домашнем каталоге под именем my_bot.py, путь будет выглядеть примерно так: /home/your_user/my_bot.py.

[Unit]
Description=My Telegram Bot Service
After=network.target

[Service]
User=<your_user>
WorkingDirectory=/home/<your_user>
ExecStart=/usr/bin/python3 /home/<your_user>/my_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
Сохраните изменения и закройте редактор. В nano это делается через сочетание клавиш Ctrl+O, затем Enter и Ctrl+X для выхода.

# Шаг 6.3: Включение и запуск службы
После создания файла службы включите ее, чтобы она запускалась при старте системы, и затем активируйте службу:
sudo systemctl enable my_telegram_bot.service
sudo systemctl start my_telegram_bot.service

# Шаг 6.4: Проверка статуса службы
Чтобы убедиться, что служба запущена и работает корректно, используйте команду:
sudo systemctl status my_telegram_bot.service
Эта команда покажет текущий статус службы, включая информацию о том, активна ли она и нет ли ошибок при запуске.

Примечания
Если вы внесете изменения в код бота, вам нужно будет перезапустить службу командой sudo systemctl restart my_telegram_bot.service, чтобы применить эти изменения.

# Все пути и имена пользователей в примерах нужно заменить на соответствующие вашему серверу и конфигурации.

# Шаг 7: Запуск бота

python bot.py
Где bot.py - ваш основной файл бота.
