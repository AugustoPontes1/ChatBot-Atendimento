import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'http://localhost:8001/api';
axios.defaults.baseURL = API_BASE_URL;
axios.defaults.withCredentials = true;

function App() {
  const [activeUser, setActiveUser] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Check if user is logged in on component mount
  useEffect(() => {
    checkSession();
  }, []);

  // Fetch messages whenever activeUser changes
  useEffect(() => {
    if (activeUser) {
      fetchMessages();
    } else {
      setMessages([]); // Clear messages when logging out
    }
  }, [activeUser]);

  const checkSession = async () => {
    try {
      const sessionUser = localStorage.getItem('activeUser');
      if (sessionUser) {
        setActiveUser(sessionUser);
      }
    } catch (err) {
      console.error('Error checking session:', err);
    }
  };

  const fetchMessages = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/message/user_messages/');
      setMessages(response.data);
      setError('');
    } catch (err) {
      console.error('Error fetching messages:', err);
      if (err.response?.status === 401) {
        // User not logged in, clear local storage
        localStorage.removeItem('activeUser');
        setActiveUser(null);
      }
      setError(err.response?.data?.Erro || 'Failed to load messages');
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (userType) => {
    try {
      setError('');
      const response = await axios.post('/message/login/', { user: userType });
      
      if (response.data.active_user) {
        setActiveUser(response.data.active_user);
        localStorage.setItem('activeUser', response.data.active_user);
        setError('');
        // Messages will be automatically fetched by the useEffect
      }
    } catch (err) {
      setError(err.response?.data?.Erro || 'Login failed');
      console.error('Login error:', err);
    }
  };

  const handleLogout = async () => {
    try {
      await axios.post('/message/logout/');
      setActiveUser(null);
      localStorage.removeItem('activeUser');
      setMessages([]);
      setError('');
    } catch (err) {
      setError('Logout failed');
      console.error('Logout error:', err);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    try {
      setError('');
      const response = await axios.post('/message/send_message/', {
        text: newMessage
      });

      setMessages(prev => [
        ...prev,
        response.data.user_message,
        response.data.bot_message
      ]);

      // Alternative: Refresh all messages to ensure consistency
      // await fetchMessages();

      setNewMessage('');
    } catch (err) {
      setError(err.response?.data?.Erro || 'Failed to send message');
      console.error('Send message error:', err);
      
      // If unauthorized, log user out
      if (err.response?.status === 401) {
        localStorage.removeItem('activeUser');
        setActiveUser(null);
      }
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  // Helper function to determine message type for styling
  const getMessageType = (message) => {
    if (message.user_sender === activeUser) {
      return 'user-message';
    } else if (message.user_sender.startsWith('Usuário: ')) {
      return 'bot-message';
    } else {
      return 'other-user-message'; // This shouldn't happen with our filtering
    }
  };

  // Helper function to display sender name nicely
  const getDisplayName = (message) => {
    if (message.user_sender === activeUser) {
      return 'You';
    } else if (message.user_sender.startsWith('Usuário: ')) {
      return 'Bot';
    }
    return message.user_sender;
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Message App</h1>
        <div className="user-section">
          {activeUser ? (
            <div className="user-info">
              <span>Logged in as: <strong>User {activeUser}</strong></span>
              <button onClick={handleLogout} className="logout-btn">
                Logout
              </button>
            </div>
          ) : (
            <div className="login-buttons">
              <p>Select user type:</p>
              <button onClick={() => handleLogin('A')} className="login-btn">
                Login as User A
              </button>
              <button onClick={() => handleLogin('B')} className="login-btn">
                Login as User B
              </button>
            </div>
          )}
        </div>
      </header>

      <main className="app-main">
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {!activeUser ? (
          <div className="welcome-message">
            <h2>Welcome to the Message App</h2>
            <p>Please log in to start sending messages.</p>
            <div className="user-description">
              <p><strong>User A</strong> and <strong>User B</strong> have separate message histories.</p>
              <p>Each user can only see their own messages.</p>
            </div>
          </div>
        ) : (
          <div className="chat-container">
            <div className="messages-section">
              <div className="messages-header">
                <h3>Your Messages</h3>
                <button onClick={fetchMessages} className="refresh-btn" disabled={loading}>
                  {loading ? 'Refreshing...' : 'Refresh'}
                </button>
              </div>
              
              {loading ? (
                <p>Loading messages...</p>
              ) : (
                <div className="messages-list">
                  {messages.map((message) => (
                    <div key={message.id} className={`message ${getMessageType(message)}`}>
                      <div className="message-header">
                        <strong>{getDisplayName(message)}</strong>
                        <span className="message-time">
                          {formatDate(message.created_at)}
                        </span>
                      </div>
                      <div className="message-content">
                        {message.user_text || message.bot_text}
                      </div>
                    </div>
                  ))}
                  {messages.length === 0 && (
                    <p className="no-messages">No messages yet. Start a conversation!</p>
                  )}
                </div>
              )}
            </div>

            <form onSubmit={handleSendMessage} className="message-form">
              <div className="input-group">
                <input
                  type="text"
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  placeholder="Type your message here..."
                  className="message-input"
                  disabled={!activeUser}
                />
                <button 
                  type="submit" 
                  disabled={!newMessage.trim() || !activeUser}
                  className="send-btn"
                >
                  Send
                </button>
              </div>
            </form>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;