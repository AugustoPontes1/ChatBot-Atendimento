from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Message, USER_TYPE_CHOICES
from .serializers import MessageSerializer
from .utils import Verifier


VALID_USERS = {user[0] for user in USER_TYPE_CHOICES}

class MessageViewSet(ViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        user = request.data.get('user') or request.query_params.get('user')
        if user not in VALID_USERS:
            return Response(
                {"Erro": "Usuário deve ser do tipo 'A' ou 'B'"},
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
        # request.data (JSON body), headers, query and session.
        user = Verifier.verify_user(request, 'user')
        text = Verifier.verify_user_text(request, 'text')
        
        if user not in VALID_USERS:
            return Response({
                "Erro": "Usuário inválido"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if not text or not str(text).strip():
            return Response({
                "Erro": "O texto é obrigatório"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user_msg = Message.objects.create(user_sender=user, 
                                          user_text=text.strip())
        bot_sender = f"Usuário: {user}"
        nome_exibicao = dict(USER_TYPE_CHOICES).get(user, user)
        bot_text = f"Obrigado por seu contato, {nome_exibicao}. Em breve responderemos."
        bot_msg = Message.objects.create(user_sender=bot_sender, bot_text=bot_text)

        return Response({
            "user_message": MessageSerializer(user_msg).data,
            "bot_message": MessageSerializer(bot_msg).data,
        }, status=status.HTTP_201_CREATED)
