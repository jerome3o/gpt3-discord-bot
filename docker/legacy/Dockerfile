FROM python:3.8

WORKDIR /bot

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONPATH=.

COPY gptbot/ gptbot/

CMD ["python", "-m", "gptbot.legacy.bot"]