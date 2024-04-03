import pika, sys, os

def main():
    # Estabelece conexão com o broker
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    def callback_luminosidade(ch, method, properties, body):
        luminosidade = int(body)
        print('Luminosidade:', luminosidade)
        
    def callback_umidade(ch, method, properties, body):
        umidade = int(body)
        print(f'Umidade: {umidade}%')

    # Consome os dados dos dois sensores e exibe as informações no display
    channel.basic_consume(queue='iluminacao', on_message_callback=callback_luminosidade, auto_ack=True)
    channel.basic_consume(queue='umidade', on_message_callback=callback_umidade, auto_ack=True)

    print('Aguardando informações do sistema')
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