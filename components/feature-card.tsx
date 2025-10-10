"use client"

import type { LucideIcon } from "lucide-react"
import { useState } from "react"
import { ChevronRight } from "lucide-react"

interface FeatureCardProps {
  title: string
  subtitle: string
  icon: LucideIcon
  color: string
  status: "active" | "normal" | "idle"
  value: string
}

export default function FeatureCard({ title, subtitle, icon: Icon, color, status, value }: FeatureCardProps) {
  const [isPressed, setIsPressed] = useState(false)

  const statusColors = {
    active: "bg-green-100 text-green-700",
    normal: "bg-blue-100 text-blue-700",
    idle: "bg-gray-100 text-gray-600",
  }

  return (
    <button
      onMouseDown={() => setIsPressed(true)}
      onMouseUp={() => setIsPressed(false)}
      onMouseLeave={() => setIsPressed(false)}
      className={`w-full bg-white rounded-3xl p-5 shadow-md hover:shadow-xl transition-all duration-300 group ${
        isPressed ? "scale-95" : "hover:scale-[1.02]"
      }`}
    >
      <div className="flex items-center gap-4">
        {/* Icon */}
        <div
          className={`${color} w-16 h-16 rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300`}
        >
          <Icon className="w-8 h-8 text-white" />
        </div>

        {/* Content */}
        <div className="flex-1 text-left">
          <h3 className="font-semibold text-gray-800 mb-1">{title}</h3>
          <p className="text-sm text-gray-600 mb-2">{subtitle}</p>
          <div className="flex items-center gap-2">
            <span className={`text-xs px-3 py-1 rounded-full font-medium ${statusColors[status]}`}>{value}</span>
          </div>
        </div>

        {/* Arrow */}
        <ChevronRight className="w-5 h-5 text-gray-600 group-hover:translate-x-1 transition-transform duration-300" />
      </div>
    </button>
  )
}
