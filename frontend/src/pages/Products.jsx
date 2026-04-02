import { useMemo, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { fetchProducts } from '../api/client.js'

const sources = ['', 'grailed', 'fashionphile', '1stdibs']

export default function Products() {
  const [source, setSource] = useState('')
  const [page, setPage] = useState(1)

  const queryKey = useMemo(() => ['products', source, page], [source, page])
  const params = useMemo(() => ({ source: source || undefined, page, limit: 20 }), [source, page])

  const productsQuery = useQuery({
    queryKey,
    queryFn: () => fetchProducts(params),
    keepPreviousData: true,
  })

  const items = productsQuery.data?.items ?? []
  const pages = productsQuery.data?.pages ?? 1

  return (
    <section className="page-card">
      <div className="page-header">
        <div>
          <p className="eyebrow">Products</p>
          <h1>Tracked listings</h1>
          <p>Browse active listings and review price history for each item.</p>
        </div>
      </div>

      <div className="filter-row">
        <label>
          Source
          <select value={source} onChange={(event) => setSource(event.target.value)}>
            {sources.map((value) => (
              <option key={value} value={value}>
                {value ? value : 'All sources'}
              </option>
            ))}
          </select>
        </label>
      </div>

      {productsQuery.isLoading && <p>Loading listings…</p>}
      {productsQuery.isError && <p className="error-message">Unable to load products.</p>}

      {items.length > 0 ? (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Brand</th>
                <th>Source</th>
                <th>Price</th>
                <th>Last seen</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td>
                    <Link to={`/products/${item.id}`}>{item.title}</Link>
                  </td>
                  <td>{item.brand}</td>
                  <td>{item.source}</td>
                  <td>{item.currency} {item.current_price.toFixed(2)}</td>
                  <td>{new Date(item.last_seen_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        !productsQuery.isLoading && <p>No listings found.</p>
      )}

      <div className="pagination-row">
        <button type="button" onClick={() => setPage((value) => Math.max(value - 1, 1))} disabled={page === 1}>
          Previous
        </button>
        <span>Page {page} of {pages}</span>
        <button type="button" onClick={() => setPage((value) => Math.min(value + 1, pages))} disabled={page === pages}>
          Next
        </button>
      </div>
    </section>
  )
}
