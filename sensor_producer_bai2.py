import pika
import json
import random
import time

def run_sensor_producer():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        channel = connection.channel()

        queue_name = "sensor_data_queue"
        channel.queue_declare(queue=queue_name, durable=True)

        print("[*] Bat dau mo phong cam bien IoT (gui moi 3 giay). Nhan Ctrl+C de dung.\n", flush=True)
        
        while True:
            payload = {
                "device_id": "sensor01",
                "temperature": round(random.uniform(25.0, 40.0), 1),
                "humidity": round(random.uniform(30.0, 80.0), 1)
            }
            
            message_json = json.dumps(payload)
            
            channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=message_json.encode("utf-8"),
                properties=pika.BasicProperties(
                    delivery_mode=pika.DeliveryMode.Persistent
                )
            )
            print(f"[x] Da gui: {message_json}", flush=True)
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\n[!] Dung mo phong cam bien.", flush=True)
    except Exception as e:
        print(f"[!] Loi xay ra: {e}", flush=True)
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()

if __name__ == "__main__":
    run_sensor_producer()