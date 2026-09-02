import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import api from '../services/api'

export default function Emails() {
  const [emails, setEmails] = useState([])
  const [error, setError] = useState('')
  const [expandedId, setExpandedId] = useState(null)
  const [copiedId, setCopiedId] = useState(null)

  const fetchEmails = async () => {
    try {
      const { data } = await api.get('/mails/')
      setEmails(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load emails')
    }
  }

  useEffect(() => {
    fetchEmails()
  }, [])

  const handleDelete = async (id) => {
    if (!confirm('Delete this email?')) return
    try {
      await api.delete(`/mails/${id}`)
      setEmails((prev) => prev.filter((item) => item.id !== id))
    } catch (err) {
      setError(err.response?.data?.detail || 'Delete failed')
    }
  }

  const handleCopy = async (id, text) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedId(id)
      setTimeout(() => setCopiedId(null), 2000)
    } catch (err) {
      console.error('Failed to copy', err)
    }
  }

  return (
    <div>
      <h1>Generated Emails</h1>
      {error && <div className="error">{error}</div>}

      <div className="card">
        {emails.length === 0 && <p className="muted">No emails generated yet.</p>}
        {emails.map((item) => (
          <div key={item.id} className="list-item" style={{ flexDirection: 'column', alignItems: 'stretch' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div><strong>{item.job_url || 'Unknown job'}</strong></div>
                <div className="muted">{new Date(item.created_at).toLocaleString()}</div>
              </div>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button onClick={() => setExpandedId(expandedId === item.id ? null : item.id)}>
                  {expandedId === item.id ? 'Hide' : 'View'}
                </button>
                <button className="danger" onClick={() => handleDelete(item.id)}>Delete</button>
              </div>
            </div>
            {expandedId === item.id && (
              <div style={{ marginTop: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '0.5rem' }}>
                  <button className="secondary" onClick={() => handleCopy(item.id, item.generated_email)}>
                    {copiedId === item.id ? 'Copied!' : 'Copy'}
                  </button>
                </div>
                <div className="email-preview">
                  {item.generated_email}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
