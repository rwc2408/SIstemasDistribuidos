import grpc
from concurrent import futures
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "generated")))

import generated.agencia_viagens_pb2 as agencia_viagens_pb2
import generated.agencia_viagens_pb2_grpc as agencia_viagens_pb2_grpc
import generated.companhia_aerea_pb2 as companhia_aerea_pb2
import generated.companhia_aerea_pb2_grpc as companhia_aerea_pb2_grpc
import generated.rede_hoteleira_pb2 as rede_hoteleira_pb2
import generated.rede_hoteleira_pb2_grpc as rede_hoteleira_pb2_grpc
import generated.locadora_carros_pb2 as locadora_carros_pb2
import generated.locadora_carros_pb2_grpc as locadora_carros_pb2_grpc

# Configuração das conexões com os serviços externos
COMPANHIA_AEREA_HOST = "localhost:50051"
REDE_HOTELEIRA_HOST = "localhost:50052"
LOCADORA_CARROS_HOST = "localhost:50053"

class AgenciaViagensService(agencia_viagens_pb2_grpc.AgenciaViagensServicer):
    def ComprarPacote(self, request, context):
        print(f"Recebendo pedido para viagem de {request.origem} para {request.destino}...")

        # Compra passagem aérea
        with grpc.insecure_channel(COMPANHIA_AEREA_HOST) as channel:
            stub = companhia_aerea_pb2_grpc.CompanhiaAereaStub(channel)
            resposta_passagem = stub.ReservarPassagem(companhia_aerea_pb2.ReservaPassagemRequest(
                origem=request.origem,
                destino=request.destino,
                data=request.data_ida,
                numero_pessoas=request.numero_pessoas,
                ida_e_volta=request.data_volta is not None
            ))

        if not resposta_passagem.sucesso:
            return agencia_viagens_pb2.CompraPacoteResponse(
                sucesso=False,
                mensagem="Falha na reserva de passagem: " + resposta_passagem.mensagem
            )

        codigo_passagem = resposta_passagem.codigo_reserva
        print(f"Passagem reservada com sucesso! Código: {codigo_passagem}")

        codigo_hotel = None
        codigo_carro = None

        # Se o cliente quiser hotel, reserva o hotel
        if request.incluir_hotel:
            with grpc.insecure_channel(REDE_HOTELEIRA_HOST) as channel:
                stub = rede_hoteleira_pb2_grpc.RedeHoteleiraStub(channel)
                resposta_hotel = stub.ReservarHotel(rede_hoteleira_pb2.ReservaHotelRequest(
                    destino=request.destino,
                    data_checkin=request.data_ida,
                    data_checkout=request.data_volta if request.data_volta else request.data_ida,
                    numero_pessoas=request.numero_pessoas
                ))

            if not resposta_hotel.sucesso:
                return agencia_viagens_pb2.CompraPacoteResponse(
                    sucesso=False,
                    mensagem="Falha na reserva de hotel: " + resposta_hotel.mensagem
                )

            codigo_hotel = resposta_hotel.codigo_reserva
            print(f"Hotel reservado com sucesso! Código: {codigo_hotel}")

        # Se o cliente quiser carro, reserva o carro
        if request.incluir_carro:
            with grpc.insecure_channel(LOCADORA_CARROS_HOST) as channel:
                stub = locadora_carros_pb2_grpc.LocadoraCarrosStub(channel)
                resposta_carro = stub.ReservarCarro(locadora_carros_pb2.ReservaCarroRequest(
                    destino=request.destino,
                    data_retirada=request.data_ida,
                    data_devolucao=request.data_volta if request.data_volta else request.data_ida,
                    numero_pessoas=request.numero_pessoas
                ))

            if not resposta_carro.sucesso:
                return agencia_viagens_pb2.CompraPacoteResponse(
                    sucesso=False,
                    mensagem="Falha na reserva de carro: " + resposta_carro.mensagem
                )

            codigo_carro = resposta_carro.codigo_reserva
            print(f"Carro reservado com sucesso! Código: {codigo_carro}")

        return agencia_viagens_pb2.CompraPacoteResponse(
            sucesso=True,
            mensagem="Pacote de viagem reservado com sucesso!",
            codigo_reserva_passagem=codigo_passagem,
            codigo_reserva_hotel=codigo_hotel,
            codigo_reserva_carro=codigo_carro
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    agencia_viagens_pb2_grpc.add_AgenciaViagensServicer_to_server(AgenciaViagensService(), server)
    server.add_insecure_port("[::]:50054")
    server.start()
    print("Agência de Viagens aberta")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
