import { useEffect, useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { useNavigate, Link } from 'react-router-dom'
import { login, setToken, isAuthenticated } from '../api/client.js'

export default function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const mutation = useMutation({
    mutationFn: login,
    onSuccess: (data) => {
      setToken(data.access_token)
      navigate('/', { replace: true })
    },
  })

  useEffect(() => {
    if (isAuthenticated()) {
      navigate('/', { replace: true })
    }
  }, [navigate])

  const handleSubmit = async (event) => {
    event.preventDefault()
    mutation.mutate({ email, password })
  }

  return (
    <section className="page-card auth-page">
      <h1>Login</h1>
      <p>Sign in to access the price monitoring dashboard.</p>
      <form onSubmit={handleSubmit} className="form-grid">
        <label>
          Email
          <input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="you@example.com"
            required
          />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="••••••••"
            required
          />
        </label>
        <button type="submit" disabled={mutation.isLoading}>
          {mutation.isLoading ? 'Signing in…' : 'Sign in'}
        </button>
        {mutation.isError && (
          <p className="error-message">{mutation.error?.response?.data?.detail ?? 'Login failed'}</p>
        )}
      </form>
      <p className="small-text">
        New here? <Link to="/register">Create an account</Link>.
      </p>
    </section>
  )
}
