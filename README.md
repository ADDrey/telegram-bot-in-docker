# Telegram Bot in Docker
This repository is tutorial to creating Telegram Bot with using Docker.

## First Step. Create Docker Repository

Create Repository in Docker Hub.
In next time you can clone this repository.

## Second Step. Install Docker Engine and Docker-Compose

(Docker Engine)[https://docs.docker.com/engine/install/ubuntu/]

(Docker-Compose)[https://docs.docker.com/compose/install/linux/]

## Third Step. Create Bot with help @BotFather in Telegram

Use Telegram [FAQ](https://core.telegram.org/bots/faq#how-do-i-create-a-bot) for Bot

## Fourth Step. Build image for Docker

In the environment variables, you need to put the bot's API token, as well as the proxy address and login password to it.

  `TELEGRAM_API_TOKEN` # — Bot API token
  `TELEGRAM_ACCESS_ID` # — ID of the Telegram account from which messages will be received (messages from other accounts are ignored)

Usage with Docker is shown below. Pre-populate the ENV variables specified above in the __Dockerfile__. The SQLite database will be located in the project folder `db/finance.db'.

Open directory with files from this repository.

Create image and conteiner. Start conteiner in Detached mode.
  
  docker-compose up --build -d

Stoping conteiner:

  docker-compose stop

Strating conteiner:
  
  docker-compose up -d
