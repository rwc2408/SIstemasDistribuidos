# Projeto 1

## Arquitetura Orientada a Evetos para Controle de Umidade e Iluminação

## Descrição:

- O objetivo do sistema é fazer a comunicação entre os sensores de umidade e iluminação com os sistemas de irrigação e iluminação respectivamente. 
- Para isso será utilizada uma arquitetura orientada a eventos, onde os sensores farão o papel de Publishers e os sistemas o papel de consumidores.
- Os sensores publicam infromações sobre o estado atual da planta, cada um em sua fila, iluminação ou irrigação.
- Os sistemas consomem informações das filas que os interessa e executa uma ação.
- Além disso, existe um sistema de display, que consome as informações das duas filas e disponibiliza na tela. 

## Para rodar a aplicação:

- Iniciar os três consumidores em terminais diferentes utilizando os comandos:
    - python3 irrigacao.py
    - python3 iluminacao.py
    - python3 display.py

- Iniciar os sensores ao mesmo tempo utilizando os comandos:
    - python3 sensor_luminosidade.py & python3 sensor_umidade.py