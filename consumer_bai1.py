from datetime import datetime
import pika


def callback(ch, method, properties, body):
    try:
        message_content = body.decode("utf-8")
        receive_time = datetime.now().strftime("%H:%M:%S")

        print(f"Da nhan message: {message_content}", flush=True)
        print(f"Thoi gian nhan: {receive_time}", flush=True)
        print("-" * 50, flush=True)

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"[!] Loi khi xu ly message: {e}", flush=True)


def run_consumer():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    queue_name = "iot_lab_queue"

    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=False,
    )

    print(
        f"[*] Dang lang nghe tren queue '{queue_name}'. Nhan Ctrl+C de thoat.\n",
        flush=True,
    )
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[!] Dung Consumer.", flush=True)
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    run_consumer()