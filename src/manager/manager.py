import asyncio
import logging
from types import SimpleNamespace

from grpc import aio
from h2pcontrol.manager.v1.manager_pb2 import (
    HeartbeatRequest,
    RegisterRequest,
    ServiceDefinition,
)
from h2pcontrol.manager.v1.manager_pb2_grpc import ManagerServiceStub

logger = logging.getLogger(__name__)


async def connect(config: SimpleNamespace) -> None:
    async with aio.insecure_channel(config.manager.address) as channel:
        stub = ManagerServiceStub(channel)

        await stub.Register(
            RegisterRequest(
                service=ServiceDefinition(
                    name=config.service.name,
                    description=config.service.description,
                    port=config.service.port,
                )
            )
        )
        logger.info(f"Registered service with h2pcontrol manager at {config.manager.address}")

        async def heartbeat_requests():
            while True:
                yield HeartbeatRequest(healthy=True)
                await asyncio.sleep(config.manager.heartbeat_interval_s)

        async for _ in stub.Heartbeat(heartbeat_requests()):
            logger.debug("Heartbeat acknowledged")
