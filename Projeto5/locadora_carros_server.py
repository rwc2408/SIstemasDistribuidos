import grpc
from concurrent import futures
import sys,os, uuid
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "generated")))

import generated.locadora_carros_pb2 as locadora_carros_pb2
import generated.locadora_carros_pb2_grpc as locadora_carros_pb2_grpc

class LocadoraCarrosService(locadora_carros_pb2_grpc.LocadoraCarrosServicer):
    def ReservarCarro(self, request, context):
        print(f"Reservando carro em {request.destino}...")
        codigo_reserva = str(uuid.uuid4())[:8] 
        return locadora_carros_pb2.ReservaCarroResponse(
            sucesso=True,
            mensagem="Carro reservado com sucesso!",
            codigo_reserva=f"CARRO-{codigo_reserva}"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    locadora_carros_pb2_grpc.add_LocadoraCarrosServicer_to_server(LocadoraCarrosService(), server)
    server.add_insecure_port("[::]:50053")
    server.start()
    print("Locadora de Carros aberta")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
