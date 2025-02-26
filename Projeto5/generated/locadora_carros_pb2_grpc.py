# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import locadora_carros_pb2 as locadora__carros__pb2

GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in locadora_carros_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class LocadoraCarrosStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ReservarCarro = channel.unary_unary(
                '/locadora_carros.LocadoraCarros/ReservarCarro',
                request_serializer=locadora__carros__pb2.ReservaCarroRequest.SerializeToString,
                response_deserializer=locadora__carros__pb2.ReservaCarroResponse.FromString,
                _registered_method=True)


class LocadoraCarrosServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ReservarCarro(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LocadoraCarrosServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ReservarCarro': grpc.unary_unary_rpc_method_handler(
                    servicer.ReservarCarro,
                    request_deserializer=locadora__carros__pb2.ReservaCarroRequest.FromString,
                    response_serializer=locadora__carros__pb2.ReservaCarroResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'locadora_carros.LocadoraCarros', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('locadora_carros.LocadoraCarros', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class LocadoraCarros(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ReservarCarro(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/locadora_carros.LocadoraCarros/ReservarCarro',
            locadora__carros__pb2.ReservaCarroRequest.SerializeToString,
            locadora__carros__pb2.ReservaCarroResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
