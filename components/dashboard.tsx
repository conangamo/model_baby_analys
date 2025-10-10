"use client"

import { useState } from "react"
import { Home, BarChart3, Settings } from "lucide-react"
import HomePage from "./home-page"
import StatsPage from "./stats-page"
import SettingsPage from "./settings-page"

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("home")

  return (
    <div className="flex flex-col h-screen max-w-md mx-auto bg-gray-50">
      <div className="flex-1 overflow-hidden">
        {activeTab === "home" && <HomePage />}
        {activeTab === "stats" && <StatsPage />}
        {activeTab === "settings" && <SettingsPage />}
      </div>

      {/* Bottom Navigation */}
      <nav className="bg-white border-t border-gray-200 px-6 py-4 rounded-t-3xl shadow-lg">
        <div className="flex items-center justify-around">
          <button
            onClick={() => setActiveTab("home")}
            className={`flex flex-col items-center gap-1 transition-all duration-300 ${
              activeTab === "home" ? "text-[#FFB3D9] scale-110" : "text-gray-600 hover:text-gray-800"
            }`}
          >
            <Home className="w-6 h-6" />
            <span className="text-xs font-medium">Trang chủ</span>
          </button>

          <button
            onClick={() => setActiveTab("stats")}
            className={`flex flex-col items-center gap-1 transition-all duration-300 ${
              activeTab === "stats" ? "text-[#FFB3D9] scale-110" : "text-gray-600 hover:text-gray-800"
            }`}
          >
            <BarChart3 className="w-6 h-6" />
            <span className="text-xs font-medium">Thống kê</span>
          </button>

          <button
            onClick={() => setActiveTab("settings")}
            className={`flex flex-col items-center gap-1 transition-all duration-300 ${
              activeTab === "settings" ? "text-[#FFB3D9] scale-110" : "text-gray-600 hover:text-gray-800"
            }`}
          >
            <Settings className="w-6 h-6" />
            <span className="text-xs font-medium">Cài đặt</span>
          </button>
        </div>
      </nav>
    </div>
  )
}
