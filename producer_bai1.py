import pika

def run_producer():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        channel = connection.channel()

        queue_name = "iot_lab_queue"
        channel.queue_declare(queue=queue_name, durable=True)

        message = "Xin chao tu ung dung Python AMQP - B23DCCN767 - Duong Duc Thanh"

        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=message.encode("utf-8"),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent  # Đảm bảo message bền vững
            )
        )
        print(f"[x] Da gui message: {message}", flush=True)

    except Exception as e:
        print(f"[!] Loi khi gui message: {e}", flush=True)
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()

if __name__ == "__main__":
    run_producer()