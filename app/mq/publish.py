import pika
import json
import os
from logs.logger import setup_logger

logger = setup_logger()

def publish_product_create(data: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv("MQ_HOST", "localhost")))
    channel = connection.channel()

    channel.exchange_declare(exchange='products.sync', exchange_type='fanout')

    message = json.dumps({
        "action": "create",
        "data": data
    })

    channel.basic_publish(exchange='products.sync', routing_key='', body=message)
    logger.debug(f" [x] Mise à jour envoyée : {message}")
    connection.close()

def publish_product_update(product_id: int, data: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv("MQ_HOST", "localhost")))
    channel = connection.channel()

    channel.exchange_declare(exchange='products.sync', exchange_type='fanout')

    message = json.dumps({
        "action": "update",
        "product_id": product_id,
        "data": data
    })

    channel.basic_publish(exchange='products.sync', routing_key='', body=message)
    logger.debug(f" [x] Mise à jour envoyée : {message}")
    connection.close()


def publish_product_delete(product_id: int):
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv("MQ_HOST", "localhost")))
    channel = connection.channel()

    channel.exchange_declare(exchange='products.sync', exchange_type='fanout')

    message = json.dumps({
        "action": "delete",
        "product_id": product_id,
        "data": {}
    })

    channel.basic_publish(exchange='products.sync', routing_key='', body=message)
    logger.debug(f" [x] Suppression envoyée : {message}")
    connection.close()