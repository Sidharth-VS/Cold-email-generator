import { NavLink, useNavigate } from 'react-router-dom'
import useAuth from '../hooks/useAuth'

export default function Navbar() {
  const { logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav>
      <NavLink to="/portfolio" className={({ isActive }) => isActive ? 'active' : ''}>Portfolio</NavLink>
      <NavLink to="/generate" className={({ isActive }) => isActive ? 'active' : ''}>Generate Email</NavLink>
      <NavLink to="/emails" className={({ isActive }) => isActive ? 'active' : ''}>Emails</NavLink>
      <div className="spacer" />
      <button onClick={handleLogout}>Logout</button>
    </nav>
  )
}
