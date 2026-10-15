import pika

def run_alert_producer():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        channel = connection.channel()

        exchange_name = "iot_alert_exchange"
        channel.exchange_declare(exchange=exchange_name, exchange_type="direct", durable=True)

        alerts = [
            ("info", "He thong cam bien hoat dong binh thuong info"),
            ("warning", "Nhiet do phong may vuot nguong warning"),
            ("critical", "Cam bien kho lanh mat ket noi critical")
        ]

        for routing_key, message in alerts:
            channel.basic_publish(
                exchange=exchange_name,
                routing_key=routing_key,
                body=message.encode("utf-8"),
                properties=pika.BasicProperties(
                    delivery_mode=pika.DeliveryMode.Persistent
                )
            )
            print(f"[x] Da gui [{routing_key}]: {message}", flush=True)

    except Exception as e:
        print(f"[!] Loi khi gui alert: {e}", flush=True)
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()

if __name__ == "__main__":
    run_alert_producer()