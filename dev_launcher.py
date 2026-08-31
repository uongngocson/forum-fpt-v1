import subprocess, os, sys, time, urllib.request

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_DIR = os.path.join(PROJECT_DIR, "server")
CLIENT_DIR = os.path.join(PROJECT_DIR, "client")

print("=" * 55)
print(" 🦊 CÁO SÁCH - TRÌNH KHỞI ĐỘNG LOCAL DEV TỰ ĐỘNG")
print("=" * 55)

# 1. Dọn dẹp tiến trình cũ
print("\n[1/3] Đang dọn dẹp các tiến trình cổng cũ...")
subprocess.run(
    ["powershell", "-Command", "Get-Process node, python -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -eq '' -and $_.Id -ne $PID } | Stop-Process -Force -ErrorAction SilentlyContinue"],
    capture_output=True
)
time.sleep(1)

# 2. Khởi động Backend (3001)
print("[2/3] Đang khởi động Backend Server (PORT 3001)...")
backend_proc = subprocess.Popen(
    ["node", "--env-file=.env", "dist/main.js"],
    cwd=SERVER_DIR,
    stdout=open(os.path.join(PROJECT_DIR, "server.log"), "w", encoding="utf-8"),
    stderr=subprocess.STDOUT
)

# 3. Khởi động Frontend (5173)
print("[3/3] Đang khởi động Frontend Client (PORT 5173)...")
vite_bin = os.path.join(CLIENT_DIR, "node_modules", ".bin", "vite.cmd")
frontend_proc = subprocess.Popen(
    [vite_bin, "--host", "--port", "5173"],
    cwd=CLIENT_DIR,
    stdout=open(os.path.join(PROJECT_DIR, "client.log"), "w", encoding="utf-8"),
    stderr=subprocess.STDOUT
)

# Đợi Backend sẵn sàng
print("\n⏳ Đang đợi Backend và Frontend kết nối...")
backend_ready = False
for i in range(25):
    time.sleep(1)
    try:
        req = urllib.request.Request("http://127.0.0.1:3001/api/v1/auth/setup-status")
        with urllib.request.urlopen(req, timeout=2) as resp:
            if resp.status == 200:
                backend_ready = True
                break
    except Exception:
        pass

print("\n" + "=" * 55)
if backend_ready:
    print(" 🎉 HỆ THỐNG ĐÃ SẴN SÀNG 100%!")
else:
    print(" ⚠️ Backend đang tải nền, bạn có thể mở web ngay:")
print(" 🌐 Giao diện Web:   http://localhost:5173/")
print(" 🔐 Trang Đăng nhập: http://localhost:5173/login")
print(" 🔑 Tài khoản:       admin / SoninfraAdmin@2026")
print(" 🇻🇳 Ngôn ngữ:        Tiếng Việt (vi) & Đa ngôn ngữ")
print("=" * 55)
print("\n(Nhấn Ctrl + C trong cửa sổ này để tắt toàn bộ hệ thống khi xong)\n")
sys.stdout.flush()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Đang tắt toàn bộ tiến trình Cáo Sách...")
    backend_proc.terminate()
    frontend_proc.terminate()
    print("👋 Đã tắt thành công!")
