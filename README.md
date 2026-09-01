<div align="center">

# 🦊 Cáo Sách (Sách Cáo)

Nền tảng quản lý thư viện và đọc sách tự lưu trữ (self-hosted) dành cho ebooks, PDF, audiobooks và truyện tranh (comics).

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg?style=flat-square&color=B461B3)](LICENSE)
[![Base Project: BookOrbit](https://img.shields.io/badge/Base_Project-BookOrbit-4169E1?style=flat-square)](https://github.com/bookorbit/bookorbit)

![Tổng quan giao diện Cáo Sách](docs/images/dashboard-overview.png)

</div>

---

## Giới thiệu

**Cáo Sách** là nền tảng quản lý thư viện sách cá nhân và đọc sách trực tuyến tự lưu trữ (self-hosted). Dự án hỗ trợ trải nghiệm đọc linh hoạt trên trình duyệt web, thiết bị Kobo hoặc ứng dụng KOReader, với khả năng đồng bộ tiến độ đọc, ghi chú (highlights) và trạng thái đọc đa chiều.

Bên cạnh đó, hệ thống tích hợp 14 nhà cung cấp metadata, thống kê chỉ số đọc sách, huy hiệu thành tích, giao thức OPDS, tính năng Send-to-Kindle, phân quyền đa người dùng với OIDC/SSO, và tự động đồng bộ với Hardcover, Readwise, StoryGraph.

---

## ✨ Tính năng nổi bật

### Trải nghiệm đọc & Đồng bộ

- **Trình đọc Web tích hợp sẵn**: Hỗ trợ Ebooks (EPUB, KEPUB, MOBI, AZW3, AZW, FB2), PDF, truyện tranh (CBZ, CBR, CB7) và sách nói (M4B, MP3, M4A, OPUS, OGG, FLAC) mà không cần cài đặt thêm plugin ngoài.
- **Đồng bộ 3 chiều (Kobo + KOReader + Web)**: Tiến độ đọc và ghi chú được đồng bộ hai chiều liên tục giữa các thiết bị Kobo, KOReader và trình đọc web.
- **Plugin KOReader**: Trình duyệt danh mục trực tiếp trên thiết bị e-reader, hỗ trợ tìm kiếm, tải sách và quản lý trạng thái, đánh giá.
- **Quản lý ghi chú & Trích dẫn**: Tìm kiếm, lọc ghi chú theo màu sắc và nguồn, xuất dữ liệu dưới dạng Markdown, CSV hoặc JSON.
- **Đồng bộ dịch vụ ngoài**: Tích hợp với Hardcover, The StoryGraph và Readwise.
- **Thống kê & Thành tích**: Bản đồ nhiệt (heatmaps), chuỗi ngày đọc sách liên tục (streaks), mục tiêu năm, thử thách tháng và hơn 50 huy hiệu thành tích.

### Quản lý Thư viện

- **Nhiều thư viện độc lập**: Phân chia thư mục theo từng thư viện, tùy biến quy tắc quét và ưu tiên định dạng.
- **14 nguồn Metadata**: Google Books, Open Library, Amazon, Goodreads, Kobo, Hardcover, Audible, Audnexus, Libro.fm, iTunes, ComicVine, RanobeDB, Aladin và Lubimyczytać.
- **Bộ lọc thông minh (Smart Scopes) & Bộ sưu tập**: Tự động lọc và sắp xếp sách theo các tiêu chí linh hoạt.

### Nền tảng & Hệ thống

- **Đa người dùng & SSO**: Phân quyền chi tiết, bảo vệ dữ liệu đọc riêng tư của từng người dùng, hỗ trợ OIDC (Authentik, Keycloak, Authelia).
- **Giao diện đa ngôn ngữ**: Hỗ trợ đầy đủ tiếng Việt và nhiều ngôn ngữ khác.
- **Phân phối nội dung**: Hỗ trợ OPDS, gửi sách qua Kindle (Send-to-Kindle) và kéo thả tải lên từ trình duyệt.

---

## 🚀 Khởi động nhanh (Docker)

```bash
mkdir caosach && cd caosach
mkdir -p books data/app data/postgres
curl -fsSLo .env https://raw.githubusercontent.com/bookorbit/bookorbit/main/.env.example
curl -fsSLo docker-compose.yml https://raw.githubusercontent.com/bookorbit/bookorbit/main/docker-compose.yml
```

Chỉnh sửa file `.env` và thiết lập các biến môi trường cần thiết:

```dotenv
APP_URL=http://localhost:3000        # URL mở trên trình duyệt
BOOKS_HOST_PATH=./books              # Thư mục chứa sách trên máy chủ

POSTGRES_PASSWORD=                   # Mật khẩu cơ sở dữ liệu (openssl rand -hex 24)
JWT_SECRET=                          # Khóa ký token đăng nhập (openssl rand -hex 32)
SETUP_BOOTSTRAP_TOKEN=               # Token khởi tạo ban đầu (openssl rand -hex 16)
```

Khởi chạy hệ thống:

```bash
docker compose up -d
```

Mở `http://localhost:3000` trên trình duyệt và hoàn tất thiết lập ban đầu với `SETUP_BOOTSTRAP_TOKEN`.

---

## 💻 Hướng dẫn Chạy cho Lập trình viên (Development)

Yêu cầu: **Node.js >= 24**, **pnpm >= 9**, **Docker** (cho PostgreSQL).

1. Khởi động cơ sở dữ liệu:
   ```bash
   docker compose -f docker-compose.dev.yml up -d
   ```
2. Cấu hình môi trường:
   ```bash
   cp server/.env.example server/.env
   ```
3. Cài đặt các thư viện:
   ```bash
   pnpm install
   ```
4. Chạy migration cơ sở dữ liệu:
   ```bash
   cd server && pnpm db:migrate && cd ..
   ```
5. Khởi động môi trường phát triển (Server + Client):
   ```bash
   pnpm dev
   ```

---

## 📱 KOReader Plugin

Plugin hỗ trợ đồng bộ tiến độ đọc, ghi chú hai chiều và duyệt danh mục trực tiếp từ thiết bị đọc sách:

1. Trên giao diện Cáo Sách, truy cập **Cài đặt > KOReader**, tạo thông tin đăng nhập và chọn **Tải Plugin**.
2. Giải nén file `bookorbit.koplugin.zip`.
3. Sao chép thư mục `bookorbit.koplugin` vào đường dẫn `koreader/plugins/` trên thiết bị.
4. Khởi động lại KOReader và mở một cuốn sách bất kỳ.
5. Chọn **Tools > BookOrbit Sync** để kết nối.

---

## 📜 Giấy phép & Bản quyền (License & Credits)

### Ghi nhận Tác giả gốc (Credits & Attribution)

Dự án **Cáo Sách** được phát triển và tùy biến dựa trên nền tảng mã nguồn mở xuất sắc **[BookOrbit](https://github.com/bookorbit/bookorbit)** sáng lập bởi **[neonsolstice](https://github.com/neonsolstice)** cùng cộng đồng các nhà phát triển BookOrbit.

Chúng tôi chân thành cảm ơn và ghi nhận những đóng góp to lớn của tác giả gốc và cộng đồng BookOrbit cho cộng đồng mã nguồn mở.

### Giấy phép (License)

Toàn bộ dự án được phân phối dưới giấy phép **[GNU Affero General Public License v3.0 (AGPL-3.0)](LICENSE)**. Bạn có toàn quyền sử dụng, sửa đổi và phân phối lại theo đúng các điều khoản của giấy phép AGPLv3.
