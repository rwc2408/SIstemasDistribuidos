import sys, os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.rabbitmq_utils import publish_event, create_rabbit_connection

EXCHANGE_NAME='Pagamentos'

app = Flask(__name__)
CORS(app)

@app.route('/pagamento/<int:pedido_id>', methods=['POST'])
def iniciar_pagamento(pedido_id):
    try:
        # Recebe dados do pedido
        dados_pedido = request.get_json()
        if not dados_pedido:
            return jsonify({'error': 'Dados do pedido não fornecidos'}), 400

        # Faz requisição para validar o pagamento
        response = requests.post("http://localhost:5010/solicitacaoPagamento", json=dados_pedido)

        if response.status_code == 200:
            return jsonify({'mensagem': 'Pagamento enviado para processamento'}), 200
        return jsonify({'error': 'Erro ao comunicar com o sistema de pagamento'}), response.status_code

    except Exception as e:
        print(f"Erro ao iniciar pagamento: {e}")
        return jsonify({'error': f'Erro inesperado ao processar o pagamento: {str(e)}'}), 500
    
@app.route('/respostaPagamento', methods=['POST'])
def webhook_pagamento():
    """Recebe notificações do sistema externo e publica eventos no RabbitMQ."""
    try:
        data = request.get_json()
        if not data or 'pedido_id' not in data or 'status' not in data:
            return jsonify({'error': 'Dados inválidos recebidos'}), 400

        pedido_id = data['pedido_id']
        status = data['status']

        # Cria conexão com RabbitMQ
        connection, channel = create_rabbit_connection()

        if status == 'Pagamento Aprovado':
            publish_event(channel, EXCHANGE_NAME, 'Pagamentos_Aprovados', data)
            print(f"Pagamento aprovado para pedido {pedido_id}. Publicado no RabbitMQ.")
        elif status == 'Pagamento Recusado':
            publish_event(channel, EXCHANGE_NAME, 'Pagamentos_Recusados', data)
            print(f"Pagamento recusado para pedido {pedido_id}. Publicado no RabbitMQ.")
        else:
            return jsonify({'error': 'Status de pagamento desconhecido'}), 400

        return jsonify({'mensagem': 'Notificação de pagamento processada com sucesso'}), 200

    except Exception as e:
        print(f"Erro ao processar notificação de pagamento: {e}")
        return jsonify({'error': 'Erro interno ao processar a notificação'}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
