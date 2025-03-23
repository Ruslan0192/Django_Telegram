FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . .

#CMD [ "python", "manage.py", "runserver" ]
