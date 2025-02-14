import pika, sys, os
from time import sleep
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Carrega a chave pública
with open('../Autenticacao/luminosidade_publica.der', 'rb') as f:
    public_key_iluminacao = RSA.import_key(f.read())
    
# Carrega a chave pública
with open('../Autenticacao/umidade_publica.der', 'rb') as f:
    public_key_irrigacao = RSA.import_key(f.read())

def main():
    # Estabelece conexão com o broker
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    def callback_luminosidade(ch, method, properties, body):
        message, signature = body.rsplit(b'  -', 1) # Divide a mensagem e a assinatura
        
        luminosidade, data = message.decode(encoding='utf-8', errors='ignore').split(' ') # Extrai umidade e data
        
        luminosidade = luminosidade.split(':')[0]
        
        luminosidade = int(luminosidade)
             
        # Verificação da assinatura
        h = SHA256.new(message)  # Hash da mensagem
        try:
            pkcs1_15.new(public_key_iluminacao).verify(h, signature)
            print(f'Iluminacao: {luminosidade}, Data: {data}')
        except (ValueError, TypeError):
            print("A assinatura é inválida.")
        
    def callback_umidade(ch, method, properties, body):
        
        message, signature = body.rsplit(b'  -', 1) # Divide a mensagem e a assinatura
        
        umidade, data = message.decode(encoding='utf-8', errors='ignore').split(' ') # Extrai umidade e data

        umidade = umidade.split(':')[0]
        
        umidade = int(umidade)
        
        # Verificação da assinatura
        h = SHA256.new(message)  # Hash da mensagem
        try:
            pkcs1_15.new(public_key_irrigacao).verify(h, signature)
            print(f'Umidade: {umidade}, Data: {data}')
        except (ValueError, TypeError):
            print("A assinatura é inválida.")

    # Consome os dados dos dois sensores e exibe as informações no display
    channel.basic_consume(queue='luminosidade', on_message_callback=callback_luminosidade)
    channel.basic_consume(queue='umidade', on_message_callback=callback_umidade)

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