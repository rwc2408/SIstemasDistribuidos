import json
from flask import Flask, jsonify, request
from threading import Thread
import sys, os
from flask_cors import CORS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.rabbitmq_utils import consume_events

# Banco de dados simulado para produtos e estoque
estoque = [
    {'id': 1, 'nome': 'Melão', 'preco': 5.99, 'quantidade': 50},
    {'id': 2, 'nome': 'Banana', 'preco': 4.50, 'quantidade': 30},
    {'id': 3, 'nome': 'Maçã', 'preco': 7.90, 'quantidade': 20},
    {'id': 4, 'nome': 'Mamão', 'preco': 6.50, 'quantidade': 30},
    {'id': 5, 'nome': 'Abacate', 'preco': 3.90, 'quantidade': 40},
    {'id': 6, 'nome': 'Maracujá', 'preco': 9.00, 'quantidade': 60}
]


app = Flask(__name__)

# Callback para pedido criado
def handle_pedido_criado(ch, method, properties, body):
    pedido = json.loads(body)
    print(f"Evento recebido: Pedido Criado - {pedido}")
    reduzir_estoque(pedido)

# Callback para pedido excluído
def handle_pedido_excluido(ch, method, properties, body):
    pedido = json.loads(body)
    print(f"Evento recebido: Pedido Excluído - {pedido}")
    restaurar_estoque(pedido)

def reduzir_estoque(pedido):
    for item in pedido['produtos']:
        print(pedido['produtos'])
        produto = next((p for p in estoque if p['id'] == item['produto_id']), None)
        if produto:
            if produto['quantidade'] >= item['quantidade']:
                produto['quantidade'] -= item['quantidade']
                print(f"Estoque reduzido {produto['nome']} agora tem {produto['quantidade']} unidades.")
            else:
                print(f"Erro: Estoque insuficiente para o produto {produto['nome']}.")

def restaurar_estoque(pedido):
    for item in pedido['produtos']:# Altere de 'itens' para 'produtos'
        produto = next((p for p in estoque if p['id'] == item['produto_id']), None)
        if produto:
            produto['quantidade'] += item['quantidade']

@app.route('/estoque', methods=['GET'])
def listar_estoque():
    return jsonify(estoque), 200

# Endpoint para consultar um único produto pelo ID
@app.route('/estoque/<int:produto_id>', methods=['GET'])
def consultar_produto(produto_id):
    produto = next((p for p in estoque if p['id'] == produto_id), None)
    if produto:
        return jsonify(produto), 200
    return jsonify({'error': 'Produto não encontrado'}), 404

Thread(target=lambda: consume_events('Pedidos', 'Pedidos_Criados', handle_pedido_criado), daemon=True).start()
Thread(target=lambda: consume_events('Pedidos', 'Pedidos_Excluídos', handle_pedido_excluido), daemon=True).start()

if __name__ == '__main__':
    
    # Inicia o servidor Flask
    app.run(debug=True)
