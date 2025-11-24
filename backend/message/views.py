from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Message, USER_TYPE_CHOICES
from .serializers import MessageSerializer


VALID_USERS = {user[0] for user in USER_TYPE_CHOICES}

class MessageViewSet(ViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        user = request.data.get('user') or request.query_params.get('user')
        if user not in VALID_USERS:
            return Response(
                {"detail": "user must be 'A' or 'B'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.session['active_user'] = user

        return Response({
            "active_user": user, "message": f"Logged in as {user}"
        })

    @action(detail=False, methods=['post'])
    def logout(self, request):
        request.session.pop('active_user', None)
        return Response({"active_user": None, "message": "Logged out"})

    @action(detail=False, methods=['post'])
    def send_message(self, request):
        # preferir request.data (JSON body). depois headers, query e session.
        user = None
        if isinstance(request.data, dict):
            user = request.data.get('user')
            text = request.data.get('text')
        else:
            text = None

        # fallbacks
        if not user:
            user = request.headers.get('X-User') or request.query_params.get('user') or request.session.get('active_user')
        if not text:
            text = request.query_params.get('text') or (request.data.get('text') if isinstance(request.data, dict) else None)

        if user not in VALID_USERS:
            return Response({"Erro": "Usuário inválido"}, status=status.HTTP_400_BAD_REQUEST)

        if not text or not str(text).strip():
            return Response({"Erro": "O texto é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

        # salva a mensagem do usuário
        user_msg = Message.objects.create(sender=user, text=text.strip())

        # cria resposta do bot com sender previsível (BOT_A, BOT_B, ...)
        bot_sender = f"BOT_{user}"
        # rótulo legível (ex: "Usuário A")
        nome_exibicao = dict(USER_TYPE_CHOICES).get(user, user)
        bot_text = f"Obrigado por seu contato, {nome_exibicao}. Em breve responderemos."

        # dependendo do model, salvar bot_msg pode falhar se choices não permitirem BOT_*
        bot_msg = Message.objects.create(sender=bot_sender, text=bot_text)

        return Response({
            "user_message": MessageSerializer(user_msg).data,
            "bot_message": MessageSerializer(bot_msg).data,
        }, status=status.HTTP_201_CREATED)