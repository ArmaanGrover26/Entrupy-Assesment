import { useEffect, useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { useNavigate, Link } from 'react-router-dom'
import { login, register, setToken, isAuthenticated } from '../api/client.js'

export default function Register() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const mutation = useMutation({
    mutationFn: register,
    onSuccess: async () => {
      const data = await login({ email, password })
      setToken(data.access_token)
      navigate('/', { replace: true })
    },
  })

  useEffect(() => {
    if (isAuthenticated()) {
      navigate('/', { replace: true })
    }
  }, [navigate])

  const handleSubmit = (event) => {
    event.preventDefault()
    mutation.mutate({ email, password })
  }

  return (
    <section className="page-card auth-page">
      <h1>Create account</h1>
      <p>Register now and start tracking price changes.</p>
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
          {mutation.isLoading ? 'Registering…' : 'Create account'}
        </button>
        {mutation.isError && (
          <p className="error-message">{mutation.error?.response?.data?.detail ?? 'Registration failed'}</p>
        )}
      </form>
      <p className="small-text">
        Already have an account? <Link to="/login">Sign in</Link>.
      </p>
    </section>
  )
}
