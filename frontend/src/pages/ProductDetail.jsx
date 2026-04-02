import { useMemo } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useParams, Link } from 'react-router-dom'
import { fetchProductHistory } from '../api/client.js'
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

export default function ProductDetail() {
  const { id } = useParams()
  const productQuery = useQuery({
    queryKey: ['product', id],
    queryFn: () => fetchProductHistory(id),
    enabled: Boolean(id),
  })

  const history = productQuery.data?.price_history ?? []
  const chartData = useMemo(
    () =>
      [...history]
        .reverse()
        .map((entry) => ({
          date: new Date(entry.recorded_at).toLocaleDateString(),
          price: entry.price,
        })),
    [history],
  )

  return (
    <section className="page-card">
      <div className="page-header">
        <div>
          <p className="eyebrow">Product details</p>
          <h1>{productQuery.data?.title ?? 'Loading item…'}</h1>
        </div>
        <Link className="secondary-button" to="/products">
          Back to products
        </Link>
      </div>

      {productQuery.isLoading && <p>Loading product details…</p>}
      {productQuery.isError && <p className="error-message">Unable to load product details.</p>}

      {productQuery.data && (
        <>
          <div className="detail-grid">
            <div className="detail-card">
              <img src={productQuery.data.image_url} alt={productQuery.data.title} />
            </div>
            <div className="detail-card detail-summary">
              <p className="detail-label">Brand</p>
              <p>{productQuery.data.brand}</p>
              <p className="detail-label">Category</p>
              <p>{productQuery.data.category}</p>
              <p className="detail-label">Source</p>
              <p>{productQuery.data.source}</p>
              <p className="detail-label">Price</p>
              <p>{productQuery.data.currency} {productQuery.data.current_price.toFixed(2)}</p>
              <p className="detail-label">Condition</p>
              <p>{productQuery.data.condition}</p>
              <p className="detail-label">Last seen</p>
              <p>{new Date(productQuery.data.last_seen_at).toLocaleString()}</p>
              <a href={productQuery.data.url} target="_blank" rel="noreferrer" className="link-button">
                Open listing
              </a>
            </div>
          </div>

          {chartData.length > 0 ? (
            <div className="chart-card">
              <h2>Price history</h2>
              <ResponsiveContainer width="100%" height={320}>
                <LineChart data={chartData} margin={{ top: 12, right: 20, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="price" stroke="#7c3aed" strokeWidth={3} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <p>No price history available yet.</p>
          )}
        </>
      )}
    </section>
  )
}
