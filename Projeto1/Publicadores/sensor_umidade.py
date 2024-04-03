import pika, json, random
import datetime
from time import sleep

def dados_sistema_umidade(umidade, data):
    channel.basic_publish(exchange='', routing_key='umidade', body=umidade)
    print(f'Nova Medição {data}:', umidade)

for i in range(20):
    sleep(3)
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