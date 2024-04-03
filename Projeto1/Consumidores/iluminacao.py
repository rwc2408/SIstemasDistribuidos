import pika, sys, os
from time import sleep

def main():
    # Estabelece conexão com o broker   
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='iluminacao')
    # A luminosidade é medida em lumens, a quantidade mínima para o crescimento são 2.000 lumens por pé quadrado, a média são 5.000 e o ideal fica entre 7.000-7.500
    def callback_luminosidade(ch, method, properties, body):
        body = int(body)
        if body < 5000:
            print('Luminosidade muito baixa, necessário ajuste')
        elif body > 7500:
            print('Luminosidade muito alta, necessário ajuste')
        else:
            print('Luminosidade ideal')

    # O sistema de iluminação consome as informações da fila de iluminação, e faz o ajuste na iluminação caso necessário
    channel.basic_consume(queue='iluminacao', on_message_callback=callback_luminosidade, auto_ack=True)

    print('Aguardando mensagens do sensor de luminosidade')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)