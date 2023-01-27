FROM python:3.9

WORKDIR /usr/src/app
ENV TELEGRAM_API_TOKEN="1234567890:sdlfajaWSIFEijsag-9sasdfwa_sdfkl435U"
ENV TELEGRAM_ACCESS_ID="0321654987"

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt ./
COPY createdb.sql ./
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "server.py"]
