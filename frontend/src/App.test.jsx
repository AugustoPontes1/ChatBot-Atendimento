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

describe('App Component', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.clearAllMocks()
  })

  test('renders login buttons when no user is logged in', () => {
    render(<App />)
    
    expect(screen.getByText('Message App')).toBeInTheDocument()
    expect(screen.getByText('Selecione o tipo de usuário:')).toBeInTheDocument()
    expect(screen.getByText('Login Usuário A')).toBeInTheDocument()
    expect(screen.getByText('Login Usuário B')).toBeInTheDocument()
    expect(screen.getByText('Bem Vindo ao Message App')).toBeInTheDocument()
  })

  test('successfully logs in user A', async () => {
    const user = userEvent.setup()
    
    // Mock da resposta da API
    axios.post.mockResolvedValueOnce({
      data: {
        active_user: 'A',
        message: 'Logged in as A'
      }
    })

    render(<App />)
    
    await user.click(screen.getByText('Login Usuário A'))
    
    expect(axios.post).toHaveBeenCalledWith('/message/login/', { user: 'A' })

    await waitFor(() => {
      expect(screen.getByText('Logged in as:')).toBeInTheDocument()
      expect(screen.getByText('User A')).toBeInTheDocument()
      expect(screen.getByText('Logout')).toBeInTheDocument()
    })
  })

  test('shows error message when login fails', async () => {
    const user = userEvent.setup()
    
    axios.post.mockRejectedValueOnce({
      response: {
        data: { Erro: 'Tipo de usuário inválido' }
      }
    })

    render(<App />)
    
    await user.click(screen.getByText('Login Usuário A'))
    
    await waitFor(() => {
      expect(screen.getByText('Tipo de usuário inválido')).toBeInTheDocument()
    })
  })

  test('successfully logs out user', async () => {
    const user = userEvent.setup()

    axios.post.mockResolvedValueOnce({
      data: {
        active_user: 'A',
        message: 'Logged in as A'
      }
    })

    axios.post.mockResolvedValueOnce({
      data: {
        active_user: null,
        message: 'Logged out'
      }
    })

    render(<App />)

    await user.click(screen.getByText('Login Usuário A'))

    await waitFor(() => {
      expect(screen.getByText('User A')).toBeInTheDocument()
    })

    await user.click(screen.getByText('Logout'))
    
    expect(axios.post).toHaveBeenCalledWith('/message/logout/')

    await waitFor(() => {
      expect(screen.getByText('Selecione o tipo de usuário:')).toBeInTheDocument()
      expect(screen.getByText('Login Usuário A')).toBeInTheDocument()
    })
  })
})