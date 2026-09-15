# Uông Bí GO — MVP Đặt món Canteen

Hệ thống đặt món ăn trưa tại căn tin theo mô hình 3 tầng (3-Tier Architecture):
- **Presentation Layer**: FastAPI routers (`backend/app/routers`) + Frontend HTML/CSS/JS thuần (`frontend/`)
- **Business/Service Layer**: `backend/app/services`
- **Data Access Layer**: `backend/app/repositories` + SQLAlchemy ORM models (`backend/app/models`) + SQLite

Đầy đủ 4 Sprint: Auth & RBAC, Menu, Cart/Order/QR Payment, KDS, Admin Dashboard, Seed data.

## 1. Yêu cầu môi trường

- Python 3.10+ (khuyến nghị 3.11)
- Không cần cài đặt Database server riêng — dự án dùng **SQLite** (1 file `uongbigo.db` tự sinh)

## 2. Cài đặt & khởi tạo Database

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Database (SQLite) sẽ **tự động được tạo** khi chạy server lần đầu (không cần lệnh migrate riêng).

## 3. Chèn dữ liệu mẫu (Seed Data) — khuyến nghị chạy trước khi demo

```bash
# vẫn đứng trong thư mục backend/, đã kích hoạt venv
python seed.py
```

Script sẽ xóa sạch và tạo lại toàn bộ dữ liệu, gồm:
- 3 tài khoản demo:
  | Vai trò | Email | Mật khẩu |
  |---|---|---|
  | Quản lý (Admin) | admin@uongbigo.vn | Admin@123 |
  | Nhân viên bếp (Staff/KDS) | staff@uongbigo.vn | Staff@123 |
  | Sinh viên (Buyer) | buyer@uongbigo.vn | Buyer@123 |
- 10 món ăn (đa dạng trạng thái Còn hàng/Hết hàng) + 1 món đã xóa mềm (demo Soft Delete)
- 5 đơn hàng lịch sử (3 Hoàn thành, 1 Đã hủy, 1 Chờ thanh toán) để Dashboard có số liệu hiển thị

## 4. Chạy Backend (API + phục vụ luôn Frontend tĩnh)

```bash
# vẫn trong thư mục backend/
uvicorn app.main:app --reload --port 8000
```

Mở trình duyệt tại: **http://localhost:8000**

- Trang đăng nhập: `http://localhost:8000/index.html`
- Swagger API docs: `http://localhost:8000/api/docs`

> Backend đã cấu hình phục vụ luôn thư mục `frontend/` (Static Files) nên **không cần chạy Frontend riêng** — chỉ cần 1 lệnh `uvicorn` ở trên là đủ để chạy toàn bộ web.

### Chạy Frontend độc lập (tùy chọn)

Nếu muốn chạy Frontend trên 1 cổng khác (ví dụ để dùng Live Server), có thể mở trực tiếp
`frontend/index.html` bằng bất kỳ static server nào (VD `python -m http.server 5500` trong
thư mục `frontend/`), miễn là Backend (`http://localhost:8000`) đang chạy vì Frontend gọi API
qua đường dẫn tương đối `/api/...`. Khi đó cần cập nhật `API_BASE` trong `frontend/js/api.js`
thành địa chỉ đầy đủ của backend (VD `http://localhost:8000/api`) và bật CORS (đã mở `*` sẵn).

## 5. Cấu trúc thư mục

```
uongbigo/
├── backend/
│   ├── app/
│   │   ├── main.py                 # Entry point, wiring router + static files + background job
│   │   ├── core/                   # config, database, security (JWT/hash)
│   │   ├── models/                 # ORM models (Data Access Layer) - theo Class Diagram
│   │   ├── schemas/                # Pydantic request/response (Presentation Layer)
│   │   ├── repositories/           # Truy vấn DB thuần (Data Access Layer)
│   │   ├── services/               # Logic nghiệp vụ (Business Layer)
│   │   ├── routers/                # API endpoints (Presentation Layer)
│   │   └── jobs/                   # Cronjob nền: timeout thanh toán (TC35)
│   ├── seed.py                     # Script chèn dữ liệu mẫu
│   └── requirements.txt
├── frontend/
│   ├── index.html / register.html  # Đăng nhập / Đăng ký
│   ├── menu.html                   # Thực đơn (Buyer)
│   ├── cart.html                   # Giỏ hàng + Thanh toán QR (mock)
│   ├── orders.html                 # Theo dõi đơn hàng (Buyer)
│   ├── kds.html                    # Kitchen Display System (Staff)
│   ├── admin/                      # Dashboard / Quản lý Menu / Quản lý Đơn hàng (Admin)
│   ├── css/style.css
│   └── js/ (api.js, cart.js)
└── README.md
```

## 6. Tài khoản & phân quyền (RBAC)

| Role | Sau đăng nhập chuyển hướng tới |
|---|---|
| `ROLE_BUYER` | `/menu.html` |
| `ROLE_STAFF` | `/kds.html` |
| `ROLE_ADMIN` | `/admin/dashboard.html` |

Toàn bộ API `/api/admin/*` bắt buộc `ROLE_ADMIN`, API `/api/kds/*` bắt buộc `ROLE_STAFF` hoặc
`ROLE_ADMIN` — tài khoản sai vai trò gọi vào sẽ nhận **HTTP 403 Forbidden** (TC60).

## 7. Quy ước lập trình (Coding Conventions) đã áp dụng

- Tên lớp (Class): `PascalCase` (VD: `NguoiDung`, `MonAn`, `DonHang`)
- Tên biến/hàm: `camelCase` (VD: `hoTen`, `donGia`, `taoDonHang`, `getCurrentUser`)
- Tên hằng số: `UPPER_SNAKE_CASE` (VD: `ROLE_ADMIN`, `TrangThaiDonHang.CHO_THANH_TOAN`)

## 8. Nghiệp vụ trọng tâm đã cài đặt

- **Xác thực & RBAC** (Sprint 1): đăng ký/đăng nhập JWT, mật khẩu băm (pbkdf2_sha256), quên mật khẩu,
  chống trùng email, điều hướng theo Role.
- **Thực đơn**: `GET /api/menu` hiển thị đúng trạng thái Còn/Hết hàng, món Hết hàng bị làm mờ và
  chặn chọn ở giao diện.
- **Giỏ hàng & Tạo đơn** (Sprint 2): validate lại tồn kho trước khi tạo đơn (TC14), validate khung
  giờ nhận nằm trong 07:00–18:00 (TC24/TC25), tính `tongTien` chính xác.
- **QR Payment mock**: sinh QR (ảnh SVG mock) đúng số tiền đơn hàng, cronjob nền quét mỗi 15s tự
  động hủy đơn quá hạn thanh toán (mặc định 5 phút — có thể chỉnh ở `core/config.py`), chống thanh
  toán trùng (TC37), sinh mã đơn rút gọn kiểu `#001`.
- **KDS**: Order State Machine tuần tự bắt buộc `Đã thanh toán → Đang chuẩn bị → Sẵn sàng nhận →
  Hoàn thành` (TC41–TC45), Quick Action bật/tắt Còn/Hết hàng ngay tại màn hình bếp (US16). Frontend
  tự động polling (5s) + tự làm mới khi có mạng trở lại (đáp ứng Risk #5: không crash khi mất mạng,
  tự đồng bộ khi có mạng lại).
- **Admin Dashboard** (Sprint 4): CRUD món ăn với **Soft Delete** (không xóa cứng khỏi DB để không
  ảnh hưởng lịch sử đơn hàng cũ), lịch sử đơn hàng, thống kê doanh thu **chỉ tính đơn "Hoàn thành"**
  (TC59), toàn bộ route yêu cầu `ROLE_ADMIN` (TC60).

## 9. Giới hạn & giả định của bản Demo (đọc trước khi chấm/báo cáo)

Vì đây là bản MVP phục vụ demo/học tập, một số phần được **giả lập (mock)** thay vì tích hợp dịch
vụ thật, cần lưu ý khi trình bày:

- **Thanh toán QR**: không kết nối cổng thanh toán thật (VietQR/Momo). Ảnh QR là SVG mock sinh từ
  hash nội dung giao dịch; xác nhận thanh toán qua nút "Giả lập thanh toán thành công/thất bại" ở
  giao diện Giỏ hàng, gọi tới endpoint `POST /api/thanhtoan/webhook` — endpoint này đóng vai trò
  webhook thật sự sẽ được cổng thanh toán gọi vào trong môi trường production.
- **Quên mật khẩu**: chưa tích hợp gửi email thật. API trả thẳng "mật khẩu tạm thời" trong response
  (chỉ dùng để test luồng) — môi trường production **bắt buộc** phải gửi qua email và không được
  trả trực tiếp trong API.
- **Đồng bộ realtime (Risk #5)**: thay vì WebSocket, KDS/Trang theo dõi đơn dùng cơ chế polling
  (gọi lại API mỗi 5 giây) + tự làm mới ngay khi trình duyệt phát hiện có mạng trở lại
  (`window.addEventListener("online", ...)`). Cách này đơn giản, ổn định cho MVP và vẫn đảm bảo
  không mất đơn khi mất mạng tạm thời.
- **Timeout thanh toán**: mặc định 5 phút kể từ lúc sinh QR (`PAYMENT_TIMEOUT_MINUTES` trong
  `backend/app/core/config.py`), cronjob quét mỗi 15 giây (`PAYMENT_TIMEOUT_CHECK_INTERVAL_SECONDS`).
  Có thể chỉnh 2 giá trị này để demo nhanh hơn khi thuyết trình.
- **JWT secret key**: giá trị mặc định trong `core/config.py` chỉ dùng cho demo/local, **phải đổi**
  bằng biến môi trường `JWT_SECRET_KEY` trước khi triển khai thật.

## 10. Kiểm thử nhanh qua Swagger

Có thể test toàn bộ API không cần Frontend tại `http://localhost:8000/api/docs`:
1. Gọi `POST /api/auth/login` với tài khoản demo → copy `accessToken`.
2. Bấm nút "Authorize" (góc trên bên phải Swagger UI), dán token theo định dạng `Bearer <token>`.
3. Gọi các endpoint còn lại theo Role tương ứng.
