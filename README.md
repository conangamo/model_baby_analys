# 🍼 NeoCradle

**Ứng dụng giám sát nôi thông minh cho bé yêu** - Một hệ thống IoT hiện đại được xây dựng với Next.js, TypeScript và Tailwind CSS để theo dõi và chăm sóc em bé một cách thông minh.

## ✨ Tính năng chính

### 📊 Dashboard thông minh
- **Theo dõi nhiệt độ cơ thể** - Giám sát nhiệt độ bé 24/7 với cảnh báo tự động
- **Phân tích tiếng khóc** - AI phân tích âm thanh để hiểu nhu cầu của bé
- **Giám sát môi trường** - Theo dõi nhiệt độ, độ ẩm, ánh sáng xung quanh
- **Theo dõi chuyển động** - Phát hiện cử động và giấc ngủ của bé
- **Nhạc ru ngủ** - Phát nhạc rock nhẹ nhàng để dỗ bé ngủ

### 🎨 Giao diện người dùng
- **Mobile-first design** - Tối ưu cho điện thoại với max-width 448px
- **Gradient backgrounds** - Màu pastel nhẹ nhàng (Pink, Blue, Mint, Purple)
- **Rounded corners** - Thiết kế mềm mại, thân thiện
- **Real-time notifications** - Thông báo tức thì khi có bất thường
- **Dark/Light mode** - Chuyển đổi giao diện theo sở thích

## 🛠️ Công nghệ sử dụng

### Frontend
- **Framework**: Next.js 14.2.16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4.x
- **UI Components**: shadcn/ui + Radix UI
- **Icons**: Lucide React
- **Charts**: Recharts
- **State Management**: React Hooks

### Backend & Database
- **Database**: MySQL
- **ORM**: Prisma 6.18.0
- **API**: Next.js API Routes
- **Authentication**: (Sẽ được thêm trong tương lai)

### Development Tools
- **Package Manager**: npm
- **Linting**: ESLint
- **Type Checking**: TypeScript
- **AI Development**: ai-devkit

## 📋 Yêu cầu hệ thống

- **Node.js**: 18.0.0 hoặc cao hơn
- **npm**: 9.0.0 hoặc cao hơn
- **MySQL**: 8.0 hoặc cao hơn
- **Git**: Để clone repository

## 🚀 Cài đặt và chạy ứng dụng

### 1. Clone repository

```bash
git clone <repository-url>
cd NeoCradle
```

### 2. Cài đặt dependencies

```bash
npm install
```

### 3. Cấu hình Database

#### Tạo file `.env`:
```bash
cp .env.example .env
```

#### Cấu hình DATABASE_URL trong `.env`:
```env
DATABASE_URL="mysql://username:password@localhost:3306/neocradle"
```

#### Chạy Prisma migrations:
```bash
npx prisma migrate dev
```

#### Generate Prisma client:
```bash
npx prisma generate
```

### 4. Chạy ứng dụng development

```bash
npm run dev
```

Ứng dụng sẽ chạy tại: [http://localhost:3000](http://localhost:3000)

### 5. Build cho production

```bash
npm run build
npm start
```

## 📁 Cấu trúc thư mục

```
NeoCradle/
├── app/                    # Next.js App Router
│   ├── api/               # API Routes
│   │   └── user/          # User API endpoints
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   ├── loading.tsx        # Loading component
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # shadcn/ui components
│   ├── details/          # Detail pages components
│   │   ├── body-temp-detail.tsx
│   │   ├── cry-analysis-detail.tsx
│   │   ├── environment-detail.tsx
│   │   ├── motion-detail.tsx
│   │   └── rock-music-detail.tsx
│   ├── dashboard.tsx     # Main dashboard
│   ├── home-page.tsx     # Home page
│   ├── settings-page.tsx # Settings page
│   └── ...               # Other components
├── docs/                 # AI Development documentation
│   └── ai/              # ai-devkit phase docs
├── hooks/                # Custom React hooks
├── lib/                  # Utility functions & Prisma client
├── prisma/               # Database schema & migrations
│   ├── schema.prisma     # Database schema
│   └── migrations/       # Database migrations
├── public/               # Static assets
└── ...                   # Config files
```

## 🔌 API Endpoints

### User Management
- `GET /api/user` - Lấy thông tin user hiện tại

### (Sẽ được thêm trong tương lai)
- `POST /api/sensors/temperature` - Gửi dữ liệu nhiệt độ
- `POST /api/sensors/cry` - Gửi dữ liệu tiếng khóc
- `GET /api/analytics/daily` - Lấy báo cáo hàng ngày

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

1. **Prisma Client không khởi tạo được**:
   ```bash
   npx prisma generate
   npx prisma migrate dev
   ```

2. **Lỗi Node.js modules trong browser**:
   - Đảm bảo Prisma chỉ được sử dụng trong server components
   - Kiểm tra `next.config.mjs` có webpack fallbacks

3. **Database connection failed**:
   - Kiểm tra `DATABASE_URL` trong `.env`
   - Đảm bảo MySQL server đang chạy
   - Chạy `npx prisma db push` để sync schema

4. **Port 3000 đã được sử dụng**:
   ```bash
   npm run dev -- --port 3001
   ```

5. **Lỗi dependencies**:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

## 🚀 Development

### AI Development với ai-devkit
Dự án sử dụng ai-devkit để quản lý phát triển có cấu trúc:
- `docs/ai/requirements/` - Phân tích yêu cầu
- `docs/ai/design/` - Thiết kế hệ thống
- `docs/ai/planning/` - Lập kế hoạch dự án
- `docs/ai/implementation/` - Hướng dẫn triển khai
- `docs/ai/testing/` - Chiến lược testing

### Database Management
```bash
# Xem database trong Prisma Studio
npx prisma studio

# Reset database
npx prisma migrate reset

# Deploy migrations
npx prisma migrate deploy
```

## 📱 Screenshots

*(Sẽ được thêm sau khi hoàn thiện UI)*

## 🗺️ Roadmap

### Phase 1: Core Features ✅
- [x] Basic dashboard
- [x] User management
- [x] Database setup
- [x] Mobile-responsive UI

### Phase 2: IoT Integration (Coming Soon)
- [ ] Real-time sensor data
- [ ] Temperature monitoring
- [ ] Cry analysis
- [ ] Environment monitoring

### Phase 3: Advanced Features
- [ ] AI-powered insights
- [ ] Push notifications
- [ ] Data analytics
- [ ] Multi-user support

## 📄 License

Dự án này được phát triển cho mục đích học tập và nghiên cứu.

## 👨‍💻 Contributors

**NeoCradle Team** - Phát triển hệ thống giám sát nôi thông minh

---

**⚠️ Lưu ý**: Đây là ứng dụng demo, không sử dụng cho mục đích thương mại mà không có sự cho phép. Để sử dụng trong môi trường production, cần thêm authentication, security và testing đầy đủ.
