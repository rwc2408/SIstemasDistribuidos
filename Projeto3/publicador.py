import Pyro4

@Pyro4.expose
class Publicador:
    def __init__(self, nome):
        self.nome = nome

    def registrar_gravacao(self, uri_lider, dados):
        """O publicador registra uma gravação"""
        lider = Pyro4.Proxy(uri_lider)
        lider.registrar_gravacao(dados)
        print(f"Publicador {self.nome} registrou uma gravação.")
