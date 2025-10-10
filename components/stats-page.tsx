"use client"

import { TrendingUp, Clock, Activity, BarChart3 } from "lucide-react"

export default function StatsPage() {
  const weeklyData = [
    { day: "T2", sleep: 7.5, cry: 5, temp: 36.7 },
    { day: "T3", sleep: 8.0, cry: 3, temp: 36.8 },
    { day: "T4", sleep: 7.2, cry: 6, temp: 36.6 },
    { day: "T5", sleep: 8.5, cry: 2, temp: 36.8 },
    { day: "T6", sleep: 7.8, cry: 4, temp: 36.7 },
    { day: "T7", sleep: 8.2, cry: 3, temp: 36.9 },
    { day: "CN", sleep: 7.5, cry: 5, temp: 36.8 },
  ]

  const maxSleep = Math.max(...weeklyData.map((d) => d.sleep))
  const maxCry = Math.max(...weeklyData.map((d) => d.cry))

  return (
    <div className="h-full overflow-y-auto bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-[#FFB3D9] via-[#E0BBE4] to-[#B4D4FF] p-6 pb-8 rounded-b-[2rem] shadow-lg">
        <div className="flex items-center gap-3 mb-2">
          <BarChart3 className="w-8 h-8 text-white" />
          <h1 className="text-2xl font-bold text-white">Thống kê</h1>
        </div>
        <p className="text-white/90 text-sm">Phân tích dữ liệu 7 ngày</p>
      </div>

      <div className="p-6 space-y-6">
        {/* Summary Cards */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gradient-to-br from-indigo-400 to-indigo-500 rounded-3xl p-5 shadow-lg text-white">
            <Clock className="w-6 h-6 mb-2 opacity-80" />
            <p className="text-sm opacity-90 mb-1">Giấc ngủ TB</p>
            <p className="text-3xl font-bold">7.8h</p>
            <div className="flex items-center gap-1 mt-2 text-xs">
              <TrendingUp className="w-3 h-3" />
              <span>+0.5h tuần này</span>
            </div>
          </div>

          <div className="bg-gradient-to-br from-purple-400 to-purple-500 rounded-3xl p-5 shadow-lg text-white">
            <Activity className="w-6 h-6 mb-2 opacity-80" />
            <p className="text-sm opacity-90 mb-1">Khóc TB/ngày</p>
            <p className="text-3xl font-bold">4 lần</p>
            <div className="flex items-center gap-1 mt-2 text-xs">
              <TrendingUp className="w-3 h-3 rotate-180" />
              <span>-1 lần tuần này</span>
            </div>
          </div>
        </div>

        {/* Sleep Chart */}
        <div className="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <h3 className="font-semibold mb-4">Thời gian ngủ (giờ)</h3>
          <div className="relative h-48">
            <svg className="w-full h-full" viewBox="0 0 300 150">
              {/* Grid lines */}
              {[0, 1, 2, 3, 4].map((i) => (
                <line key={i} x1="0" y1={30 + i * 30} x2="300" y2={30 + i * 30} stroke="#e5e7eb" strokeWidth="1" />
              ))}

              {/* Sleep area */}
              <defs>
                <linearGradient id="sleepGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stopColor="#818cf8" stopOpacity="0.5" />
                  <stop offset="100%" stopColor="#818cf8" stopOpacity="0.1" />
                </linearGradient>
              </defs>

              <polygon
                points={`0,150 ${weeklyData
                  .map((d, i) => {
                    const x = (i / (weeklyData.length - 1)) * 280 + 10
                    const y = 150 - ((d.sleep - 6) / 3) * 120
                    return `${x},${y}`
                  })
                  .join(" ")} 300,150`}
                fill="url(#sleepGradient)"
              />

              {/* Sleep line */}
              <polyline
                points={weeklyData
                  .map((d, i) => {
                    const x = (i / (weeklyData.length - 1)) * 280 + 10
                    const y = 150 - ((d.sleep - 6) / 3) * 120
                    return `${x},${y}`
                  })
                  .join(" ")}
                fill="none"
                stroke="#6366f1"
                strokeWidth="3"
                strokeLinecap="round"
              />

              {/* Data points */}
              {weeklyData.map((d, i) => {
                const x = (i / (weeklyData.length - 1)) * 280 + 10
                const y = 150 - ((d.sleep - 6) / 3) * 120
                return <circle key={i} cx={x} cy={y} r="4" fill="#6366f1" />
              })}
            </svg>

            {/* Day labels */}
            <div className="flex justify-between mt-2 text-xs text-gray-600">
              {weeklyData.map((d, i) => (
                <span key={i}>{d.day}</span>
              ))}
            </div>
          </div>
        </div>

        {/* Cry Frequency Chart */}
        <div className="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <h3 className="font-semibold mb-4">Tần suất khóc (lần/ngày)</h3>
          <div className="flex items-end justify-between h-40 gap-2">
            {weeklyData.map((data, index) => (
              <div key={index} className="flex-1 flex flex-col items-center gap-2">
                <div className="w-full bg-gray-200 rounded-t-xl relative" style={{ height: "100%" }}>
                  <div
                    className="absolute bottom-0 w-full bg-gradient-to-t from-purple-500 to-purple-400 rounded-t-xl transition-all"
                    style={{ height: `${(data.cry / maxCry) * 100}%` }}
                  />
                  <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-xs font-medium">{data.cry}</span>
                </div>
                <span className="text-xs text-gray-600">{data.day}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Temperature Trend */}
        <div className="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <h3 className="font-semibold mb-4">Xu hướng thân nhiệt (°C)</h3>
          <div className="relative h-32">
            <svg className="w-full h-full" viewBox="0 0 300 100">
              {/* Temperature line */}
              <polyline
                points={weeklyData
                  .map((d, i) => {
                    const x = (i / (weeklyData.length - 1)) * 280 + 10
                    const y = 100 - ((d.temp - 36.5) / 0.5) * 80
                    return `${x},${y}`
                  })
                  .join(" ")}
                fill="none"
                stroke="#f97316"
                strokeWidth="3"
                strokeLinecap="round"
              />

              {/* Data points */}
              {weeklyData.map((d, i) => {
                const x = (i / (weeklyData.length - 1)) * 280 + 10
                const y = 100 - ((d.temp - 36.5) / 0.5) * 80
                return (
                  <g key={i}>
                    <circle cx={x} cy={y} r="4" fill="#f97316" />
                    <text x={x} y={y - 10} textAnchor="middle" fontSize="10" fill="#6b7280">
                      {d.temp}
                    </text>
                  </g>
                )
              })}
            </svg>

            {/* Day labels */}
            <div className="flex justify-between mt-2 text-xs text-gray-600">
              {weeklyData.map((d, i) => (
                <span key={i}>{d.day}</span>
              ))}
            </div>
          </div>
        </div>

        {/* Insights */}
        <div className="bg-gradient-to-br from-pink-50 to-purple-50 border border-pink-200 rounded-3xl p-6">
          <h3 className="font-semibold mb-3 text-pink-900">Nhận xét từ AI</h3>
          <ul className="space-y-2 text-sm text-pink-800">
            <li className="flex items-start gap-2">
              <span className="text-pink-500 mt-0.5">•</span>
              <span>Chất lượng giấc ngủ đang cải thiện, tăng 0.5h so với tuần trước</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-pink-500 mt-0.5">•</span>
              <span>Tần suất khóc giảm, bé đang thích nghi tốt với môi trường</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-pink-500 mt-0.5">•</span>
              <span>Thân nhiệt ổn định trong khoảng bình thường</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
}
