import logging
from types import SimpleNamespace

from grpc import aio
from h2pcontrol.example.v1.example_pb2 import (
    SayHelloRequest,
    SayHelloResponse,
)
from h2pcontrol.example.v1.example_pb2_grpc import (
    ExampleServiceServicer,
    add_ExampleServiceServicer_to_server,
)

logger = logging.getLogger(__name__)


class ExampleService(ExampleServiceServicer):
    async def SayHello(self, request: SayHelloRequest, context) -> SayHelloResponse:
        logger.info(f"Received request: {request}")
        response = SayHelloResponse(message=f"Hello, {request.name}!")
        logger.info(f"Sending response: {response}")
        return response


async def run(config: SimpleNamespace) -> None:
    server = aio.server()
    add_ExampleServiceServicer_to_server(ExampleService(), server)
    server.add_insecure_port(f"{config.service.host}:{config.service.port}")
    await server.start()
    logger.info(f"Server started on {config.service.host}:{config.service.port}")
    await server.wait_for_termination()
    logger.info("Server shutdown complete")
