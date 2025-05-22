import asyncio
from datetime import UTC, datetime
from pathlib import Path

import aiohttp
import structlog
from aiohttp import ClientSession
from google.cloud import storage

from block_collector.config import Config, flr_config, sgb_config
from block_collector.parser import append_blocks
from block_collector.retriever import fetch_data
from block_collector.gcp_storage import uploader_loop

logger = structlog.get_logger(__name__)

# Local output directories
OUTPUT_DIR = Path("data")

# GCP settings
GCS_BUCKET_NAME = "your-gcs-bucket"
UPLOAD_INTERVAL = 15 * 60  # seconds


async def collector_loop(config: Config, session: ClientSession) -> None:
    """Continuously fetch and save blocks for a given network."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    csv_file = OUTPUT_DIR / f"{config.network}_blocks_{datetime.now(UTC):%Y%m%d}.csv"
    max_height = -1

    while True:
        items = await fetch_data(session, config.explorer_url)
        if items:
            # append only the fields you care about
            max_height = append_blocks(csv_file, items, max_height)
            logger.info("Appended to CSV", network=config.network, count=len(items))
        await asyncio.sleep(config.wait_time)


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
                bucket_name=GCS_BUCKET_NAME,
                output_dir=OUTPUT_DIR,
                upload_interval=UPLOAD_INTERVAL,
            ),
        ]
        await asyncio.gather(*tasks)


def start() -> None:
    """Start app."""
    asyncio.run(main())


if __name__ == "__main__":
    start()
