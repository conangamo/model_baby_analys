import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import StartupLoader from "@/components/startup-loader"

const inter = Inter({
  subsets: ["latin", "vietnamese"],
  variable: "--font-sans",
})

export const metadata: Metadata = {
  title: "Neo Cradle",
  description: "Ứng dụng quản lý nôi thông minh cho bé yêu",
    generator: 'v0.app'
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="vi" className={inter.variable}>
      <body className="antialiased">
        <StartupLoader>{children}</StartupLoader>
      </body>
    </html>
  )
}
