# Work Environment
- git
- make 
- docker (compose)

# Local development
1. check .env.production - bot token should be from ifcmlocaldev_bot
2. make up

# Prod deploy
1. check .env.production - bot token should be from iFCMlegal_bot
2. make up

# User manual

## Статистика использования
хранится на хост-машине /var/lib/docker/volumes/ в папке `eaglebot_eaglebot_data`
чтобы ее посмотреть надо перенести и открыть файл, например sqlite explorer in VScode


## Файлы, которые посылает бот по запросу пользователя
### Хранилище файлов
[disk.yandex](https://disk.yandex.ru/d/pAbEemDwF2LsXA)
### Требования к файлам
Вместо .docx нужен формат .doc
Почему-то .docx дает ошибку при отправке "Файл не найден"