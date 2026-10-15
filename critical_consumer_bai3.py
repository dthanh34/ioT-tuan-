import pika

def callback(ch, method, properties, body):
    try:
        message = body.decode("utf-8")
        print(f"[critical_queue] Da nhan: {message}", flush=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"[!] Loi: {e}", flush=True)

def run_critical_consumer():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    exchange_name = "iot_alert_exchange"
    queue_name = "critical_queue"
    routing_key = "critical"

    channel.exchange_declare(exchange=exchange_name, exchange_type="direct", durable=True)
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=False,
    )

    print(f"[*] Dang lang nghe muc '{routing_key}' tren '{queue_name}'. Nhan Ctrl+C de thoat.", flush=True)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[!] Dung Critical Consumer.", flush=True)
        channel.stop_consuming()
    finally:
        connection.close()

if __name__ == "__main__":
    run_critical_consumer()