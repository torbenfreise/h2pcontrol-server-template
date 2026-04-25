import asyncio
import logging

from h2pcontrol.sdk import H2PServerConfig

from service import ExampleService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


async def main():
    cfg = H2PServerConfig.load()
    svc = ExampleService(cfg)
    await svc.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
