import pika
import json
import os
from database import SessionLocal
from logs.logger import setup_logger
from mq.db_function import create_order, update_order, delete_order, create_user, update_user, delete_user

logger = setup_logger()

def receive_user_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("MQ_HOST", "localhost")))
    channel = connection.channel()

    channel.exchange_declare(exchange="users.sync", exchange_type="fanout")
    channel.queue_declare(queue="api_products_users", durable=True)
    channel.queue_bind(exchange="users.sync", queue="api_products_users")

    def callback(ch, method, properties, body):
        try:
            data = json.loads(body)
            action = data.get("action")
            user_id = data.get("user_id")
            user_data = data.get("data")

            db = SessionLocal()

            if action == "create":
                logger.debug(f"[x] Reçu création utilisateur : {data}")
                create_user(db, user_data)

            elif action == "update":
                logger.debug(f"[x] Reçu mise à jour utilisateur : {data}")
                update_user(db, user_id, user_data)

            elif action == "delete":
                logger.debug(f"[x] Reçu suppression utilisateur : {data}")
                delete_user(db, user_id)

            else:
                logger.debug(f"[!] Action inconnue : {action}")

        except json.JSONDecodeError:
            logger.debug("[!] Impossible de parser le message JSON")
        except Exception as e:
            logger.debug(f"[!] Erreur : {e}")
        finally:
            db.close()

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue="api_products_users", on_message_callback=callback)

    try:
        logger.debug("[*] En attente de messages utilisateurs... Ctrl+C pour arrêter.")
        channel.start_consuming()
    except KeyboardInterrupt:
        logger.info("Arrêt du consumer.")
        channel.stop_consuming()
        connection.close()

def receive_order_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("MQ_HOST", "localhost")))
    channel = connection.channel()

    channel.exchange_declare(exchange="orders.sync", exchange_type="fanout")
    channel.queue_declare(queue="api_products_customers", durable=True)
    channel.queue_bind(exchange="orders.sync", queue="api_products_customers")

    def callback(ch, method, properties, body):
        try:
            data = json.loads(body)
            action = data.get("action")
            order_id = data.get("order_id")
            order_data = data.get("data")

            db = SessionLocal()
            if action == "create":
                logger.debug(f"[x] Reçu création commande : {data}")
                create_order(db, order_id, order_data)

            elif action == "update":
                logger.debug(f"[x] Reçu mise à jour commande : {data}")
                update_order(db, order_id, order_data)

            elif action == "delete":
                logger.debug(f"[x] Reçu suppression commande : {data}")
                delete_order(db, order_id)

            else:
                logger.debug(f"[!] Action inconnue : {action}")

        except json.JSONDecodeError:
            logger.debug("[!] Impossible de parser le message JSON")
        except Exception as e:
            logger.debug(f"[!] Erreur : {e}")
        finally:
            db.close()

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue="api_products_customers", on_message_callback=callback)

    try:
        logger.debug("[*] En attente de messages... Ctrl+C pour arrêter.")
        channel.start_consuming()
    except KeyboardInterrupt:
        logger.info("Arrêt du consumer.")
        channel.stop_consuming()
        connection.close()