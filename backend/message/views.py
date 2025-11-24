from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

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

    @action(detail=False, methods=['get'])
    def user_messages(self, request):
        """Get messages only for the currently logged-in user"""
        active_user = request.session.get('active_user')
        
        if not active_user:
            return Response(
                {"Erro": "Usuário não está logado"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Filter messages: user's messages + bot responses to this user
        user_messages_filtered = Message.objects.filter(
            Q(user_sender=active_user) | 
            Q(user_sender=f"Usuário: {active_user}")
        ).order_by('created_at')
        
        serializer = MessageSerializer(user_messages_filtered, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def send_message(self, request):
        # Get user from session instead of request data for security
        active_user = request.session.get('active_user')
        
        if not active_user:
            return Response({
                "Erro": "Usuário não está logado"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        text = Verifier.verify_user_text(request, 'text')
        
        if not text or not str(text).strip():
            return Response({
                "Erro": "O texto é obrigatório"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user_msg = Message.objects.create(
            user_sender=active_user, 
            user_text=text.strip()
        )
        
        bot_sender = f"Usuário: {active_user}"
        nome_exibicao = dict(USER_TYPE_CHOICES).get(active_user, active_user)
        bot_text = f"Obrigado por seu contato, {nome_exibicao}. Em breve responderemos."
        bot_msg = Message.objects.create(
            user_sender=bot_sender, 
            bot_text=bot_text
        )

        return Response({
            "user_message": MessageSerializer(user_msg).data,
            "bot_message": MessageSerializer(bot_msg).data,
        }, status=status.HTTP_201_CREATED)
