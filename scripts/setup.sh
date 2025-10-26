#!/bin/bash

# NeoCradle Setup Script
# Hướng dẫn thiết lập tự động cho dự án NeoCradle

echo "🍼 NeoCradle Setup Script"
echo "========================="

# Kiểm tra Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js chưa được cài đặt. Vui lòng cài đặt Node.js 18.0.0 hoặc cao hơn."
    exit 1
fi

# Kiểm tra npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm chưa được cài đặt."
    exit 1
fi

# Kiểm tra MySQL
if ! command -v mysql &> /dev/null; then
    echo "⚠️  MySQL chưa được cài đặt. Vui lòng cài đặt MySQL 8.0 hoặc cao hơn."
    echo "   Xem hướng dẫn trong PRISMA_SETUP.md"
fi

echo "✅ Node.js và npm đã sẵn sàng"

# Cài đặt dependencies
echo "📦 Đang cài đặt dependencies..."
npm install

# Tạo file .env nếu chưa có
if [ ! -f .env ]; then
    echo "⚙️  Tạo file .env..."
    cat > .env << EOF
# Database Configuration
DATABASE_URL="mysql://username:password@localhost:3306/neocradle"

# Next.js Configuration
NEXTAUTH_SECRET="your-secret-key-here"
NEXTAUTH_URL="http://localhost:3000"
EOF
    echo "📝 Đã tạo file .env. Vui lòng cập nhật DATABASE_URL với thông tin database của bạn."
fi

# Generate Prisma client
echo "🔧 Đang generate Prisma client..."
npx prisma generate

# Kiểm tra database connection
echo "🔍 Kiểm tra kết nối database..."
if npx prisma migrate status &> /dev/null; then
    echo "✅ Database đã được thiết lập"
else
    echo "⚠️  Database chưa được thiết lập. Vui lòng:"
    echo "   1. Cập nhật DATABASE_URL trong file .env"
    echo "   2. Chạy: npx prisma migrate dev"
fi

echo ""
echo "🎉 Setup hoàn tất!"
echo ""
echo "📋 Các bước tiếp theo:"
echo "   1. Cập nhật DATABASE_URL trong file .env"
echo "   2. Chạy: npx prisma migrate dev"
echo "   3. Chạy: npm run dev"
echo ""
echo "📖 Xem PRISMA_SETUP.md để có hướng dẫn chi tiết"
