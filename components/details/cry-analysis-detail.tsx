"use client"

import { ArrowLeft, Mic, Activity, AlertCircle } from "lucide-react"

export default function CryAnalysisDetail({ onBack }: { onBack: () => void }) {
  const cryHistory = [
    { time: "14:30", type: "Đói", duration: "2 phút", intensity: "Trung bình" },
    { time: "11:15", type: "Buồn ngủ", duration: "5 phút", intensity: "Nhẹ" },
    { time: "08:45", type: "Khó chịu", duration: "3 phút", intensity: "Cao" },
    { time: "06:20", type: "Đói", duration: "4 phút", intensity: "Cao" },
    { time: "04:10", type: "Ợ hơi", duration: "1 phút", intensity: "Cao" },

  ]

  const cryTypes = [
    { type: "Đói", count: 8, color: "bg-orange-500" },
    { type: "Buồn ngủ", count: 5, color: "bg-purple-500" },
    { type: "Khó chịu", count: 3, color: "bg-red-500" },
    { type: "Đau", count: 1, color: "bg-pink-500" },
    { type: "Ợ hơi", count: 1, color: "bg-blue-500" },
  ]

  return (
    <div className="h-full bg-gradient-to-b from-purple-50 to-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-400 to-purple-500 p-6 pb-8 rounded-b-[2rem] shadow-lg">
        <button onClick={onBack} className="mb-4 text-white hover:scale-110 transition-transform">
          <ArrowLeft className="w-6 h-6" />
        </button>
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center">
            <Mic className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Phân tích tiếng khóc</h1>
            <p className="text-white/90 text-sm">AI nhận diện thông minh</p>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Current Status */}
        <div className="bg-white rounded-3xl p-8 shadow-lg border border-gray-200 text-center">
          <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Activity className="w-10 h-10 text-green-600" />
          </div>
          <p className="text-2xl font-bold mb-2">Yên tĩnh</p>
          <p className="text-sm text-gray-600">Bé đang ngủ ngon</p>
        </div>

        {/* Cry Statistics */}
        <div className="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <h3 className="font-semibold mb-4">Thống kê hôm nay</h3>
          <div className="space-y-3">
            {cryTypes.map((item) => (
              <div key={item.type}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">{item.type}</span>
                  <span className="text-sm text-gray-600">{item.count} lần</span>
                </div>
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className={`h-full ${item.color} rounded-full`}
                    style={{ width: `${(item.count / 17) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Cry History */}
        <div className="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <h3 className="font-semibold mb-4">Lịch sử khóc</h3>
          <div className="space-y-3">
            {cryHistory.map((item, index) => (
              <div key={index} className="p-4 bg-gray-200 rounded-2xl">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-sm">{item.type}</span>
                  <span className="text-xs text-gray-600">{item.time}</span>
                </div>
                <div className="flex items-center gap-4 text-xs text-gray-600">
                  <span>⏱️ {item.duration}</span>
                  <span>📊 {item.intensity}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Insights */}
        <div className="bg-purple-50 border border-purple-200 rounded-2xl p-4 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-purple-600 mt-0.5" />
          <div className="flex-1">
            <p className="text-sm font-medium text-purple-900">Gợi ý từ AI</p>
            <p className="text-xs text-purple-700 mt-1">
              Bé thường khóc vào khoảng 14:00-15:00. Có thể bé đói hoặc cần thay tã.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
