from Crypto.PublicKey import RSA

dispositivos = ['umidade', 'luminosidade']

for i in dispositivos:
    key = RSA.generate(2048)
    with open(f'{i}_privada.der', 'wb') as f:
        f.write(key.export_key(format='DER'))
    with open(f'{i}_publica.der', 'wb') as f:
        f.write(key.publickey().export_key(format='DER'))