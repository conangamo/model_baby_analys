# Neo Cradle

Ứng dụng quản lý nôi thông minh cho bé yêu - Một ứng dụng web hiện đại được xây dựng với Next.js, TypeScript và Tailwind CSS.

## 🚀 Tính năng

- Dashboard quản lý thông tin nôi thông minh
- Theo dõi nhiệt độ cơ thể bé
- Phân tích tiếng khóc
- Giám sát môi trường xung quanh
- Theo dõi chuyển động
- Phát nhạc rock cho bé
- Giao diện hiện đại với dark/light mode
- Responsive design

## 🛠️ Công nghệ sử dụng

- **Framework**: Next.js 14.2.16
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui + Radix UI
- **Icons**: Lucide React
- **Charts**: Recharts
- **Font**: Inter (hỗ trợ tiếng Việt)
- **Package Manager**: npm

## 📋 Yêu cầu hệ thống

- Node.js 18.0.0 hoặc cao hơn
- npm
- Git

## 🚀 Cách chạy ứng dụng

### 1. Clone repository

```bash
git clone <repository-url>
cd NeoCradle
```

### 2. Cài đặt dependencies

```bash
npm install
```

### 3. Chạy ứng dụng ở chế độ development

```bash
npm run dev
```

Ứng dụng sẽ chạy tại: [http://localhost:3000](http://localhost:3000)

### 4. Build ứng dụng cho production

```bash
npm run build
```

### 5. Chạy ứng dụng production

```bash
npm start
```

## 📁 Cấu trúc thư mục

```
NeoCradle/
├── app/                    # Next.js App Router
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   ├── loading.tsx        # Loading component
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # shadcn/ui components
│   ├── details/          # Detail pages components
│   ├── dashboard.tsx     # Dashboard component
│   ├── home-page.tsx     # Home page component
│   └── ...               # Other components
├── hooks/                # Custom React hooks
├── lib/                  # Utility functions
├── public/               # Static assets
├── styles/               # Additional styles
└── ...                   # Config files
```

## 🎨 UI Components

Ứng dụng sử dụng shadcn/ui với các component sau:
- Accordion, Alert, Avatar, Badge
- Button, Card, Dialog, Dropdown
- Form, Input, Label, Select
- Table, Tabs, Toast, Tooltip
- Và nhiều component khác...

## 🌙 Theme

Ứng dụng hỗ trợ dark/light mode với next-themes.

## 📱 Responsive Design

Ứng dụng được thiết kế responsive, hoạt động tốt trên:
- Desktop
- Tablet
- Mobile

## 🔧 Scripts có sẵn

- `npm run dev` - Chạy development server
- `npm run build` - Build ứng dụng cho production
- `npm start` - Chạy production server
- `npm run lint` - Chạy ESLint

## 🐛 Troubleshooting

### Lỗi thường gặp:

1. **Port 3000 đã được sử dụng**:
   ```bash
   npm run dev -- --port 3001
   ```

2. **Lỗi dependencies**:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **Lỗi TypeScript**:
   - Kiểm tra file `tsconfig.json`
   - Đảm bảo tất cả dependencies đã được cài đặt

## 📄 License

Dự án này được phát triển cho mục đích học tập và nghiên cứu.

## 👨‍💻 Tác giả

Neo Cradle Team

---

**Lưu ý**: Đây là ứng dụng demo, không sử dụng cho mục đích thương mại mà không có sự cho phép.
