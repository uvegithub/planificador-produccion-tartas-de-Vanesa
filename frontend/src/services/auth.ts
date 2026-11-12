const API_URL = '/api/auth'

export interface AuthUser {
  id: number
  email: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: AuthUser
}

const TOKEN_KEY = 'access_token'

export function getToken(): string | null {
  return sessionStorage.getItem(TOKEN_KEY)
}

export function saveSession(response: AuthResponse): void {
  sessionStorage.setItem(TOKEN_KEY, response.access_token)
}

export function clearSession(): void {
  sessionStorage.removeItem(TOKEN_KEY)
}

async function authRequest(
  endpoint: string,
  email: string,
  password: string,
): Promise<AuthResponse> {
  const response = await fetch(`${API_URL}/${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail || 'No se pudo completar la autenticación.')
  }

  return data as AuthResponse
}

export async function register(
  email: string,
  password: string,
): Promise<AuthResponse> {
  const result = await authRequest('register', email, password)
  saveSession(result)
  return result
}

export async function login(
  email: string,
  password: string,
): Promise<AuthResponse> {
  const result = await authRequest('login', email, password)
  saveSession(result)
  return result
}

export async function getCurrentUser(): Promise<AuthUser | null> {
  const token = getToken()

  if (!token) return null

  const response = await fetch(`${API_URL}/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (!response.ok) {
    clearSession()
    return null
  }

  return response.json() as Promise<AuthUser>
}