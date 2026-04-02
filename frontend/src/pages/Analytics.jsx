import { useQuery } from '@tanstack/react-query'
import { fetchAnalytics } from '../api/client.js'

export default function Analytics() {
  const summaryQuery = useQuery({ queryKey: ['analytics'], queryFn: fetchAnalytics })
  const summary = summaryQuery.data

  return (
    <section className="page-card">
      <div className="page-header">
        <div>
          <p className="eyebrow">Analytics</p>
          <h1>Marketplace insights</h1>
          <p>View aggregate data and pricing trends across sources.</p>
        </div>
      </div>

      {summaryQuery.isLoading && <p>Loading analytics…</p>}
      {summaryQuery.isError && <p className="error-message">Unable to load analytics summary.</p>}

      {summary && (
        <div className="analytics-grid">
          <div className="stat-card">
            <span className="stat-label">Total active listings</span>
            <strong>{summary.total_active_listings}</strong>
          </div>
          <div className="stat-card">
            <span className="stat-label">Price changes (24h)</span>
            <strong>{summary.price_changes_last_24h}</strong>
          </div>
          <div className="stat-card">
            <span className="stat-label">Price changes (7d)</span>
            <strong>{summary.price_changes_last_7d}</strong>
          </div>
        </div>
      )}

      {summary && (
        <div className="page-section">
          <h2>Average price by category</h2>
          <div className="summary-list">
            {Object.entries(summary.avg_price_by_category).map(([category, average]) => (
              <div key={category} className="summary-item">
                <span>{category}</span>
                <strong>{average}</strong>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  )
}
