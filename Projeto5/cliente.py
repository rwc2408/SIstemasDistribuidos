import grpc
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "generated")))

import generated.agencia_viagens_pb2 as agencia_viagens_pb2
import generated.agencia_viagens_pb2_grpc as agencia_viagens_pb2_grpc

AGENCIA_VIAGENS_HOST = "localhost:50054"

def solicitar_pacote():
    with grpc.insecure_channel(AGENCIA_VIAGENS_HOST) as channel:
        stub = agencia_viagens_pb2_grpc.AgenciaViagensStub(channel)

        print("\n===== Solicitação de Pacote de Viagem =====")
        origem = input("Origem: ")
        destino = input("Destino: ")
        data_ida = input("Data de Ida (YYYY-MM-DD): ")
        data_volta = input("Data de Volta (YYYY-MM-DD) [deixe em branco se for só ida]: ")
        numero_pessoas = int(input("Número de pessoas: "))
        incluir_hotel = input("Incluir hotel? (s/n): ").strip().lower() == "s"
        incluir_carro = input("Incluir carro? (s/n): ").strip().lower() == "s"

        request = agencia_viagens_pb2.CompraPacoteRequest(
            origem=origem,
            destino=destino,
            data_ida=data_ida,
            data_volta=data_volta if data_volta else None,
            numero_pessoas=numero_pessoas,
            incluir_hotel=incluir_hotel,
            incluir_carro=incluir_carro
        )

        resposta = stub.ComprarPacote(request)

        if resposta.sucesso:
            print("\nPacote reservado com sucesso!")
            print(f"Passagem: {resposta.codigo_reserva_passagem}")
            if resposta.codigo_reserva_hotel:
                print(f"Hotel: {resposta.codigo_reserva_hotel}")
            if resposta.codigo_reserva_carro:
                print(f"Carro: {resposta.codigo_reserva_carro}")
        else:
            print(f"\nFalha ao reservar pacote: {resposta.mensagem}")

if __name__ == "__main__":
    solicitar_pacote()
