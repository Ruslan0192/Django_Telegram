FROM python:3.11

WORKDIR /bot

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY requirements_bot.txt .

RUN pip install --no-cache-dir -r requirements_bot.txt


COPY . .


#CMD ["python", "main.py"]
