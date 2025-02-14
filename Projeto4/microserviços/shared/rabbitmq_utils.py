import pika
import json


def create_rabbit_connection():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        
        return connection, channel
    except Exception as e:
        print(f"Erro ao conectar ao RabbitMQ: {e}")
        return None, None


def declare_exchange(channel, exchange_name):
    try:
        channel.exchange_declare(exchange=exchange_name, exchange_type='topic', durable=True)
    except Exception as e:
        print(f"Erro ao declarar o exchange {exchange_name}: {e}")


def publish_event(channel, exchange_name, routing_key, event):
    try:
        message = json.dumps(event)
        
        declare_exchange(channel, exchange_name)

        # Habilitar confirmações do publisher
        channel.confirm_delivery()
        
        channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2 
            )
        )
        print(f"[x] Evento publicado no exchange '{exchange_name}' com routing key '{routing_key}': {event}")
    except Exception as e:
        print(f"Erro ao publicar o evento no exchange {exchange_name}: {e}")


def consume_events(exchange_name, binding_key, callback):
    connection, channel = create_rabbit_connection()
    if not channel:
        print("Erro: Não foi possível criar o canal para consumo de eventos.")
        return

    try:
        declare_exchange(channel, exchange_name)

        # Criar uma fila temporária para receber as mensagens do tópico
        result = channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue

        # Associar a fila ao exchange com a routing key
        channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=binding_key)

        print(f"[*] Aguardando eventos do exchange '{exchange_name}' com binding '{binding_key}'...")

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Consumo interrompido pelo usuário.")
    finally:
        close_rabbit_connection(connection)


def close_rabbit_connection(connection):
    try:
        if connection:
            connection.close()
            print("Conexão com o RabbitMQ encerrada.")
    except Exception as e:
        print(f"Erro ao fechar a conexão com o RabbitMQ: {e}")