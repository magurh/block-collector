import asyncio
from datetime import UTC, datetime

import aiohttp
import structlog
from aiohttp import ClientSession
from google.cloud import storage

from block_collector.config import NetworkConfig, config, flr_config, sgb_config
from block_collector.gcp_storage import uploader_loop
from block_collector.parser import append_blocks
from block_collector.retriever import fetch_data

logger = structlog.get_logger(__name__)


async def collector_loop(network_config: NetworkConfig, session: ClientSession) -> None:
    """Continuously fetch and save blocks for a given network."""
    config.output_dir.mkdir(exist_ok=True)
    csv_file = (
        config.output_dir
        / f"{network_config.network}_blocks_{datetime.now(UTC):%Y%m%d}.csv"
    )
    max_height = -1

    while True:
        items = await fetch_data(session, network_config.explorer_url)
        if items:
            # append only the fields you care about
            max_height = append_blocks(csv_file, items, max_height)
            logger.info(
                "Appended to CSV", network=network_config.network, count=len(items)
            )
        await asyncio.sleep(network_config.wait_time)


async def main() -> None:
    """Main loop."""
    # Initialize GCP client
    storage_client = storage.Client()

    # Create a shared HTTP session
    async with aiohttp.ClientSession(headers={"accept": "application/json"}) as session:
        # Schedule collector tasks
        tasks = [
            collector_loop(flr_config, session),
            collector_loop(sgb_config, session),
            uploader_loop(
                storage_client=storage_client,
                bucket_name=config.gcp_bucket,
                output_dir=config.output_dir,
                upload_interval=config.upload_interval,
            ),
        ]
        await asyncio.gather(*tasks)


def start() -> None:
    """Start app."""
    asyncio.run(main())


if __name__ == "__main__":
    start()
