from .models import Message
from .serializers import MessageSerializer
from ..telegram_bot.tasks import send_telegram_message
from rest_framework import generics, status
from rest_framework.response import Response


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['user'] = request.user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        user = self.request.user
        if user.telegram_chat_id:
            text = serializer.validated_data['text']
            send_telegram_message.delay(user.id, text)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

