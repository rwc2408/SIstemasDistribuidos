import pika, sys, os
from time import sleep
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Carrega a chave pública em formato DER
with open('../Autenticacao/umidade_publica.der', 'rb') as f:
    public_key = RSA.import_key(f.read())

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='umidade')

    # A umidade é medida em porcentagem, a quantidade ideal fica entre 50-70%
    def callback_umidade(ch, method, properties, body):
        message, signature = body.rsplit(b'  -', 1) # Divide a mensagem e a assinatura
        
        umidade, data = message.decode(encoding='utf-8', errors='ignore').split(' ') # Extrai umidade e data

        umidade = umidade.split(':')[0]
        
        umidade = int(umidade)
        
        # Verificação da assinatura
        h = SHA256.new(message)  # Hash da mensagem
        try:
            pkcs1_15.new(public_key).verify(h, signature)
            print(f'Umidade: {umidade}, Data: {data}')
        except (ValueError, TypeError):
            print("A assinatura é inválida.")

        if umidade < 50:
            print('Umidade muito baixa, ligue o conta gotas')
        elif umidade > 70:
            print('Umiadade muito alta, desligue o conta gotas')
        else:
            print('Umidade ideal')

    # O sistema de irrigação consome as informações da fila de umidade, e faz o ajuste no contagotas caso necessário
    channel.basic_consume(queue='umidade', on_message_callback=callback_umidade)

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