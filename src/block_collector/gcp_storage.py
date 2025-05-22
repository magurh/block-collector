import asyncio
from pathlib import Path

import structlog
from google.cloud import storage

logger = structlog.get_logger(__name__)


async def uploader_loop(
    storage_client: storage.Client,
    bucket_name: str,
    output_dir: Path,
    upload_interval: int,
) -> None:
    """Periodically upload local files to GCS."""
    bucket = storage_client.bucket(bucket_name)
    while True:
        for local_file in output_dir.glob("*_blocks_*.json"):
            blob = bucket.blob(local_file.name)
            blob.upload_from_filename(local_file)
            logger.info("Uploaded file to GCP bucket", name=local_file.name)
        await asyncio.sleep(upload_interval)
