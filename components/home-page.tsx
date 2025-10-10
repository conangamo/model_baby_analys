"use client"

import { useState } from "react"
import { Baby, Music, Thermometer, Droplets, Mic, Video, ChevronRight, Bell } from "lucide-react"
import FeatureCard from "./feature-card"
import StatusBar from "./status-bar"
import MiniChart from "./mini-chart"
import RockMusicDetail from "./details/rock-music-detail"
import BodyTempDetail from "./details/body-temp-detail"
import EnvironmentDetail from "./details/environment-detail"
import CryAnalysisDetail from "./details/cry-analysis-detail"
import MotionDetail from "./details/motion-detail"
import NotificationPanel from "./notification-panel"

export default function HomePage() {
  const [selectedFeature, setSelectedFeature] = useState<string | null>(null)
  const [showNotifications, setShowNotifications] = useState(false)

  const features = [
    {
      id: "rock",
      title: "Lắc nôi & Nhạc",
      subtitle: "Tự động ru ngủ",
      icon: Music,
      color: "bg-gradient-to-br from-[#FFB3D9] to-[#FFC0E0]",
      status: "active" as const,
      value: "Đang phát",
    },
    {
      id: "temp",
      title: "Thân nhiệt",
      subtitle: "Theo dõi liên tục",
      icon: Thermometer,
      color: "bg-gradient-to-br from-[#FFD4B2] to-[#FFE0C7]",
      status: "normal" as const,
      value: "36.8°C",
    },
    {
      id: "environment",
      title: "Môi trường",
      subtitle: "Nhiệt độ & độ ẩm",
      icon: Droplets,
      color: "bg-gradient-to-br from-[#B4D4FF] to-[#C7E0FF]",
      status: "normal" as const,
      value: "24°C • 65%",
    },
    {
      id: "cry",
      title: "Phân tích tiếng khóc",
      subtitle: "AI nhận diện",
      icon: Mic,
      color: "bg-gradient-to-br from-[#E0BBE4] to-[#EDD0F0]",
      status: "idle" as const,
      value: "Yên tĩnh",
    },
    {
      id: "motion",
      title: "Giám sát chuyển động",
      subtitle: "Camera thông minh",
      icon: Video,
      color: "bg-gradient-to-br from-[#D4C5F9] to-[#E3D9FC]",
      status: "active" as const,
      value: "Đang ngủ",
    },
  ]

  if (selectedFeature) {
    return (
      <div className="h-full overflow-y-auto">
        {selectedFeature === "rock" && <RockMusicDetail onBack={() => setSelectedFeature(null)} />}
        {selectedFeature === "temp" && <BodyTempDetail onBack={() => setSelectedFeature(null)} />}
        {selectedFeature === "environment" && <EnvironmentDetail onBack={() => setSelectedFeature(null)} />}
        {selectedFeature === "cry" && <CryAnalysisDetail onBack={() => setSelectedFeature(null)} />}
        {selectedFeature === "motion" && <MotionDetail onBack={() => setSelectedFeature(null)} />}
      </div>
    )
  }

  return (
    <div className="h-full overflow-y-auto relative">
      {/* Header */}
      <div className="bg-gradient-to-r from-[#FFB3D9] via-[#E0BBE4] to-[#B4D4FF] p-6 pb-8 rounded-b-[2rem] shadow-lg">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-800 mb-1">Neo Cradle</h1>
            <p className="text-gray-700 text-sm">Neo Cradle - Nôi thông minh</p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="relative w-12 h-12 bg-white/60 backdrop-blur-sm rounded-2xl flex items-center justify-center hover:bg-white/80 transition-all duration-300 hover:scale-105 active:scale-95 shadow-md"
            >
              <Bell className="w-5 h-5 text-gray-700" />
              <span className="absolute -top-1 -right-1 w-5 h-5 bg-[#FFB3D9] rounded-full text-gray-800 text-xs flex items-center justify-center font-bold shadow-md animate-pulse-soft">
                3
              </span>
            </button>
            <div className="w-12 h-12 bg-white/60 backdrop-blur-sm rounded-2xl flex items-center justify-center animate-float shadow-md">
              <Baby className="w-6 h-6 text-gray-700" />
            </div>
          </div>
        </div>

        <StatusBar />
      </div>

      {/* Main Content */}
      <div className="px-4 py-6 space-y-4">
        {/* Quick Stats */}
        <div className="grid grid-cols-2 gap-3 mb-2">
          <MiniChart
            title="Nhiệt độ phòng"
            value="24°C"
            trend="stable"
            data={[22, 23, 23.5, 24, 24, 23.8, 24]}
            color="#B4D4FF"
          />
          <MiniChart title="Độ ẩm" value="65%" trend="up" data={[60, 62, 63, 64, 65, 65, 65]} color="#B5EAD7" />
        </div>

        {/* Feature Cards */}
        <div className="space-y-3">
          <h2 className="text-lg font-semibold text-gray-800 px-1">Chức năng chính</h2>
          {features.map((feature, index) => (
            <div
              key={feature.id}
              className="animate-slide-up cursor-pointer"
              style={{ animationDelay: `${index * 0.1}s` }}
              onClick={() => setSelectedFeature(feature.id)}
            >
              <div className="relative">
                <FeatureCard {...feature} />
                <ChevronRight className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-600" />
              </div>
            </div>
          ))}
        </div>
      </div>

      <NotificationPanel isOpen={showNotifications} onClose={() => setShowNotifications(false)} />
    </div>
  )
}
