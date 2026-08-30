import { useState } from 'react'

export function Table({ columns, rows }) {
  const [sortKey, setSortKey] = useState(columns[0]?.key)
  const [sortDirection, setSortDirection] = useState('asc')

  const sorted = [...rows].sort((a, b) => {
    if (!sortKey) return 0
    const left = String(a[sortKey])
    const right = String(b[sortKey])
    return sortDirection === 'asc' ? left.localeCompare(right) : right.localeCompare(left)
  })

  const onSort = (key) => {
    if (sortKey === key) {
      setSortDirection((direction) => (direction === 'asc' ? 'desc' : 'asc'))
      return
    }
    setSortKey(key)
    setSortDirection('asc')
  }

  return (
    <div className="overflow-auto rounded-lg border border-slate-700">
      <table className="min-w-full text-left text-sm">
        <thead className="bg-slate-800 text-slate-200">
          <tr>
            {columns.map((column) => (
              <th key={column.key} className="px-4 py-3">
                <button className="font-semibold" type="button" onClick={() => onSort(column.key)}>
                  {column.label}
                </button>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sorted.map((row, index) => (
            <tr key={`${row.id}-${index}`} className={`hover:bg-slate-800 ${index % 2 === 0 ? 'bg-slate-900' : 'bg-slate-950'}`}>
              {columns.map((column) => (
                <td key={column.key} className="px-4 py-3">
                  {row[column.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
