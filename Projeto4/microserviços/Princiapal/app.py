import json
import os, sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread
import requests
    
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.rabbitmq_utils import publish_event, consume_events, create_rabbit_connection

EXCHANGE_NAME='Pedidos'

pedidos = []

# Callback pagamento aprovado
def handle_payment_approved(ch, method, properties, body):
    event = json.loads(body)
    print(f"Pagamento aprovado para o pedido: {event}")
    atualizar_status_pedido(event['pedido_id'], 'Pagamento Aprovado')
    

# Callback pagamento recusado
def handle_payment_failed(ch, method, properties, body):
    event = json.loads(body)
    print(f"Pagamento recusado para o pedido: {event}")
    atualizar_status_pedido(event['pedido_id'], 'Pagamento Recusado')
    

# Callback pedido enviado
def handle_order_shipped(ch, method, properties, body):
    event = json.loads(body)
    print(f"Pedido enviado: {event}")
    atualizar_status_pedido(event['pedido_id'], 'Enviado')
    

# Atualiza status do pedido
def atualizar_status_pedido(pedido_id, novo_status):
    for pedido in pedidos:
        if pedido['pedido_id'] == pedido_id:
            pedido['status'] = novo_status
            print(f"Status do pedido {pedido['pedido_id']} atualizado para '{novo_status}'")
            break

app = Flask(__name__)
CORS(app) 

# Simulação de carrinho e pedidos
carrinho = []

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = requests.get('http://localhost:5001/estoque').json()
    return jsonify(produtos)

@app.route('/carrinho', methods=['GET'])
def listar_carrinho():
    return jsonify(carrinho)

@app.route('/carrinho', methods=['POST'])
def adicionar_ao_carrinho():
    item = request.get_json()
    
    try:
        response = requests.get(f'http://localhost:5001/estoque/{item["produto_id"]}')
        if response.status_code == 200:
            produto_estoque = response.json()
        else:
            return jsonify({'error': 'Produto não encontrado no estoque'}), 404
    except requests.RequestException as e:
        return jsonify({'error': f'Erro ao consultar estoque: {str(e)}'}), 500

    # Valida a quantidade do produto em estoque
    if item['quantidade'] > produto_estoque['quantidade']:
        return jsonify({
            'error': f"Estoque insuficiente para '{produto_estoque['nome']}'. Disponível: {produto_estoque['quantidade']}"
        }), 400

    # Verifica se o produto já está no carrinho
    carrinho_item = next((i for i in carrinho if i['produto_id'] == item['produto_id']), None)
    if carrinho_item:
        nova_quantidade = carrinho_item['quantidade'] + item['quantidade']

        # Verifica novamente se a nova quantidade ultrapassa o estoque
        if nova_quantidade > produto_estoque['quantidade']:
            return jsonify({
                'error': f"Estoque insuficiente ao atualizar quantidade. Disponível: {produto_estoque['quantidade']}"
            }), 400

        carrinho_item['quantidade'] = nova_quantidade
    else:
        carrinho.append(item)

    return jsonify(item), 201

# Remove produtos do carrinho
@app.route('/carrinho', methods=['DELETE'])
def remover_do_carrinho():
    item = request.get_json()
    carrinho[:] = [i for i in carrinho if i['produto_id'] != item['produto_id']]
    return jsonify({'message': 'Produto removido do carrinho'}), 200

# Esvazia o carrinho
@app.route('/esvaziaCarrinho', methods=['DELETE'])
def limpar_carrinho():
    global carrinho
    carrinho = []
    return jsonify({'message': 'Carrinho esvaziado com sucesso!'}), 200

@app.route('/pedidos', methods=['POST'])
def criar_pedido():
    pedido = request.get_json()
    
    pedido['pedido_id'] = len(pedidos) + 1
    pedido['comprador'] = f"comprador{pedido['pedido_id']}"
    pedido['status'] = 'Criado'

    produtos = json.loads(listar_produtos().data.decode())
    
    # Armazenar os produtos que irão para o pedido final
    pedido_produtos = []

    for item in pedido['produtos']:        
        # Procura o produto nos dados disponíveis
        produto = next((p for p in produtos if p['id'] == item['produto_id']), None)
        
        if produto:
            item['nome'] = produto['nome']
            item['preco'] = produto['preco']
            pedido_produtos.append(item)
    
    pedido['produtos'] = pedido_produtos
    
    pedidos.append(pedido)

    # PUblica no canal Pedidos Criados
    connection, channel = create_rabbit_connection()
    publish_event(channel, EXCHANGE_NAME, "pedidos.criado", pedido)
    
    return jsonify(pedido), 201

@app.route('/pedidos', methods=['GET'])
def listar_pedidos():
    return jsonify(pedidos), 200

@app.route('/pedidos/<int:pedido_id>', methods=['DELETE'])
def excluir_pedido(pedido_id):
    pedido = next((p for p in pedidos if p['pedido_id'] == pedido_id), None)
    if pedido:
        pedidos.remove(pedido)
        # Publica no canal Pedidos Excluídos
        connection, channel = create_rabbit_connection()
        publish_event(channel, EXCHANGE_NAME, 'Pedidos_Excluidos', pedido)
        return jsonify({'message': 'Pedido excluído'}), 200
    return jsonify({'error': 'Pedido não encontrado'}), 404

Thread(target=lambda: consume_events('Pagamentos', 'Pagamentos_Aprovados', handle_payment_approved), daemon=True).start()
Thread(target=lambda: consume_events('Pagamentos', 'Pagamentos_Recusados', handle_payment_failed), daemon=True).start()
Thread(target=lambda: consume_events('Pedidos', 'Pedidos_Enviados', handle_order_shipped), daemon=True).start()

if __name__ == '__main__':
    
    # Inicia a API Flask
    app.run(debug=True, Threaded=True)
    
    


