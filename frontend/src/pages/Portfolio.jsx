import { useState, useEffect } from 'react'
import api from '../services/api'

export default function Portfolio() {
  const [items, setItems] = useState([])
  const [techStack, setTechStack] = useState('')
  const [link, setLink] = useState('')
  const [editingId, setEditingId] = useState(null)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)

  const fetchPortfolios = async () => {
    try {
      const { data } = await api.get('/portfolio/')
      setItems(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load portfolios')
    }
  }

  useEffect(() => {
    fetchPortfolios()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setLoading(true)
    try {
      if (editingId) {
        await api.put(`/portfolio/${editingId}`, { tech_stack: techStack, link })
        setSuccess('Portfolio updated')
      } else {
        await api.post('/portfolio/', { tech_stack: techStack, link })
        setSuccess('Portfolio created')
      }
      setTechStack('')
      setLink('')
      setEditingId(null)
      fetchPortfolios()
    } catch (err) {
      setError(err.response?.data?.detail || 'Operation failed')
    } finally {
      setLoading(false)
    }
  }

  const handleEdit = (item) => {
    setEditingId(item.id)
    setTechStack(item.tech_stack)
    setLink(item.link)
  }

  const handleDelete = async (id) => {
    if (!confirm('Delete this portfolio entry?')) return
    try {
      await api.delete(`/portfolio/${id}`)
      fetchPortfolios()
    } catch (err) {
      setError(err.response?.data?.detail || 'Delete failed')
    }
  }

  const cancelEdit = () => {
    setEditingId(null)
    setTechStack('')
    setLink('')
  }

  return (
    <div>
      <h1>Portfolio</h1>
      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      <div className="card">
        <h2>{editingId ? 'Edit Portfolio' : 'Add Portfolio'}</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Tech Stack (comma separated)</label>
            <input
              type="text"
              value={techStack}
              onChange={(e) => setTechStack(e.target.value)}
              placeholder="Python, FastAPI, React"
              required
            />
          </div>
          <div className="form-group">
            <label>Link</label>
            <input
              type="url"
              value={link}
              onChange={(e) => setLink(e.target.value)}
              placeholder="https://github.com/yourusername"
              required
            />
          </div>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button type="submit" className="primary" disabled={loading}>
              {loading ? 'Saving...' : editingId ? 'Update' : 'Create'}
            </button>
            {editingId && (
              <button type="button" onClick={cancelEdit}>Cancel</button>
            )}
          </div>
        </form>
      </div>

      <div className="card">
        <h2>Your Portfolios</h2>
        {items.length === 0 && <p className="muted">No portfolios yet.</p>}
        {items.map((item) => (
          <div key={item.id} className="list-item">
            <div>
              <div><strong>{item.tech_stack}</strong></div>
              <div className="muted">{item.link}</div>
            </div>
            <div className="actions">
              <button onClick={() => handleEdit(item)}>Edit</button>
              <button className="danger" onClick={() => handleDelete(item.id)}>Delete</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
