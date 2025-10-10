"use client"

import { User, Bell, Shield, Info, ChevronRight } from "lucide-react"

export default function SettingsPage() {
  const settingsSections = [
    {
      title: "Tài khoản",
      icon: User,
      items: [
        { label: "Thông tin cá nhân", value: "Nguyễn Văn A" },
        { label: "Email", value: "user@example.com" },
      ],
    },
    {
      title: "Thông báo",
      icon: Bell,
      items: [
        { label: "Cảnh báo nhiệt độ", value: "Bật" },
        { label: "Cảnh báo tiếng khóc", value: "Bật" },
        { label: "Báo cáo hàng ngày", value: "Tắt" },
      ],
    },
    {
      title: "Bảo mật",
      icon: Shield,
      items: [
        { label: "Mã PIN", value: "Đã thiết lập" },
        { label: "Xác thực 2 lớp", value: "Tắt" },
      ],
    },
  ]

  return (
    <div className="h-full overflow-y-auto bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-[#FFB3D9] via-[#E0BBE4] to-[#B4D4FF] p-6 pb-8 rounded-b-[2rem] shadow-lg">
        <div className="flex items-center gap-3 mb-2">
          <User className="w-8 h-8 text-white" />
          <h1 className="text-2xl font-bold text-white">Cài đặt</h1>
        </div>
        <p className="text-white/90 text-sm">Quản lý tài khoản và ứng dụng</p>
      </div>

      <div className="p-6 space-y-6">
        {/* Profile Card */}
        <div className="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-gradient-to-br from-pink-400 to-purple-500 rounded-2xl flex items-center justify-center text-white text-2xl font-bold">
              NA
            </div>
            <div className="flex-1">
              <p className="font-semibold text-lg">Nguyễn Văn A</p>
              <p className="text-sm text-gray-600">user@example.com</p>
            </div>
            <ChevronRight className="w-5 h-5 text-gray-600" />
          </div>
        </div>

        {/* Settings Sections */}
        {settingsSections.map((section) => (
          <div key={section.title} className="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
            <div className="flex items-center gap-2 mb-4">
              <section.icon className="w-5 h-5 text-[#FFB3D9]" />
              <h3 className="font-semibold">{section.title}</h3>
            </div>
            <div className="space-y-3">
              {section.items.map((item, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 bg-gray-200 rounded-xl hover:bg-gray-300 transition-all cursor-pointer"
                >
                  <span className="text-sm">{item.label}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-gray-600">{item.value}</span>
                    <ChevronRight className="w-4 h-4 text-gray-600" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}

        {/* App Info */}
        <div className="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <div className="flex items-center gap-2 mb-4">
            <Info className="w-5 h-5 text-[#FFB3D9]" />
            <h3 className="font-semibold">Thông tin ứng dụng</h3>
          </div>
          <div className="space-y-2 text-sm text-gray-600">
            <div className="flex justify-between">
              <span>Phiên bản</span>
              <span>1.0.0</span>
            </div>
            <div className="flex justify-between">
              <span>Cập nhật lần cuối</span>
              <span>10/02/2025</span>
            </div>
          </div>
        </div>

        {/* Logout Button */}
        <button className="w-full bg-red-50 text-red-600 font-medium py-4 rounded-2xl hover:bg-red-100 transition-all">
          Đăng xuất
        </button>
      </div>
    </div>
  )
}
