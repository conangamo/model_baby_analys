"use client"

import { Moon, Clock } from "lucide-react"

export default function StatusBar() {
  return (
    <div className="bg-white/20 backdrop-blur-md rounded-2xl p-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-white/30 rounded-xl flex items-center justify-center">
            <Moon className="w-5 h-5 text-white" />
          </div>
          <div>
            <p className="text-white font-medium">Chế độ ngủ</p>
            <p className="text-white/80 text-sm">Đang hoạt động</p>
          </div>
        </div>

        <div className="flex items-center gap-2 bg-white/30 px-3 py-2 rounded-xl">
          <Clock className="w-4 h-4 text-white" />
          <span className="text-white text-sm font-medium">2h 15p</span>
        </div>
      </div>
    </div>
  )
}
