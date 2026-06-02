import logging

from h2pcontrol.example.v1.example_pb2 import SayHelloRequest, SayHelloResponse
from h2pcontrol.example.v1.example_pb2_grpc import ExampleServiceServicer
from h2pcontrol.sdk.server import Server

logger = logging.getLogger(__name__)


class ExampleService(Server, ExampleServiceServicer):
    def _healthy(self) -> bool:
        return True

    async def SayHello(self, request: SayHelloRequest, context) -> SayHelloResponse:
        logger.info(f"Received request: {request}")
        response = SayHelloResponse(message=f"Hello, {request.name}!")
        logger.info(f"Sending response: {response}")
        return response
