import { Routes, Route, Navigate } from 'react-router-dom'
import useAuth from './hooks/useAuth'
import Navbar from './components/Navbar'
import Login from './pages/Login'
import Register from './pages/Register'
import Portfolio from './pages/Portfolio'
import GenerateEmail from './pages/GenerateEmail'
import Emails from './pages/Emails'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  const { token } = useAuth()

  return (
    <div className="app">
      {token && <Navbar />}
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
