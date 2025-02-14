import pika, json, random
import datetime
from time import sleep
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Carrega a chave privada em formato DER
with open('../Autenticacao/umidade_privada.der', 'rb') as f:
    private_key = RSA.import_key(f.read())

def dados_sistema_umidade(umidade, data):
    message = f"{umidade}:{data}".encode(encoding='utf-8')  # Mensagem com umidade e data
    h = SHA256.new(message)  # Hash da mensagem
    signature = pkcs1_15.new(private_key).sign(h)
    
    channel.basic_publish(exchange='', routing_key='umidade', body=message + b'  -' + signature   )
    print(f'Nova Medição {data}:', umidade)

for i in range(20):
    sleep(5)
    data = datetime.datetime.now()
    # Estabelece conexão com o broker
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Gera valor aleatório de umidade
    nivel_umidade = random.randint(0, 100)

    # Declara a fila do sensor de umidade
    channel.queue_declare(queue='umidade')

    # Publica as informações do sensor de umidade na fila de umidade
    dados_sistema_umidade(str(nivel_umidade), data)

    connection.close()