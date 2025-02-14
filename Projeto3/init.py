import Pyro4
from Lider import Lider
from Votantes_Observadore import Votante, Observador
from publicador import Publicador

   # Registrar o Líder
def registrar_lider():
    lider_nome = "Lider_Epoca1"
    lider_uri = "tcp://localhost:9090"
    
    lider = Lider(lider_nome, lider_uri)
    daemon = Pyro4.Daemon()
    uri = daemon.register(lider)
    
    # Registra o líder no serviço de nomes
    nameserver = Pyro4.locateNS()
    nameserver.register(lider_nome, uri)
    
    print(f"Líder {lider_nome} registrado com URI: {uri}")
    
    daemon.requestLoop()

# Registrar o Votante
def registrar_votante():
    nameserver = Pyro4.locateNS()
    uri_lider = nameserver.lookup("Lider_Epoca1")
    
    votante = Votante("Votante1")
    lider = Pyro4.Proxy(uri_lider)
    lider.registrar_broker(votante, "Votante")
    
    votante.buscar_dados(uri_lider, 0, 0)

# Registrar o Publicador
def registrar_publicador():
    nameserver = Pyro4.locateNS()
    uri_lider = nameserver.lookup("Lider_Epoca1")
    
    publicador = Publicador("Publicador1")
    publicador.registrar_gravacao(uri_lider, {"chave": "valor"})

# Registrar o Consumidor
def registrar_consumidor():
    nameserver = Pyro4.locateNS()
    uri_lider = nameserver.lookup("Lider_Epoca1")
    
    consumidor = Consumidor("Consumidor1")
    consumidor.consumir_dados(uri_lider)


# Registrar o Observador
def registrar_observador():
    nameserver = Pyro4.locateNS()
    uri_lider = nameserver.lookup("Lider_Epoca1")
    
    observador = Observador("Observador1")
    lider = Pyro4.Proxy(uri_lider)
    lider.registrar_broker(observador, "Observador")

if __name__ == "__main__":
    # Inicializar o Líder
    registrar_lider()
    
    # Inicializar os outros brokers e interações
    registrar_votante()
    registrar_publicador()
    registrar_consumidor()
    registrar_observador()
