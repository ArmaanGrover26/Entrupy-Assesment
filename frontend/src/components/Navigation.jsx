import { Link, useLocation, useNavigate } from 'react-router-dom'
import { clearToken, isAuthenticated } from '../api/client.js'

const links = [
  { to: '/', label: 'Dashboard' },
  { to: '/products', label: 'Products' },
  { to: '/analytics', label: 'Analytics' },
]

export default function Navigation() {
  const location = useLocation()
  const navigate = useNavigate()
  const auth = isAuthenticated()

  const handleLogout = () => {
    clearToken()
    navigate('/login', { replace: true })
  }

  return (
    <header className="app-header">
      <div className="brand">
        <Link to="/">Price Monitor</Link>
      </div>
      <nav className="nav-links">
        {auth &&
          links.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className={location.pathname === item.to ? 'active' : ''}
            >
              {item.label}
            </Link>
          ))}
      </nav>
      <div className="auth-actions">
        {auth ? (
          <button type="button" className="text-button" onClick={handleLogout}>
            Logout
          </button>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </header>
  )
}
