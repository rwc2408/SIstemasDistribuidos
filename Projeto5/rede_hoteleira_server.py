import grpc
from concurrent import futures
import sys,os, uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "generated")))

import generated.rede_hoteleira_pb2 as rede_hoteleira_pb2
import generated.rede_hoteleira_pb2_grpc as rede_hoteleira_pb2_grpc

class RedeHoteleiraService(rede_hoteleira_pb2_grpc.RedeHoteleiraServicer):
    def ReservarHotel(self, request, context):
        print(f"Reservando hotel em {request.destino}...")
        codigo_reserva = str(uuid.uuid4())[:8] 
        return rede_hoteleira_pb2.ReservaHotelResponse(
            sucesso=True,
            mensagem="Hotel reservado com sucesso!",
            codigo_reserva=f"HOTEL-{codigo_reserva}"
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rede_hoteleira_pb2_grpc.add_RedeHoteleiraServicer_to_server(RedeHoteleiraService(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    print("Rede Hoteleira aberta")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
