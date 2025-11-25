import { describe, test, expect, beforeEach, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

vi.mock('axios', () => {
  const mockAxios = {
    post: vi.fn(),
    get: vi.fn(),
    defaults: {
      baseURL: 'http://localhost:8001/api',
      withCredentials: true
    }
  }
  
  return {
    default: mockAxios,
    post: mockAxios.post,
    get: mockAxios.get
  }
})

// Importar axios DEPOIS do mock
import axios from 'axios'

describe('Integration Tests', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.clearAllMocks()
  })

  test('complete user flow: login → send message → logout', async () => {
    const user = userEvent.setup()

    axios.post
      .mockResolvedValueOnce({
        data: { active_user: 'B', message: 'Logged in as B' }
      })
      .mockResolvedValueOnce({
        data: {
          user_message: {
            id: 1,
            user_sender: 'B',
            user_text: 'Hello, I need help',
            bot_text: null,
            created_at: '2023-01-01T00:00:00Z'
          },
          bot_message: {
            id: 2,
            user_sender: 'Usuário: B',
            user_text: null,
            bot_text: 'Obrigado por seu contato, Usuário B. Em breve responderemos.',
            created_at: '2023-01-01T00:00:01Z'
          }
        }
      })
      .mockResolvedValueOnce({
        data: { active_user: null, message: 'Logged out' }
      })

    render(<App />)
    
    await user.click(screen.getByText('Login Usuário B'))
    
    await waitFor(() => {
      expect(screen.getByText('Logged in as:')).toBeInTheDocument()
      expect(screen.getByText('User B')).toBeInTheDocument()
    })

    await user.type(screen.getByPlaceholderText('Type your message here...'), 'Hello, I need help')
    await user.click(screen.getByText('Send'))
    
    await waitFor(() => {
      expect(screen.getByText('Hello, I need help')).toBeInTheDocument()
      expect(screen.getByText('Obrigado por seu contato, Usuário B. Em breve responderemos.')).toBeInTheDocument()
    })

    await user.click(screen.getByText('Logout'))
    
    await waitFor(() => {
      expect(screen.getByText('Selecione o tipo de usuário:')).toBeInTheDocument()
    })
  })
})