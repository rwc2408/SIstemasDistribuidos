import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='umidade')

    # A umidade é medida em porcentagem, a quantidade ideal fica entre 50-70%
    def callback_umidade(ch, method, properties, body):
        body = int(body)
        if body < 50:
            print('Umidade muito baixa, ligue o conta gotas')
        elif body > 70:
            print('Umiadade muito alta, desligue o conta gotas')
        else:
            print('Umidade ideal')

    # O sistema de irrigação consome as informações da fila de umidade, e faz o ajuste no contagotas caso necessário
    channel.basic_consume(queue='umidade', on_message_callback=callback_umidade, auto_ack=True)

    print('Aguardando mensagens do sensor de umidade')
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