"use client"

import { ArrowLeft, Thermometer, TrendingUp, AlertCircle } from "lucide-react"

export default function BodyTempDetail({ onBack }: { onBack: () => void }) {
  const tempHistory = [
    { time: "00:00", temp: 36.5 },
    { time: "02:00", temp: 36.6 },
    { time: "04:00", temp: 36.7 },
    { time: "06:00", temp: 36.8 },
    { time: "08:00", temp: 36.8 },
    { time: "10:00", temp: 36.9 },
    { time: "12:00", temp: 36.8 },
  ]

  const maxTemp = Math.max(...tempHistory.map((h) => h.temp))
  const minTemp = Math.min(...tempHistory.map((h) => h.temp))

  return (
    <div className="h-full bg-gradient-to-b from-orange-50 to-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-400 to-orange-500 p-6 pb-8 rounded-b-[2rem] shadow-lg">
        <button onClick={onBack} className="mb-4 text-white hover:scale-110 transition-transform">
          <ArrowLeft className="w-6 h-6" />
        </button>
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center">
            <Thermometer className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Thân nhiệt</h1>
            <p className="text-white/90 text-sm">Theo dõi liên tục</p>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Current Temperature */}
        <div className="bg-white rounded-3xl p-8 shadow-lg border border-gray-200 text-center">
          <p className="text-sm text-gray-600 mb-2">Nhiệt độ hiện tại</p>
          <div className="text-6xl font-bold text-orange-500 mb-2">36.8°C</div>
          <div className="flex items-center justify-center gap-2 text-green-600">
            <TrendingUp className="w-4 h-4" />
            <span className="text-sm font-medium">Bình thường</span>
          </div>
        </div>

        {/* Temperature Range */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-white rounded-2xl p-4 shadow border border-gray-200">
            <p className="text-xs text-gray-600 mb-1">Cao nhất</p>
            <p className="text-2xl font-bold text-orange-600">{maxTemp}°C</p>
            <p className="text-xs text-gray-600 mt-1">Hôm nay</p>
          </div>
          <div className="bg-white rounded-2xl p-4 shadow border border-gray-200">
            <p className="text-xs text-gray-600 mb-1">Thấp nhất</p>
            <p className="text-2xl font-bold text-cyan-600">{minTemp}°C</p>
            <p className="text-xs text-gray-600 mt-1">Hôm nay</p>
          </div>
        </div>

        {/* Temperature Chart */}
        <div className="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <h3 className="font-semibold mb-4">Biểu đồ nhiệt độ 24h</h3>
          <div className="relative h-48">
            <svg className="w-full h-full" viewBox="0 0 300 150">
              {/* Grid lines */}
              {[0, 1, 2, 3, 4].map((i) => (
                <line key={i} x1="0" y1={30 + i * 30} x2="300" y2={30 + i * 30} stroke="#e5e7eb" strokeWidth="1" />
              ))}

              {/* Temperature line */}
              <polyline
                points={tempHistory
                  .map((h, i) => {
                    const x = (i / (tempHistory.length - 1)) * 280 + 10
                    const y = 150 - ((h.temp - 36.4) / 0.6) * 120
                    return `${x},${y}`
                  })
                  .join(" ")}
                fill="none"
                stroke="url(#tempGradient)"
                strokeWidth="3"
                strokeLinecap="round"
              />

              {/* Data points */}
              {tempHistory.map((h, i) => {
                const x = (i / (tempHistory.length - 1)) * 280 + 10
                const y = 150 - ((h.temp - 36.4) / 0.6) * 120
                return <circle key={i} cx={x} cy={y} r="4" fill="#f97316" />
              })}

              <defs>
                <linearGradient id="tempGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#fb923c" />
                  <stop offset="100%" stopColor="#f97316" />
                </linearGradient>
              </defs>
            </svg>

            {/* Time labels */}
            <div className="flex justify-between mt-2 text-xs text-gray-600">
              {tempHistory.map((h, i) => (
                <span key={i}>{h.time}</span>
              ))}
            </div>
          </div>
        </div>

        {/* Alert Settings */}
        <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-amber-600 mt-0.5" />
          <div className="flex-1">
            <p className="text-sm font-medium text-amber-900">Cảnh báo nhiệt độ</p>
            <p className="text-xs text-amber-700 mt-1">Thông báo khi nhiệt độ &gt; 37.5°C hoặc &lt; 36.0°C</p>
          </div>
        </div>
      </div>
    </div>
  )
}
