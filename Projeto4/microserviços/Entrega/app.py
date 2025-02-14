import json
from flask import Flask
import os, sys
from flask_cors import CORS
from threading import Thread
from time import sleep

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.rabbitmq_utils import publish_event, consume_events, create_rabbit_connection

EXCHANGE_NAME='Pedidos'

def handle_payment_approved(ch, method, properties, body):
    event = json.loads(body)
    
    print(f"Pedido {event['pedido_id']} em separação...")
    
    sleep(3)
    
    print(f"Emitindo {event['pedido_id']}  nota fiscal...")

    sleep(3)

    conection, channel = create_rabbit_connection()
    publish_event(channel, EXCHANGE_NAME, 'Pedidos_Enviados', {'pedido_id': event['pedido_id'], 'status': 'Enviado'})

    print(f"Pedido {event['pedido_id']} enviado.")

app = Flask(__name__)
CORS(app)

Thread(target=lambda: consume_events('Pagamentos', 'Pagamentos_Aprovados', handle_payment_approved), daemon=True).start()

if __name__ == '__main__':

    # Inicia a API Flask
    app.run(debug=True)
