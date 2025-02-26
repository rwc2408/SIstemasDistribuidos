import grpc
from concurrent import futures
import sys, os, uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "generated")))

import generated.companhia_aerea_pb2 as companhia_aerea_pb2
import generated.companhia_aerea_pb2_grpc as companhia_aerea_pb2_grpc

class CompanhiaAereaService(companhia_aerea_pb2_grpc.CompanhiaAereaServicer):
    def ReservarPassagem(self, request, context):
        print(f"Reservando passagem para {request.destino}...")
        codigo_reserva = str(uuid.uuid4())[:8]
        return companhia_aerea_pb2.ReservaPassagemResponse(
            sucesso=True,
            mensagem="Passagem reservada com sucesso!",
            codigo_reserva=f"AEREO-{codigo_reserva}"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    companhia_aerea_pb2_grpc.add_CompanhiaAereaServicer_to_server(CompanhiaAereaService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Companhia Aérea aberta")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
