import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { fetchAnalytics, refreshSource } from '../api/client.js'

export default function Dashboard() {
  const queryClient = useQueryClient()
  const summaryQuery = useQuery({ queryKey: ['analytics'], queryFn: fetchAnalytics })
  const refreshMutation = useMutation({
    mutationFn: () => refreshSource(),
    onSuccess: () => {
      queryClient.invalidateQueries(['analytics'])
    },
  })

  const summary = summaryQuery.data

  return (
    <section className="page-card">
      <div className="page-header">
        <div>
          <p className="eyebrow">Dashboard</p>
          <h1>Monitoring overview</h1>
          <p>Track active listings, price movement, and marketplace coverage.</p>
        </div>
        <button
          className="primary-button"
          onClick={() => refreshMutation.mutate()}
          disabled={refreshMutation.isLoading}
        >
          {refreshMutation.isLoading ? 'Refreshing…' : 'Refresh data'}
        </button>
      </div>

      {summaryQuery.isLoading && <p>Loading analytics…</p>}
      {summaryQuery.isError && (
        <p className="error-message">Unable to load analytics summary.</p>
      )}

      {summary && (
        <div className="stats-grid">
          <div className="stat-card">
            <span className="stat-label">Active listings</span>
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
          <div className="stat-card">
            <span className="stat-label">Last refresh</span>
            <strong>{new Date(summary.last_refresh).toLocaleString()}</strong>
          </div>
        </div>
      )}

      {summary && (
        <div className="dashboard-grid">
          <section className="page-section">
            <h2>Market coverage</h2>
            <div className="summary-list">
              {Object.entries(summary.totals_by_source).map(([source, count]) => (
                <div key={source} className="summary-item">
                  <span>{source}</span>
                  <strong>{count}</strong>
                </div>
              ))}
            </div>
          </section>

          <section className="page-section">
            <h2>Price overview</h2>
            <div className="summary-list">
              <div className="summary-item">
                <span>Min price</span>
                <strong>{summary.price_stats.min}</strong>
              </div>
              <div className="summary-item">
                <span>Max price</span>
                <strong>{summary.price_stats.max}</strong>
              </div>
              <div className="summary-item">
                <span>Average price</span>
                <strong>{summary.price_stats.avg}</strong>
              </div>
            </div>
          </section>
        </div>
      )}
    </section>
  )
}
