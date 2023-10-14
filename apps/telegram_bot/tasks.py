from celery import shared_task
from ..telegram_bot.management.commands.runbot import get_updates, send_message
from apps.users.models import CustomUser


@shared_task
def send_telegram_message(user_id, text):
    user = CustomUser.objects.get(id=user_id)
    if user.telegram_chat_id:
        formatted_message = f"{user.username}, я получил от тебя сообщение:\n{text}"
        send_message(user.telegram_chat_id, formatted_message)


@shared_task
def fetch_telegram_updates_task():
    updates = get_updates()
    for update in updates.get("result", []):
        message = update.get("message", {})
        text = message.get("text")
        chat_id = message.get("chat", {}).get("id")

        if not text or not chat_id:
            continue
        try:
            user = CustomUser.objects.get(telegram_token=text)
            user.telegram_chat_id = chat_id
            user.save()
            confirmation_msg = f" {user.username}! Теперь ты связан с этим Telegram аккаунтом."
            send_message(chat_id, confirmation_msg)
        except CustomUser.DoesNotExist:
            error_msg = "Токен не распознан. Пожалуйста, проверьте и попробуйте ещё раз."
            send_message(chat_id, error_msg)


