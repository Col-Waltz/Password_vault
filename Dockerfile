FROM python:3.10.6

ADD bot.py storage_python.py storage_sqlite.py .

RUN pip install aiogram

CMD python3 ./bot.py