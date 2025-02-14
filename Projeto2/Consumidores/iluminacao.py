import pika, sys, os
from time import sleep
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Carrega a chave pública em formato DER
with open('../Autenticacao/luminosidade_publica.der', 'rb') as f:
    public_key = RSA.import_key(f.read())

def main():
    # Estabelece conexão com o broker   
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='luminosidade')
    # A luminosidade é medida em lumens, a quantidade mínima para o crescimento são 2.000 lumens por pé quadrado, a média são 5.000 e o ideal fica entre 7.000-7.500
    def callback_luminosidade(ch, method, properties, body):
        message, signature = body.rsplit(b'  -', 1) # Divide a mensagem e a assinatura
        
        luminosidade, data = message.decode(encoding='utf-8', errors='ignore').split(' ') # Extrai umidade e data
        
        luminosidade = luminosidade.split(':')[0]
        
        luminosidade = int(luminosidade)
             
        # Verificação da assinatura
        h = SHA256.new(message)  # Hash da mensagem
        try:
            pkcs1_15.new(public_key).verify(h, signature)
            print(f'Iluminacao: {luminosidade}, Data: {data}')
        except (ValueError, TypeError):
            print("A assinatura é inválida.")
        
        
        if luminosidade < 5000:
            print('Luminosidade muito baixa, necessário ajuste')
        elif luminosidade > 7500:
            print('Luminosidade muito alta, necessário ajuste')
        else:
            print('Luminosidade ideal')

    # O sistema de iluminação consome as informações da fila de iluminação, e faz o ajuste na iluminação caso necessário
    channel.basic_consume(queue='luminosidade', on_message_callback=callback_luminosidade)

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