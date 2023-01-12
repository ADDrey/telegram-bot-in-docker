# Telegram-бот в Docker [RUS]  [ENG ->]

Этот репозиторий является руководством по созданию Telegram-бота с использованием Docker.

## Первый шаг. Установите Docker Engine и Docker-Compose

(Docker Engine)[https://docs.docker.com/engine/install/ubuntu /]

(Docker-Compose)[https://docs.docker.com/compose/install/linux /]

## Второй шаг. Создайте бота с помощью @BotFather в Telegram

Используйте Telegram [Часто задаваемые вопросы](https://core.telegram.org/bots/faq#how-do-i-create-a-bot ) для бота.

## Третий шаг. Создайте образ для Docker

В переменных окружения вам нужно поместить токен API бота, а также адрес прокси-сервера и пароль для входа в него.

`TELEGRAM_API_TOKEN` — токен API бота.

`TELEGRAM_ACCESS_ID` — идентификатор учетной записи Telegram, с которой будут приниматься сообщения (сообщения от других учетных записей игнорируются).

Использование с Docker показано ниже. Предварительно заполните переменные ENV, указанные выше, в __Dockerfile__. База данных SQLite будет находиться в папке проекта 'db/finance.db'.

Откройте каталог с файлами из этого репозитория.

Создание образа и контейнера. Запуск контейнера в автономном режиме.

    docker-compose up -build -d

Остановка контейнера:

    docker-compose stop

Запуск контейнера:

    docker-compose up -d

-----------------------------------------------------------------

# Telegram Bot in Docker [ENG]
This repository is tutorial to creating Telegram Bot with using Docker.

## First Step. Install Docker Engine and Docker-Compose

(Docker Engine)[https://docs.docker.com/engine/install/ubuntu/]

(Docker-Compose)[https://docs.docker.com/compose/install/linux/]

## Second Step. Create Bot with help @BotFather in Telegram

Use Telegram [FAQ](https://core.telegram.org/bots/faq#how-do-i-create-a-bot) for Bot.

## Third Step. Build image for Docker

In the environment variables, you need to put the bot's API token, as well as the proxy address and login password to it.

  `TELEGRAM_API_TOKEN` — Bot API token.
  
  `TELEGRAM_ACCESS_ID` — ID of the Telegram account from which messages will be received (messages from other accounts are ignored).

Usage with Docker is shown below. Pre-populate the ENV variables specified above in the __Dockerfile__. The SQLite database will be located in the project folder 'db/finance.db'.

Open directory with files from this repository.

Create image and conteiner. Start conteiner in Detached mode.

    docker-compose up --build -d

Stoping conteiner:

    docker-compose stop

Strating conteiner:
  
    docker-compose up -d
