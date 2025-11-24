from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from .models import Message


class MessageTestCase(TestCase):

    def setUp(self):
        """Set up test data and client"""
        self.client = APIClient()
        self.login_url = reverse('message-login')
        self.logout_url = reverse('message-logout')
        self.user_messages_url = reverse('message-user-messages')
        self.send_message_url = reverse('message-send-message')

        # Create some test messages for different users
        self.message_a1 = Message.objects.create(
            user_sender='A',
            user_text='Hello from User A - Message 1'
        )
        self.message_a2 = Message.objects.create(
            user_sender='A', 
            user_text='Hello from User A - Message 2'
        )
        self.message_b1 = Message.objects.create(
            user_sender='B',
            user_text='Hello from User B - Message 1'
        )
        
        # Create bot responses
        self.bot_response_a = Message.objects.create(
            user_sender='Usuário: A',
            bot_text='Bot response to User A'
        )
        self.bot_response_b = Message.objects.create(
            user_sender='Usuário: B', 
            bot_text='Bot response to User B'
        )

    def test_user_login_success(self):
        """Test successful user login"""
        # Test login for User A
        response = self.client.post(self.login_url, {'user': 'A'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['active_user'], 'A')
        self.assertIn('Logged in as A', response.data['message'])
        
        # Test login for User B
        response = self.client.post(self.login_url, {'user': 'B'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['active_user'], 'B')
        self.assertIn('Logged in as B', response.data['message'])

    def test_user_login_invalid_user(self):
        """Test login with invalid user type"""
        # Test with invalid user
        response = self.client.post(self.login_url, {'user': 'C'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Erro', response.data)
        self.assertIn("Usuário deve ser do tipo 'A' ou 'B'", response.data['Erro'])
        
        # Test with empty user
        response = self.client.post(self.login_url, {'user': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test with no user data
        response = self.client.post(self.login_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_logout(self):
        """Test user logout functionality"""
        # First login as User A
        self.client.post(self.login_url, {'user': 'A'})
        
        # Verify session has active_user
        session = self.client.session
        self.assertEqual(session['active_user'], 'A')
        
        # Test logout
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data['active_user'])
        self.assertEqual(response.data['message'], 'Logged out')
        
        # Verify session is cleared
        session = self.client.session
        self.assertNotIn('active_user', session)

    def test_user_filtered_messages_success(self):
        """Test that users only see their own messages"""
        # Login as User A and get messages
        self.client.post(self.login_url, {'user': 'A'})
        response = self.client.get(self.user_messages_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # User A should only see their messages and bot responses to A
        messages = response.data
        user_senders = [msg['user_sender'] for msg in messages]
        
        # Should only contain User A messages and bot responses to A
        expected_senders = {'A', 'Usuário: A'}
        actual_senders = set(user_senders)
        
        self.assertTrue(actual_senders.issubset(expected_senders))
        
        # Should NOT contain User B messages or bot responses to B
        self.assertNotIn('B', user_senders)
        self.assertNotIn('Usuário: B', user_senders)
        
        # Verify the correct messages are returned
        message_texts = [msg['user_text'] for msg in messages if msg['user_text']]
        self.assertIn('Hello from User A - Message 1', message_texts)
        self.assertIn('Hello from User A - Message 2', message_texts)
        self.assertNotIn('Hello from User B - Message 1', message_texts)

    def test_user_filtered_messages_unauthorized(self):
        """Test that unauthorized users cannot access messages"""
        # Try to get messages without logging in
        response = self.client.get(self.user_messages_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Erro', response.data)
        self.assertIn('Usuário não está logado', response.data['Erro'])

    def test_user_send_message_success(self):
        """Test successful message sending"""
        # Login as User A
        self.client.post(self.login_url, {'user': 'A'})
        
        # Send a message
        message_text = 'This is a test message from User A'
        response = self.client.post(self.send_message_url, {'text': message_text})
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify response structure
        self.assertIn('user_message', response.data)
        self.assertIn('bot_message', response.data)
        
        # Verify user message data
        user_message = response.data['user_message']
        self.assertEqual(user_message['user_sender'], 'A')
        self.assertEqual(user_message['user_text'], message_text)
        self.assertIsNone(user_message['bot_text'])
        
        # Verify bot message data
        bot_message = response.data['bot_message']
        self.assertEqual(bot_message['user_sender'], 'Usuário: A')
        self.assertIn('Obrigado por seu contato, Usuário A', bot_message['bot_text'])
        self.assertIsNone(bot_message['user_text'])
        
        # Verify messages were saved to database
        self.assertEqual(Message.objects.filter(user_sender='A', user_text=message_text).count(), 1)
        self.assertEqual(Message.objects.filter(user_sender='Usuário: A').count(), 2)  # Original + new

    def test_user_send_message_empty_text(self):
        """Test sending message with empty text"""
        # Login as User B
        self.client.post(self.login_url, {'user': 'B'})
        
        # Try to send empty message
        response = self.client.post(self.send_message_url, {'text': ''})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Erro', response.data)
        self.assertIn('O texto é obrigatório', response.data['Erro'])
        
        # Try to send message with only whitespace
        response = self.client.post(self.send_message_url, {'text': '   '})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Erro', response.data)
        self.assertIn('O texto é obrigatório', response.data['Erro'])

    def test_user_send_message_unauthorized(self):
        """Test that unauthorized users cannot send messages"""
        # Try to send message without logging in
        response = self.client.post(self.send_message_url, {'text': 'Unauthorized message'})
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Erro', response.data)
        self.assertIn('Usuário não está logado', response.data['Erro'])

    def test_message_isolation_between_users(self):
        """Test complete isolation between User A and User B"""
        # User A sends messages
        self.client.post(self.login_url, {'user': 'A'})
        self.client.post(self.send_message_url, {'text': 'Message from A'})
        
        # User B sends messages  
        self.client.post(self.login_url, {'user': 'B'})
        self.client.post(self.send_message_url, {'text': 'Message from B'})
        
        # Check User A's messages
        self.client.post(self.login_url, {'user': 'A'})
        response_a = self.client.get(self.user_messages_url)
        messages_a = response_a.data
        
        # User A should only see their own messages
        user_senders_a = set(msg['user_sender'] for msg in messages_a)
        self.assertEqual(user_senders_a, {'A', 'Usuário: A'})
        
        # Check User B's messages
        self.client.post(self.login_url, {'user': 'B'})
        response_b = self.client.get(self.user_messages_url)
        messages_b = response_b.data
        
        # User B should only see their own messages
        user_senders_b = set(msg['user_sender'] for msg in messages_b)
        self.assertEqual(user_senders_b, {'B', 'Usuário: B'})

    def test_message_ordering(self):
        """Test that messages are ordered by creation date"""
        # Login and send multiple messages
        self.client.post(self.login_url, {'user': 'A'})
        
        self.client.post(self.send_message_url, {'text': 'First message'})
        self.client.post(self.send_message_url, {'text': 'Second message'})
        self.client.post(self.send_message_url, {'text': 'Third message'})
        
        # Get messages and check ordering
        response = self.client.get(self.user_messages_url)
        messages = response.data
        
        # Filter user messages (excluding bot responses)
        user_messages = [msg for msg in messages if msg['user_sender'] == 'A']
        user_texts = [msg['user_text'] for msg in user_messages]
        
        # Messages should be in chronological order
        self.assertEqual(user_texts, [
            'Hello from User A - Message 1',
            'Hello from User A - Message 2', 
            'First message',
            'Second message',
            'Third message'
        ])

    def test_bot_response_content(self):
        """Test that bot responses contain correct user information"""
        # Test for User A
        self.client.post(self.login_url, {'user': 'A'})
        response = self.client.post(self.send_message_url, {'text': 'Test message'})
        
        bot_message = response.data['bot_message']
        self.assertIn('Obrigado por seu contato, Usuário A', bot_message['bot_text'])
        
        # Test for User B  
        self.client.post(self.login_url, {'user': 'B'})
        response = self.client.post(self.send_message_url, {'text': 'Test message'})
        
        bot_message = response.data['bot_message']
        self.assertIn('Obrigado por seu contato, Usuário B', bot_message['bot_text'])
