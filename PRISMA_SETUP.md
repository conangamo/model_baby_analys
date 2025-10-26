# 🗄️ Hướng dẫn thiết lập Prisma cho NeoCradle

Hướng dẫn chi tiết về cách thiết lập database và Prisma khi clone dự án NeoCradle về máy.

## 📋 Yêu cầu trước khi bắt đầu

- **Node.js**: 18.0.0 hoặc cao hơn
- **npm**: 9.0.0 hoặc cao hơn  
- **MySQL**: 8.0 hoặc cao hơn
- **Git**: Để clone repository

## 🚀 Bước 1: Clone và cài đặt dependencies

```bash
# Clone repository
git clone <repository-url>
cd NeoCradle

# Cài đặt dependencies
npm install
```

## 🗄️ Bước 2: Thiết lập Database

### 2.1. Cài đặt MySQL

#### Trên Windows:
```bash
# Sử dụng Chocolatey
choco install mysql

# Hoặc tải từ: https://dev.mysql.com/downloads/mysql/
```

#### Trên macOS:
```bash
# Sử dụng Homebrew
brew install mysql
brew services start mysql
```

#### Trên Ubuntu/Debian:
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

### 2.2. Tạo database

```bash
# Kết nối MySQL
mysql -u root -p

# Tạo database
CREATE DATABASE neocradle;

# Tạo user (tùy chọn)
CREATE USER 'neocradle_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON neocradle.* TO 'neocradle_user'@'localhost';
FLUSH PRIVILEGES;

# Thoát MySQL
EXIT;
```

## ⚙️ Bước 3: Cấu hình Environment Variables

### 3.1. Tạo file `.env`

```bash
# Tạo file .env từ template
cp .env.example .env
```

### 3.2. Cấu hình DATABASE_URL

Mở file `.env` và thêm:

```env
# Database
DATABASE_URL="mysql://username:password@localhost:3306/neocradle"

# Ví dụ:
# DATABASE_URL="mysql://root:password@localhost:3306/neocradle"
# DATABASE_URL="mysql://neocradle_user:your_password@localhost:3306/neocradle"
```

**Lưu ý**: Thay `username`, `password` bằng thông tin MySQL của bạn.

## 🔧 Bước 4: Thiết lập Prisma

### 4.1. Generate Prisma Client

```bash
npx prisma generate
```

Lệnh này sẽ:
- Tạo Prisma Client trong `lib/generated/prisma/`
- Sử dụng cấu hình custom output từ `prisma.config.ts`

### 4.2. Chạy Database Migrations

```bash
npx prisma migrate dev
```

Lệnh này sẽ:
- Áp dụng tất cả migrations trong `prisma/migrations/`
- Tạo bảng `users` với cấu trúc đã định nghĩa
- Tạo migration mới nếu có thay đổi schema

### 4.3. (Tùy chọn) Seed database với dữ liệu mẫu

```bash
# Nếu có file seed
npx prisma db seed
```

## ✅ Bước 5: Kiểm tra thiết lập

### 5.1. Kiểm tra Prisma Studio

```bash
npx prisma studio
```

Mở trình duyệt tại `http://localhost:5555` để xem database.

### 5.2. Test API endpoint

```bash
# Chạy development server
npm run dev

# Test API trong terminal khác
curl http://localhost:3000/api/user
```

## 🐛 Troubleshooting

### Lỗi: "Prisma Client did not initialize yet"

```bash
# Giải pháp:
npx prisma generate
npx prisma migrate dev
```

### Lỗi: "Database connection failed"

1. **Kiểm tra MySQL đang chạy**:
   ```bash
   # Windows
   net start mysql
   
   # macOS/Linux
   sudo systemctl start mysql
   # hoặc
   brew services start mysql
   ```

2. **Kiểm tra DATABASE_URL**:
   ```bash
   # Test connection
   mysql -u username -p -h localhost -P 3306 neocradle
   ```

3. **Reset database**:
   ```bash
   npx prisma migrate reset
   ```

### Lỗi: "Module not found: @prisma/client"

```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
npx prisma generate
```

### Lỗi: "Migration failed"

```bash
# Xem trạng thái migrations
npx prisma migrate status

# Reset và chạy lại
npx prisma migrate reset
npx prisma migrate dev
```

## 📊 Cấu trúc Database hiện tại

### Bảng `users`
```sql
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255) UNIQUE NOT NULL,
  createdAt DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 Workflow Development

### Khi thay đổi schema:

1. **Sửa file `prisma/schema.prisma`**
2. **Tạo migration**:
   ```bash
   npx prisma migrate dev --name describe_your_change
   ```
3. **Generate client**:
   ```bash
   npx prisma generate
   ```

### Khi thêm dữ liệu mẫu:

```bash
# Sử dụng Prisma Studio
npx prisma studio

# Hoặc tạo seed script trong package.json
```

## 📝 Lệnh hữu ích

```bash
# Xem trạng thái database
npx prisma migrate status

# Reset database (xóa tất cả dữ liệu)
npx prisma migrate reset

# Deploy migrations (production)
npx prisma migrate deploy

# Format schema file
npx prisma format

# Validate schema
npx prisma validate

# Xem database trong browser
npx prisma studio
```

## 🎯 Kết quả mong đợi

Sau khi hoàn thành tất cả các bước:

- ✅ Database `neocradle` được tạo
- ✅ Bảng `users` được tạo với dữ liệu mẫu
- ✅ Prisma Client được generate trong `lib/generated/prisma/`
- ✅ API endpoint `/api/user` hoạt động
- ✅ Ứng dụng chạy không lỗi tại `http://localhost:3000`

## 📞 Hỗ trợ

Nếu gặp vấn đề, hãy kiểm tra:
1. MySQL server đang chạy
2. DATABASE_URL đúng format
3. User có quyền truy cập database
4. Port 3306 không bị block

---

**Lưu ý**: Hướng dẫn này dành cho môi trường development. Đối với production, cần thêm security và backup strategies.
