FROM python:3.11-slim

WORKDIR /chat-entrevista

ENV PYTHON DONTWRITEBYTECODE 1
ENV PYTHONUNBUFERRED 1

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD python manage.py migrate && python manage.py rag marcus.pdf && python manage.py runserver 0.0.0.0:8000
