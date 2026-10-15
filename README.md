# BÀI THỰC HÀNH — LẬP TRÌNH PYTHON VỚI GIAO THỨC AMQP

## 1. Thông tin sinh viên

| STT | Họ tên | MSSV |
|---|---|---|
| 1 | Trương Đình Hoàng Vũ | B23DCCN949 |
| 2 | Dương Đức Thành | B23DCCN767 |
| 3 | Vũ Minh Quang | B23DCCN697 |

| Thông tin | Nội dung |
|---|---|
| Môn | IoT |
| Buổi thực hành | Buổi 2 — Python với AMQP (RabbitMQ) |

## 2. Môi trường
- Ngôn ngữ: Python 3.x
- Thư viện yêu cầu: `pika`
- Lệnh cài đặt:
  ```bash
  pip install pika
3. AMQP Broker sử dụng
Broker: localhost (hoặc RabbitMQ Server dùng chung)

Port: 5672

Giao thức: AMQP (RabbitMQ)

## 4. Cấu trúc thư mục
```text
BaiThucHanh2/
├── producer_bai1.py           # Bài 1 — Producer cơ bản
├── consumer_bai1.py           # Bài 1 — Consumer cơ bản
├── sensor_producer_bai2.py    # Bài 2 — Sensor producer (JSON)
├── monitor_consumer_bai2.py   # Bài 2 — Monitoring consumer (Kiểm tra ngưỡng)
├── alert_producer_bai3.py     # Bài 3 — Alert producer (Direct Exchange)
├── warning_consumer_bai3.py   # Bài 3 — Warning consumer (Routing key: warning)
├── critical_consumer_bai3.py  # Bài 3 — Critical consumer (Routing key: critical)
└── README.md
```

## 5. Cách chạy từng chương trình
Bài 1 — Gửi và nhận message cơ bản qua queue
Queue sử dụng: iot_lab_queue

Bước 1 (Terminal 1 — Chạy trước): Khởi chạy Consumer để lắng nghe queue:

```bash
python consumer_bai1.py
```

Bước 2 (Terminal 2): Khởi chạy Producer để gửi thông điệp:

```bash
python producer_bai1.py
```

Bài 2 — Mô phỏng cảm biến IoT gửi dữ liệu môi trường 
Queue sử dụng: sensor_data_queue

Bước 1 (Terminal 1 — Chạy trước): Khởi chạy Monitoring Consumer:

```bash
python monitor_consumer_bai2.py
```

Bước 2 (Terminal 2): Khởi chạy Sensor Producer để bắn dữ liệu định kỳ mỗi 3 giây:

```bash
python sensor_producer_bai2.py
```

Bài 3 — Mô phỏng hệ thống điều phối cảnh báo IoT với Exchange
Exchange sử dụng: iot_alert_exchange (Loại: direct)

Bước 1 (Terminal 1 — Chạy trước): Khởi chạy Consumer để lắng nghe queue:

```bash
python consumer_bai1.py
```

Bước 2 (Terminal 2): Khởi chạy Critical Consumer:

```bash
python critical_consumer_bai3.py
```

Bước 3 (Terminal 3): Khởi chạy Alert Producer để phát các thông điệp:

```bash
python alert_producer_bai3.py
```

## 6. Kết quả đạt được

### Bài 1

Producer:
```text
[x] Da gui message: Xin chao tu ung dung Python AMQP - B23DCCN767 - Duong Duc Thanh
Consumer:

Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN767 - Duong Duc Thanh
Thoi gian nhan: 14:05:21
```

### Bài 2
Sensor Producer:
```text
[x] Da gui: {"device_id": "sensor01", "temperature": 36.4, "humidity": 38.9}
Monitoring Consumer:

Device: sensor01
Temperature: 36.4
Humidity: 38.9
CANH BAO: Nhiet do cao
CANH BAO: Do am thap
------------------------------
```

### Bài 3
Alert Producer:
``` text
[x] Da gui [info]: He thong cam bien hoat dong binh thuong info
[x] Da gui [warning]: Nhiet do phong may vuot nguong warning
[x] Da gui [critical]: Cam bien kho lanh mat ket noi critical
Warning Consumer:

[warning_queue] Da nhan: Nhiet do phong may vuot nguong warning
Critical Consumer:

[critical_queue] Da nhan: Cam bien kho lanh mat ket noi critical
```

## 7. Ghi chú
Đảm bảo RabbitMQ Server đã được khởi động trước khi chạy các chương trình Python.

Thứ tự chạy khuyến cáo: Khởi chạy các Consumer trước, sau đó mới chạy Producer để đảm bảo Queue / Exchange đã được khai báo và bind sẵn sàng.