from flask import Flask, Response
from flask_cors import CORS
import json
import sys, os
from threading import Thread
from queue import Queue

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.rabbitmq_utils import consume_events


# Funções específicas para cada tipo de evento
def handle_order_created(ch, method, properties, body):
    handle_event(ch, method, properties, body, "Pedido Criado")
    

def handle_payment_approved(ch, method, properties, body):
    handle_event(ch, method, properties, body, "Pagamento Aprovado")
    

def handle_payment_failed(ch, method, properties, body):
    handle_event(ch, method, properties, body, "Pagamento Recusado")
    

def handle_order_shipped(ch, method, properties, body):
    handle_event(ch, method, properties, body, "Pedido Enviado")
    
def handle_event(ch, method, properties, body, event_name):
    
    event = json.loads(body)
    print(f"{event_name}: {event}")

    formatted_event = {
        "pedido_id": event.get("pedido_id", event.get("pedido_id")),
        "produtos": event.get("produtos", []),
        "total": event.get("total", 0),
        "comprador": event.get("comprador"),
        "status": event.get("status")
    }

    notification_queue.put(json.dumps(formatted_event))

# Fila para transmissão das mensagens
notification_queue = Queue()

def event_stream():
    while True:
        message = notification_queue.get()
        yield f"data: {message}\n\n"
        
        
app = Flask(__name__)
CORS(app) 

@app.route('/notificacoes')
def notificacoes():
    """Rota para conectar o front ao SSE."""
    return Response(event_stream(), content_type='text/event-stream')

# Inicia consumidores de eventos em threads separadas
Thread(target=lambda: consume_events('Pagamentos', 'Pagamentos_Aprovados', handle_payment_approved), daemon=True).start()
Thread(target=lambda: consume_events('Pagamentos', 'Pagamentos_Recusados', handle_payment_failed), daemon=True).start()
Thread(target=lambda: consume_events('Pedidos', 'Pedidos_Enviados', handle_order_shipped), daemon=True).start()
Thread(target=lambda: consume_events('Pedidos', 'Pedidos_Criados', handle_order_created), daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
