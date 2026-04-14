import asyncio
import logging

import config
import manager
import service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


async def register_service(cfg):
    try:
        await manager.connect(cfg)
    except Exception as e:
        logger.error(f"Failed to register service with h2pcontrol manager: {e}")


async def main():
    cfg = config.H2PConfig()  # type: ignore[call-arg]
    await asyncio.gather(
        service.run(cfg),
        register_service(cfg),
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
