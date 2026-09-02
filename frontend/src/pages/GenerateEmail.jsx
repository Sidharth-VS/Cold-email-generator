import { useState } from 'react'
import api from '../services/api'

export default function GenerateEmail() {
  const [jobUrl, setJobUrl] = useState('')
  const [role, setRole] = useState('')
  const [organisation, setOrganisation] = useState('')
  const [generated, setGenerated] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [copied, setCopied] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setGenerated('')
    setLoading(true)
    try {
      const params = new URLSearchParams({ job_url: jobUrl })
      if (role) params.set('role', role)
      if (organisation) params.set('organisation', organisation)

      const { data } = await api.post(`/mails/generate?${params.toString()}`)
      setGenerated(data.generated_email)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate email')
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(generated)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy', err)
    }
  }

  return (
    <div>
      <h1>Generate Cold Email</h1>
      {error && <div className="error">{error}</div>}

      <div className="card">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Job Posting URL</label>
            <input
              type="url"
              value={jobUrl}
              onChange={(e) => setJobUrl(e.target.value)}
              placeholder="https://example.com/careers/job"
              required
            />
          </div>
          <div className="form-group">
            <label>Your Role</label>
            <input
              type="text"
              value={role}
              onChange={(e) => setRole(e.target.value)}
              placeholder="Software Engineer"
            />
          </div>
          <div className="form-group">
            <label>Organisation</label>
            <input
              type="text"
              value={organisation}
              onChange={(e) => setOrganisation(e.target.value)}
              placeholder="Acme Inc."
            />
          </div>
          <button type="submit" className="primary" disabled={loading}>
            {loading ? 'Generating...' : 'Generate Mail'}
          </button>
        </form>
      </div>

      {generated && (
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h2>Generated Email</h2>
            <button type="button" className="secondary" onClick={handleCopy}>
              {copied ? 'Copied!' : 'Copy'}
            </button>
          </div>
          <div className="email-preview">{generated}</div>
        </div>
      )}
    </div>
  )
}
