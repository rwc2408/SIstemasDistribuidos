import Pyro4

@Pyro4.expose
class Observador:
    def __init__(self, nome):
        self.nome = nome

    def atualizar(self, novo_topico):
        """Método chamado quando o líder notifica uma mudança de tópico"""
        print(f"Observador {self.nome} foi notificado sobre o novo tópico: {novo_topico}")

@Pyro4.expose
class Votante:
    def __init__(self, nome):
        self.nome = nome
        self.log_local = []  # Log local do votante
        self.epoca_local = 0  # A última época que o votante tem confirmada

    def buscar_dados(self, uri_lider, epoca_busca, offset_busca):
        """Votante envia requisição de busca ao líder"""
        lider = Pyro4.Proxy(uri_lider)
        resposta = lider.buscar_dados(epoca_busca, offset_busca)
        
        if "erro" in resposta:
            print(f"Votante {self.nome} encontrou erro: {resposta['erro']}")
            # Truncar o log local até o offset final
            self.log_local = self.log_local[:resposta["offset_final"] + 1]
            # Repetir a busca com a nova época e offset
            self.buscar_dados(uri_lider, resposta["epoca"], resposta["offset_final"] + 1)
        else:
            # Adicionar os dados recebidos ao log local
            self.log_local.append(resposta)
            print(f"Votante {self.nome} recebeu dados: {resposta}")
            # Confirmar a gravação
            lider.confirmar_gravacao(resposta["epoca"], len(self.log_local) - 1)


