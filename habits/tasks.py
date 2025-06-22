# habits/tasks.py
import os
from celery import shared_task
from telegram import Bot
from django.conf import settings

@shared_task
def send_telegram_message(chat_id, text):
    """
    Отправляет сообщение в Telegram.
    """
    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        print("Telegram bot token not found. Skipping message.")
        return

    bot = Bot(token=bot_token)
    try:
        bot.send_message(chat_id=chat_id, text=text)
        print(f"Сообщение отправлено в чат {chat_id}")
    except Exception as e:
        print(f"Ошибка при отправке сообщения в чат {chat_id}: {e}")