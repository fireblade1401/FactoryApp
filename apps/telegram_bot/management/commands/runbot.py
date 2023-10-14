import time

from django.core.management.base import BaseCommand
import requests
from django.conf import settings

from apps.users.models import CustomUser

BASE_TELEGRAM_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/"


def send_message(chat_id, text):
    url = BASE_TELEGRAM_URL + f"sendMessage?chat_id={chat_id}&text={text}"
    response = requests.get(url)
    print(f"Sending message to {chat_id}. Response: {response.status_code}, {response.text}")


def get_updates(offset=None):
    url = BASE_TELEGRAM_URL + "getUpdates?timeout=100"
    if offset:
        url += f"&offset={offset}"
    return requests.get(url).json()


class Command(BaseCommand):
    help = 'Запускает вашего бота для Telegram'

    def handle(self, *args, **kwargs):
        self.stdout.write('Бот запущен!')

        last_update_id = None
        while True:
            try:
                updates = get_updates(last_update_id)
                for update in updates.get("result", []):
                    chat_id = update["message"]["chat"]["id"]
                    text = update["message"]["text"]

                    if text == "/start":
                        send_message(chat_id, "Привет! Я ваш бот. Дай мне токен, чтобы я привязал его")
                    elif len(text) == 36:
                        try:
                            user = CustomUser.objects.get(telegram_token=text)
                            if user.telegram_chat_id:
                                send_message(chat_id, "Вы уже привязаны к этому чату!")
                            else:
                                user.telegram_chat_id = chat_id
                                user.save()
                                send_message(chat_id, "Токен получен, и успешно привязан!")
                        except CustomUser.DoesNotExist:
                            send_message(chat_id, "Токен не распознан. Пожалуйста, проверьте и попробуйте ещё раз.")
                    else:
                        send_message(chat_id, "Я не понимаю эту команду.")
                    last_update_id = update["update_id"] + 1
            except requests.exceptions.ConnectionError as e:
                print(f"Connection error: {e}. Waiting for 5 seconds before retrying...")
                time.sleep(5)
