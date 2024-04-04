import pika, json, random
import datetime
from time import sleep

def dados_sistema_luminosidade(luminosidade, data):
    channel.basic_publish(exchange='', routing_key='luminosidade', body=luminosidade)
    print(f'Nova Medição {data}:', luminosidade)

for i in range(20):
    sleep(3)
    data = datetime.datetime.now()
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