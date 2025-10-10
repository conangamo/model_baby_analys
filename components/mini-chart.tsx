"use client"

import { TrendingUp, TrendingDown, Minus } from "lucide-react"

interface MiniChartProps {
  title: string
  value: string
  trend: "up" | "down" | "stable"
  data: number[]
  color: string
}

export default function MiniChart({ title, value, trend, data, color }: MiniChartProps) {
  const max = Math.max(...data)
  const min = Math.min(...data)
  const range = max - min || 1

  const TrendIcon = trend === "up" ? TrendingUp : trend === "down" ? TrendingDown : Minus
  const trendColor = trend === "up" ? "text-green-500" : trend === "down" ? "text-red-500" : "text-gray-500"

  return (
    <div className="bg-white rounded-2xl p-4 shadow-md hover:shadow-lg transition-all duration-300 group">
      <div className="flex items-center justify-between mb-3">
        <p className="text-xs text-gray-600 font-medium">{title}</p>
        <TrendIcon className={`w-4 h-4 ${trendColor}`} />
      </div>

      <p className="text-2xl font-bold text-gray-800 mb-3">{value}</p>

      {/* Mini Line Chart */}
      <div className="flex items-end gap-1 h-12">
        {data.map((point, index) => {
          const height = ((point - min) / range) * 100
          return (
            <div
              key={index}
              className="flex-1 rounded-t-sm transition-all duration-500 group-hover:opacity-80"
              style={{
                backgroundColor: color,
                height: `${Math.max(height, 10)}%`,
                opacity: 0.7 + (index / data.length) * 0.3,
              }}
            />
          )
        })}
      </div>
    </div>
  )
}
