"use client"

import { X, Moon, Thermometer, Droplets, AlertCircle, CheckCircle, Clock } from "lucide-react"

interface NotificationPanelProps {
  isOpen: boolean
  onClose: () => void
}

interface Notification {
  id: string
  title: string
  message: string
  time: string
  type: "info" | "success" | "warning" | "alert"
  icon: any
  read: boolean
}

export default function NotificationPanel({ isOpen, onClose }: NotificationPanelProps) {
  const notifications: Notification[] = [
    {
      id: "1",
      title: "Chế độ ngủ",
      message: "Đang hoạt động",
      time: "2 phút trước",
      type: "info",
      icon: Moon,
      read: false,
    },
    {
      id: "2",
      title: "Nhiệt độ phòng",
      message: "Đã điều chỉnh xuống 24°C",
      time: "15 phút trước",
      type: "success",
      icon: Thermometer,
      read: false,
    },
    {
      id: "3",
      title: "Độ ẩm cao",
      message: "Độ ẩm đạt 68%, đã bật quạt",
      time: "1 giờ trước",
      type: "warning",
      icon: Droplets,
      read: false,
    },
    {
      id: "4",
      title: "Bé đã thức dậy",
      message: "Phát hiện chuyển động lúc 14:30",
      time: "2 giờ trước",
      type: "info",
      icon: AlertCircle,
      read: true,
    },
    {
      id: "5",
      title: "Nhạc ru ngủ",
      message: "Đã phát xong playlist",
      time: "3 giờ trước",
      type: "success",
      icon: CheckCircle,
      read: true,
    },
  ]

  const getTypeColor = (type: string) => {
    switch (type) {
      case "info":
        return "from-[#B4D4FF] to-[#C7E0FF]"
      case "success":
        return "from-[#B5EAD7] to-[#C9F0E3]"
      case "warning":
        return "from-[#FFF4B7] to-[#FFF8D1]"
      case "alert":
        return "from-[#FFB3D9] to-[#FFC0E0]"
      default:
        return "from-gray-200 to-gray-300"
    }
  }

  return (
    <>
      {/* Backdrop */}
      <div
        className={`fixed inset-0 bg-black/40 backdrop-blur-sm z-40 transition-opacity duration-300 ${
          isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
        }`}
        onClick={onClose}
      />

      {/* Notification Panel */}
      <div
        className={`fixed top-0 right-0 h-full w-full max-w-md bg-gray-50 shadow-2xl z-50 transition-transform duration-300 border-l border-[#FFB3D9]/30 ${
          isOpen ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="bg-gradient-to-r from-[#FFB3D9] via-[#E0BBE4] to-[#B4D4FF] p-6 pb-8 rounded-b-[2rem] shadow-lg">
          <div className="flex items-center justify-between mb-2">
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-1">Thông báo</h2>
              <p className="text-gray-700 text-sm">{notifications.filter((n) => !n.read).length} thông báo mới</p>
            </div>
            <button
              onClick={onClose}
              className="w-10 h-10 bg-white/60 backdrop-blur-sm rounded-xl flex items-center justify-center hover:bg-white/80 transition-all duration-300 hover:scale-105 active:scale-95 shadow-md"
            >
              <X className="w-5 h-5 text-gray-700" />
            </button>
          </div>
        </div>

        {/* Notifications List */}
        <div className="overflow-y-auto h-[calc(100%-140px)] px-4 py-6 space-y-3">
          {notifications.map((notification, index) => {
            const Icon = notification.icon
            return (
              <div
                key={notification.id}
                className={`relative bg-white rounded-2xl p-4 shadow-md border transition-all duration-300 hover:shadow-lg hover:scale-[1.02] cursor-pointer animate-slide-up ${
                  !notification.read ? "border-[#FFB3D9] border-l-4 shadow-[#FFB3D9]/20" : "border-gray-200"
                }`}
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                <div className="flex gap-3">
                  <div
                    className={`w-12 h-12 rounded-xl bg-gradient-to-br ${getTypeColor(notification.type)} flex items-center justify-center flex-shrink-0 shadow-sm`}
                  >
                    <Icon className="w-6 h-6 text-gray-700" />
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-2 mb-1">
                      <h3 className="font-semibold text-gray-800 text-sm">{notification.title}</h3>
                      {!notification.read && (
                        <span className="w-2 h-2 bg-[#FFB3D9] rounded-full flex-shrink-0 mt-1.5 animate-pulse-soft shadow-sm" />
                      )}
                    </div>
                    <p className="text-gray-600 text-sm mb-2 leading-relaxed">{notification.message}</p>
                    <div className="flex items-center gap-1 text-xs text-gray-500">
                      <Clock className="w-3 h-3" />
                      <span>{notification.time}</span>
                    </div>
                  </div>
                </div>
              </div>
            )
          })}
        </div>

        <div className="absolute bottom-0 left-0 right-0 p-4 bg-white border-t border-gray-200">
          <button className="w-full py-3 bg-gradient-to-r from-[#FFB3D9] to-[#E0BBE4] text-gray-800 rounded-xl font-medium hover:shadow-lg transition-all duration-300 hover:scale-[1.02] active:scale-95 shadow-md">
            Đánh dấu tất cả đã đọc
          </button>
        </div>
      </div>
    </>
  )
}
