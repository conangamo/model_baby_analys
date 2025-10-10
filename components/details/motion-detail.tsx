"use client"

import { ArrowLeft, Video, Moon, AlertTriangle } from "lucide-react"

export default function MotionDetail({ onBack }: { onBack: () => void }) {
  const motionData = [
    { time: "00:00", activity: 2 },
    { time: "02:00", activity: 1 },
    { time: "04:00", activity: 3 },
    { time: "06:00", activity: 5 },
    { time: "08:00", activity: 8 },
    { time: "10:00", activity: 6 },
    { time: "12:00", activity: 4 },
  ]

  const sleepPhases = [
    { phase: "Ngủ sâu", duration: "4.5h", percentage: 60, color: "bg-indigo-500" },
    { phase: "Ngủ nông", duration: "2h", percentage: 27, color: "bg-purple-400" },
    { phase: "Thức giấc", duration: "1h", percentage: 13, color: "bg-pink-400" },
  ]

  return (
    <div className="h-full bg-gradient-to-b from-indigo-50 to-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-400 to-indigo-500 p-6 pb-8 rounded-b-[2rem] shadow-lg">
        <button onClick={onBack} className="mb-4 text-white hover:scale-110 transition-transform">
          <ArrowLeft className="w-6 h-6" />
        </button>
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center">
            <Video className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Giám sát chuyển động</h1>
            <p className="text-white/90 text-sm">Camera thông minh</p>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Live Camera View */}
        <div className="bg-white rounded-3xl overflow-hidden shadow-lg border border-gray-200">
          <div className="relative aspect-video bg-gradient-to-br from-indigo-900 to-purple-900 flex items-center justify-center">
            <div className="text-center text-white">
              <Video className="w-16 h-16 mx-auto mb-3 opacity-50" />
              <p className="text-sm opacity-75">Camera đang hoạt động</p>
            </div>
            <div className="absolute top-4 left-4 bg-red-500 text-white text-xs px-3 py-1 rounded-full flex items-center gap-2 animate-pulse-soft">
              <div className="w-2 h-2 bg-white rounded-full" />
              LIVE
            </div>
          </div>
          <div className="p-4 bg-gray-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Moon className="w-5 h-5 text-indigo-600" />
                <span className="text-sm font-medium">Đang ngủ sâu</span>
              </div>
              <span className="text-xs text-gray-600">Cập nhật 1 phút trước</span>
            </div>
          </div>
        </div>

        {/* Sleep Quality */}
        <div className="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <h3 className="font-semibold mb-4">Chất lượng giấc ngủ</h3>
          <div className="space-y-4">
            {sleepPhases.map((phase) => (
              <div key={phase.phase}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">{phase.phase}</span>
                  <span className="text-sm text-gray-600">{phase.duration}</span>
                </div>
                <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
                  <div className={`h-full ${phase.color} rounded-full`} style={{ width: `${phase.percentage}%` }} />
                </div>
              </div>
            ))}
          </div>
          <div className="mt-6 p-4 bg-indigo-50 rounded-2xl text-center">
            <p className="text-sm text-gray-600 mb-1">Tổng thời gian ngủ</p>
            <p className="text-3xl font-bold text-indigo-600">7.5 giờ</p>
          </div>
        </div>

        {/* Activity Chart */}
        <div className="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <h3 className="font-semibold mb-4">Mức độ hoạt động 24h</h3>
          <div className="relative h-32">
            <div className="flex items-end justify-between h-full gap-2">
              {motionData.map((data, index) => (
                <div key={index} className="flex-1 flex flex-col items-center gap-2">
                  <div className="w-full bg-gray-200 rounded-t-lg relative" style={{ height: "100%" }}>
                    <div
                      className="absolute bottom-0 w-full bg-gradient-to-t from-indigo-500 to-indigo-400 rounded-t-lg transition-all"
                      style={{ height: `${(data.activity / 10) * 100}%` }}
                    />
                  </div>
                  <span className="text-xs text-gray-600">{data.time}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Alerts */}
        <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4 flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-amber-600 mt-0.5" />
          <div className="flex-1">
            <p className="text-sm font-medium text-amber-900">Cảnh báo chuyển động</p>
            <p className="text-xs text-amber-700 mt-1">Thông báo khi phát hiện chuyển động bất thường</p>
          </div>
        </div>
      </div>
    </div>
  )
}
