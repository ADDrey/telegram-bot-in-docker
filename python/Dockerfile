FROM python:3.9

WORKDIR /usr/src/app
ENV TELEGRAM_API_TOKEN="1234351634:ASFsdFdSDFewgfs-sa8etuv_-sdgadbasbs"
ENV TELEGRAM_ACCESS_ID="1234567891"

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt ./
COPY createdb.sql ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install sqlite3 -y

ENTRYPOINT ["python", "server.py"]