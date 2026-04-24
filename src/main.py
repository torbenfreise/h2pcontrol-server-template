import asyncio
import logging

from service import ExampleService
from h2pcontrol.sdk import H2PServerConfig

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


async def main():
    cfg = H2PServerConfig()  # type: ignore[call-arg]
    service = ExampleService(cfg)
    await service.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
