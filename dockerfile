FROM python:3.9.16-buster

RUN apt update
RUN yes | apt install vim
RUN yes | apt install libgl1

COPY ./ /app
WORKDIR /app

ENV STATIC_URL /app/static
ENV STATIC_PATH /var/www/app/static

RUN pip install -r /app/requirements.txt

CMD ["uwsgi", "wsgi.ini"]
