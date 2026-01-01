import uvicorn
from server import create_app

# Tạo ứng dụng FastAPI bằng cách gọi hàm đã định nghĩa
app = create_app()

if __name__ == "__main__":
    # Đây là điểm bắt đầu khi bạn chạy file: python main.py
    # uvicorn sẽ dùng đối tượng 'app' để chạy server
    print("🚀 Khởi chạy server tại http://localhost:8000")
    print(" Mở trình duyệt và truy cập http://localhost:8000/docs để xem API.")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)