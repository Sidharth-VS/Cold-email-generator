import { Routes, Route, Navigate, Link } from 'react-router-dom'
import useAuth from './hooks/useAuth'
import useTheme from './hooks/useTheme'
import Login from './pages/Login'
import Register from './pages/Register'
import Portfolio from './pages/Portfolio'
import GenerateEmail from './pages/GenerateEmail'
import Emails from './pages/Emails'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  const { token, logout } = useAuth()
  const { theme, toggleTheme } = useTheme()

  return (
    <div className="app">
      <header>
        <div className="container">
          <Link to="/" className="logo">Cold Email Generator</Link>
          <div className="nav-links">
            {token ? (
              <>
                <Link to="/portfolio">Portfolio</Link>
                <Link to="/generate">Generate</Link>
                <Link to="/emails">Emails</Link>
              </>
            ) : (
              <>
                <Link to="/login">Login</Link>
                <Link to="/register">Register</Link>
              </>
            )}
          </div>
          <div className="nav-actions">
            {token && (
              <>
                <button className="theme-toggle" onClick={toggleTheme} title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}>
                  {theme === 'light' ? '🌙' : '☀️'}
                </button>
                <button onClick={() => { logout(); window.location.href = '/login'; }}>Logout</button>
              </>
            )}
            {!token && (
              <button className="theme-toggle" onClick={toggleTheme} title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}>
                {theme === 'light' ? '🌙' : '☀️'}
              </button>
            )}
          </div>
        </div>
      </header>
      <main className="container">
        <Routes>
          <Route path="/login" element={token ? <Navigate to="/portfolio" /> : <Login />} />
          <Route path="/register" element={token ? <Navigate to="/portfolio" /> : <Register />} />
          <Route path="/portfolio" element={<ProtectedRoute><Portfolio /></ProtectedRoute>} />
          <Route path="/generate" element={<ProtectedRoute><GenerateEmail /></ProtectedRoute>} />
          <Route path="/emails" element={<ProtectedRoute><Emails /></ProtectedRoute>} />
          <Route path="*" element={<Navigate to={token ? "/portfolio" : "/login"} />} />
        </Routes>
      </main>
    </div>
  )
}

export default App