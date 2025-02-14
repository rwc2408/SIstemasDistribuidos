import Pyro4

@Pyro4.expose
class Lider:
    def __init__(self, nome, uri):
        self.nome = nome
        self.uri = uri
        self.topico = "Tópico inicial"
        self.particao = {}  # Dados da partição
        self.log = []  # Log de gravações
        self.ultima_epoca = 0  # Controla a época das gravações
        self.quorum = 2  # Número mínimo de confirmações para marcar a gravação como comprometida
        self.votantes = []  # Lista de votantes registrados

    def registrar_broker(self, broker, estado):
        """Registrar um broker (votante, observador)"""
        self.votantes.append({"broker": broker, "estado": estado})
        print(f"Broker {broker.nome} registrado como {estado}!")

    def registrar_gravacao(self, dados):
        """O líder recebe uma gravação e adiciona ao seu log"""
        self.ultima_epoca += 1  # Nova época
        log_entry = {"epoca": self.ultima_epoca, "dados": dados}
        self.log.append(log_entry)
        print(f"Líder registrou uma gravação na época {self.ultima_epoca}")
        
        # Notificar os votantes para buscar os dados
        self.notificar_votantes()

    def notificar_votantes(self):
        """Notifica todos os votantes sobre a nova gravação"""
        for votante_info in self.votantes:
            if votante_info["estado"] == "Votante":
                votante_info["broker"].buscar_dados(self.uri, self.ultima_epoca, len(self.log) - 1)

    def buscar_dados(self, epoca_busca, offset_busca):
        """Processa uma solicitação de busca de dados"""
        if epoca_busca < self.ultima_epoca:
            # Verificar se o offset de busca é consistente
            if offset_busca < len(self.log):
                dados = self.log[offset_busca]
                return dados
            else:
                # Erro: offset inconsistente
                return {"erro": "offset inconsistente", "epoca": self.ultima_epoca, "offset_final": len(self.log) - 1}
        else:
            # A época solicitada não é válida
            return {"erro": "época inconsistente", "epoca": self.ultima_epoca, "offset_final": len(self.log) - 1}

    def confirmar_gravacao(self, epoca, offset):
        """Registrar a confirmação da gravação por parte dos votantes"""
        if len(self.votantes) >= self.quorum:
            print(f"A gravação na época {epoca} foi comprometida!")
            return True  # Comprometida
        return False

 