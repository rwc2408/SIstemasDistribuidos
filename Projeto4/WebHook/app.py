from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/solicitacaoPagamento', methods=['POST'])
def webhook_pagamento():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não informados'}), 400
        
        print(f"Solicitação de pagamento recebida")

        response = requests.post("http://localhost:5010/validaPagamento", json=data)

        if response.status_code == 200:
            return jsonify({'mensagem': 'Pagamento em avaliação'}), 200
        else:
            return jsonify({'error': 'Erro ao comunicar com o sistema de pagamento'}), response.status_code

    except Exception as e:
        print(f"Erro ao se comunicar: {e}")
        return jsonify({'error': 'Erro ao se comunicar'}), 500


@app.route('/validaPagamento', methods=['POST'])
def valida_pagamento():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados inválidos'}), 400

        print(f"Validando pagamento..")

        data.update({'status': 'Pagamento Aprovado'})

        response = requests.post("http://localhost:5002/respostaPagamento", json=data)

        if response.status_code == 200:
            return jsonify({'mensagem': 'Pagamento avaliado com sucesso'}), 200
        else:
            return jsonify({'error': 'Erro ao retornar resposta de pagamento'}), response.status_code

    except Exception as e:
        print(f"Erro ao processar o pagamento: {e}")
        return jsonify({'error': 'Erro ao processar pagamento'}), 500

if __name__ == '__main__':
    app.run(port=5010, debug=True)
