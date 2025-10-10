"use client"

import { ArrowLeft, Music, Play, Pause, Volume2, RotateCw } from "lucide-react"
import { useState } from "react"

export default function RockMusicDetail({ onBack }: { onBack: () => void }) {
  const [isPlaying, setIsPlaying] = useState(true)
  const [isRocking, setIsRocking] = useState(true)
  const [volume, setVolume] = useState(60)
  const [rockSpeed, setRockSpeed] = useState(3)

  const songs = [
    { id: 1, name: "Ru con", duration: "3:45", active: true },
    { id: 2, name: "Twinkle Twinkle", duration: "2:30", active: false },
    { id: 3, name: "Brahms Lullaby", duration: "4:15", active: false },
    { id: 4, name: "Âm thanh tự nhiên", duration: "10:00", active: false },
  ]

  return (
    <div className="h-full bg-gradient-to-b from-pink-50 to-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-pink-400 to-pink-500 p-6 pb-8 rounded-b-[2rem] shadow-lg">
        <button onClick={onBack} className="mb-4 text-white hover:scale-110 transition-transform">
          <ArrowLeft className="w-6 h-6" />
        </button>
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center">
            <Music className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Lắc nôi & Nhạc</h1>
            <p className="text-white/90 text-sm">Điều khiển tự động</p>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Control Panel */}
        <div className="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <div className="flex items-center justify-between mb-6">
            <div>
              <p className="text-sm text-gray-600">Đang phát</p>
              <p className="text-lg font-semibold">Ru con</p>
            </div>
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="w-14 h-14 bg-gradient-to-br from-pink-400 to-pink-500 rounded-full flex items-center justify-center text-white hover:scale-110 transition-transform shadow-lg"
            >
              {isPlaying ? <Pause className="w-6 h-6" /> : <Play className="w-6 h-6 ml-1" />}
            </button>
          </div>

          {/* Volume Control */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Volume2 className="w-5 h-5 text-pink-500" />
                <span className="text-sm font-medium">Âm lượng</span>
              </div>
              <span className="text-sm text-gray-600">{volume}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="100"
              value={volume}
              onChange={(e) => setVolume(Number(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-pink-500"
            />
          </div>
        </div>

        {/* Rocking Control */}
        <div className="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <RotateCw className="w-5 h-5 text-cyan-500" />
              <span className="text-sm font-medium">Lắc nôi</span>
            </div>
            <button
              onClick={() => setIsRocking(!isRocking)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                isRocking ? "bg-cyan-500 text-white" : "bg-gray-200 text-gray-800"
              }`}
            >
              {isRocking ? "Đang bật" : "Tắt"}
            </button>
          </div>

          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm">Tốc độ</span>
              <span className="text-sm text-gray-600">Cấp {rockSpeed}</span>
            </div>
            <input
              type="range"
              min="1"
              max="5"
              value={rockSpeed}
              onChange={(e) => setRockSpeed(Number(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-cyan-500"
            />
          </div>
        </div>

        {/* Song List */}
        <div className="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <h3 className="font-semibold mb-4">Danh sách nhạc</h3>
          <div className="space-y-2">
            {songs.map((song) => (
              <div
                key={song.id}
                className={`p-4 rounded-2xl transition-all cursor-pointer ${
                  song.active ? "bg-pink-100 border-2 border-pink-300" : "bg-gray-200 hover:bg-gray-300"
                }`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-sm">{song.name}</p>
                    <p className="text-xs text-gray-600">{song.duration}</p>
                  </div>
                  {song.active && <Music className="w-4 h-4 text-pink-500 animate-pulse-soft" />}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
