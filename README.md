# Telegram-бот в Docker [RUS]  [ENG ->]

Этот репозиторий является руководством по созданию Telegram-бота с использованием Docker.

Вдохновлялся кодом из [этого](https://github.com/alexey-goloburdin/telegram-finance-bot) (https://github.com/alexey-goloburdin/telegram-finance-bot) репозитория.

## Первый шаг. Установите Docker Engine и Docker-Compose

[Docker Engine](https://docs.docker.com/engine/install/ubuntu/)

[Docker-Compose](https://docs.docker.com/compose/install/linux/)

## Второй шаг. Создайте бота с помощью @BotFather в Telegram

Используйте Telegram [Часто задаваемые вопросы](https://core.telegram.org/bots/faq#how-do-i-create-a-bot ) для бота.

## Третий шаг. Создайте образ для Docker

В переменных окружения вам нужно поместить токен API бота, а также адрес прокси-сервера и пароль для входа в него.

`TELEGRAM_API_TOKEN` — токен API бота.

`TELEGRAM_ACCESS_ID` — идентификатор учетной записи Telegram, с которой будут приниматься сообщения (сообщения от других учетных записей игнорируются).

Использование с Docker показано ниже. Предварительно заполните переменные ENV, указанные выше, в __Dockerfile__. База данных SQLite будет находиться в папке проекта 'db/finance.db'.

Откройте каталог с файлами из этого репозитория.

Создание образа:

    docker build --force-rm --no-cache -t [image_name] [PATH_to_Dockerfile]
    # --force-rm - удаление всех промежуточных образов после сборки своего образа.
    # --no-cache - игнорирование кэша от редыдущих сборок, помогает при пересборке.
    # -t - настройка имени для образа в самом Docker вписываем вместо [image_name].
    # [PATH_to_Dockerfile] - путь до файла с инструкциями Dockerfile.

Создание и Запуск контейнера:

    docker run -d --name tgbot -v ./db:/home/db --restart unless-stopped [image_name]
    
Создание БД в контейнере:

    docker exec -ti tgbot bash
    sqlite3 /home/db/finance.db
    CTRL+C
    CTRL+C
    CTRL+C
    exit

Остановка контейнера:

    docker stop tgbot

-----------------------------------------------------------------

# Telegram Bot in Docker [ENG]

This repository is tutorial to creating Telegram Bot with using Docker.

Inspired by code from [this](https://github.com/alexey-goloburdin/telegram-finance-bot) (https://github.com/alexey-goloburdin/telegram-finance-bot) repository.

## First Step. Install Docker Engine and Docker-Compose

[Docker Engine](https://docs.docker.com/engine/install/ubuntu/)

[Docker-Compose](https://docs.docker.com/compose/install/linux/)

## Second Step. Create Bot with help @BotFather in Telegram

Use Telegram [FAQ](https://core.telegram.org/bots/faq#how-do-i-create-a-bot) for Bot.

## Third Step. Build image for Docker

In the environment variables, you need to put the bot's API token, as well as the proxy address and login password to it.

  `TELEGRAM_API_TOKEN` — Bot API token.
  
  `TELEGRAM_ACCESS_ID` — ID of the Telegram account from which messages will be received (messages from other accounts are ignored).

Usage with Docker is shown below. Pre-populate the ENV variables specified above in the __Dockerfile__. The SQLite database will be located in the project folder 'db/finance.db'.

Open directory with files from this repository.

Image Creation:

    docker build --force-rm --no-cache -t [image_name] [PATH_to_Dockerfile]
    # -force-rm - Removes all intermediate images after building your image.
    # -no-cache - ignoring the cache from the redirecting builds, helps with re-collection.
    # -t - configure the name for the image in the docker, enter instead of [image_name].
    # [PATH_to_Dockerfile] is the path to the Dockerfile.

Build and Start the container:

    docker run -d --name tgbot -v ./db:/home/db --restart unless-stopped [image_name]
    
Create DB in the container:

    docker exec -ti tgbot bash
    sqlite3 /home/db/finance.db
    CTRL+C
    CTRL+C
    CTRL+C
    exit

Container stop:

    docker stop [container_id]
