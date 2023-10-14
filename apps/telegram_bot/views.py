from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..telegram_bot.management.commands.runbot import get_updates, send_message


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_telegram_token(request):
    user = request.user
    updates = get_updates()
    if not updates.get("result"):
        return Response({"error": "No updates from Telegram"}, status=status.HTTP_400_BAD_REQUEST)

    last_update_id = None

    if user.telegram_chat_id:
        send_message(user.telegram_chat_id, "Вы уже связали этот Telegram аккаунт!")
        return Response({"error": "Account already linked."}, status=status.HTTP_400_BAD_REQUEST)

    for update in reversed(updates["result"]):
        last_update_id = update["update_id"]
        message = update.get("message")

        if message and message["text"] == user.telegram_token:
            user.telegram_chat_id = message["chat"]["id"]
            user.save()
            send_message(user.telegram_chat_id, "Вы успешно связали телеграмм аккаунт!")
            return Response({"status": "Token has been set."}, status=status.HTTP_200_OK)

    return Response({"error": "Token not found in recent messages. Please send your token to the bot again."},
                    status=status.HTTP_400_BAD_REQUEST)
