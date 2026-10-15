import pika
import json
from datetime import datetime

def callback(ch, method, properties, body):
    try:
        data = json.loads(body.decode("utf-8"))
        
        device_id = data.get("device_id")
        temperature = data.get("temperature")
        humidity = data.get("humidity")
        current_time = datetime.now().strftime("%H:%M:%S")
        
        print(f"Device: {device_id}", flush=True)
        print(f"Temperature: {temperature}", flush=True)
        print(f"Humidity: {humidity}", flush=True)
        
        if temperature > 35:
            print("CANH BAO: Nhiet do cao", flush=True)
        if humidity < 40:
            print("CANH BAO: Do am thap", flush=True)
            
        print(f"Thoi gian: {current_time}", flush=True)
        print("-" * 30, flush=True)
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"[!] Loi xu ly du lieu sensor: {e}", flush=True)

def run_monitor():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    queue_name = "sensor_data_queue"
    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=False,
    )

    print(f"[*] Dang giam sat du lieu tu '{queue_name}'. Nhan Ctrl+C de thoat.\n", flush=True)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[!] Da dung chuong trinh giam sat.", flush=True)
        channel.stop_consuming()
    finally:
        connection.close()

if __name__ == "__main__":
    run_monitor()