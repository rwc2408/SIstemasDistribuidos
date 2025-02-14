import pika, json, random
import datetime
from time import sleep
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Carrega a chave privada em formato DER
with open('../Autenticacao/luminosidade_privada.der', 'rb') as f:
    private_key = RSA.import_key(f.read())

def dados_sistema_luminosidade(luminosidade, data):
    message = f"{luminosidade}:{data}".encode(encoding='utf-8')  # Mensagem com umidade e data
    h = SHA256.new(message)  # Hash da mensagem
    signature = pkcs1_15.new(private_key).sign(h) # Assina o hash
    
    channel.basic_publish(exchange='', routing_key='luminosidade', body= message + b'  -' + signature)    
    
    print(f'Nova Medição {data}:', luminosidade)

for i in range(20):
    sleep(5)
    data = str(datetime.datetime.now())
    # Estabelece conexão com o broker 
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Gera valor aleatório de luminosidade
    nivel_luminosidade = random.randint(1000, 8000)

    # Declara a fila do sensor de luminosidade
    channel.queue_declare(queue='luminosidade')

    # O sensor de luminosidade publica as informações na fila de luminosidade
    dados_sistema_luminosidade(str(nivel_luminosidade), data)

    connection.close()