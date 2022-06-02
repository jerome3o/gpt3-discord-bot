FROM python:3.8

WORKDIR /bot

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY *.py .
CMD ["python", "bot.py"]