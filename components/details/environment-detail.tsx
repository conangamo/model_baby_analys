"use client"

import { ArrowLeft, Droplets, Wind, Thermometer } from "lucide-react"
import { useState } from "react"

export default function EnvironmentDetail({ onBack }: { onBack: () => void }) {
  const [targetTemp, setTargetTemp] = useState(24)
  const [targetHumidity, setTargetHumidity] = useState(65)
  const [autoMode, setAutoMode] = useState(true)

  return (
    <div className="h-full bg-gradient-to-b from-cyan-50 to-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-cyan-400 to-cyan-500 p-6 pb-8 rounded-b-[2rem] shadow-lg">
        <button onClick={onBack} className="mb-4 text-white hover:scale-110 transition-transform">
          <ArrowLeft className="w-6 h-6" />
        </button>
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center">
            <Droplets className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Môi trường</h1>
            <p className="text-white/90 text-sm">Nhiệt độ & độ ẩm</p>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Current Status */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gradient-to-br from-orange-400 to-orange-500 rounded-3xl p-6 shadow-lg text-white">
            <Thermometer className="w-8 h-8 mb-3 opacity-80" />
            <p className="text-sm opacity-90 mb-1">Nhiệt độ</p>
            <p className="text-4xl font-bold">24°C</p>
          </div>
          <div className="bg-gradient-to-br from-cyan-400 to-cyan-500 rounded-3xl p-6 shadow-lg text-white">
            <Droplets className="w-8 h-8 mb-3 opacity-80" />
            <p className="text-sm opacity-90 mb-1">Độ ẩm</p>
            <p className="text-4xl font-bold">65%</p>
          </div>
        </div>

        {/* Auto Mode Toggle */}
        <div className="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-semibold">Chế độ tự động</p>
              <p className="text-sm text-gray-600">Điều chỉnh thông minh</p>
            </div>
            <button
              onClick={() => setAutoMode(!autoMode)}
              className={`w-14 h-8 rounded-full transition-all ${autoMode ? "bg-cyan-500" : "bg-gray-200"} relative`}
            >
              <div
                className={`w-6 h-6 bg-white rounded-full absolute top-1 transition-all shadow-md ${
                  autoMode ? "left-7" : "left-1"
                }`}
              />
            </button>
          </div>
        </div>

        {/* Temperature Control */}
        <div className="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <div className="flex items-center gap-2 mb-4">
            <Thermometer className="w-5 h-5 text-orange-500" />
            <span className="font-semibold">Nhiệt độ mục tiêu</span>
          </div>
          <div className="flex items-center justify-between mb-4">
            <button
              onClick={() => setTargetTemp(Math.max(18, targetTemp - 1))}
              className="w-12 h-12 rounded-full bg-gray-200 hover:bg-gray-300 transition-all font-bold text-xl"
            >
              -
            </button>
            <div className="text-center">
              <p className="text-5xl font-bold text-orange-500">{targetTemp}°C</p>
            </div>
            <button
              onClick={() => setTargetTemp(Math.min(30, targetTemp + 1))}
              className="w-12 h-12 rounded-full bg-gray-200 hover:bg-gray-300 transition-all font-bold text-xl"
            >
              +
            </button>
          </div>
          <div className="flex justify-between text-xs text-gray-600">
            <span>18°C</span>
            <span>30°C</span>
          </div>
        </div>

        {/* Humidity Control */}
        <div className="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <div className="flex items-center gap-2 mb-4">
            <Droplets className="w-5 h-5 text-cyan-500" />
            <span className="font-semibold">Độ ẩm mục tiêu</span>
          </div>
          <div className="flex items-center justify-between mb-4">
            <button
              onClick={() => setTargetHumidity(Math.max(40, targetHumidity - 5))}
              className="w-12 h-12 rounded-full bg-gray-200 hover:bg-gray-300 transition-all font-bold text-xl"
            >
              -
            </button>
            <div className="text-center">
              <p className="text-5xl font-bold text-cyan-500">{targetHumidity}%</p>
            </div>
            <button
              onClick={() => setTargetHumidity(Math.min(80, targetHumidity + 5))}
              className="w-12 h-12 rounded-full bg-gray-200 hover:bg-gray-300 transition-all font-bold text-xl"
            >
              +
            </button>
          </div>
          <div className="flex justify-between text-xs text-gray-600">
            <span>40%</span>
            <span>80%</span>
          </div>
        </div>

        {/* Device Status */}
        <div className="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <h3 className="font-semibold mb-4">Trạng thái thiết bị</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-gray-200 rounded-xl">
              <div className="flex items-center gap-3">
                <Wind className="w-5 h-5 text-cyan-500" />
                <span className="text-sm">Quạt điều hòa</span>
              </div>
              <span className="text-sm font-medium text-green-600">Đang bật</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-200 rounded-xl">
              <div className="flex items-center gap-3">
                <Droplets className="w-5 h-5 text-cyan-500" />
                <span className="text-sm">Máy tạo ẩm</span>
              </div>
              <span className="text-sm font-medium text-gray-600">Tắt</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
