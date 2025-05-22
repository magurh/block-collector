import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def load_env_var(var_name: str) -> str:
    """Loads and validates environment variables."""
    return os.getenv(var_name, default="")


@dataclass
class NetworkConfig:
    """General Network configuration."""

    network: str
    explorer_url: str
    wait_time: int


flr_explorer_url = load_env_var("FLR_EXPLORER_URL")

flr_config = NetworkConfig(
    network="flare",
    explorer_url=flr_explorer_url,
    wait_time=70,
)

sgb_explorer_url = load_env_var("SGB_EXPLORER_URL")

sgb_config = NetworkConfig(
    network="songbird",
    explorer_url=sgb_explorer_url,
    wait_time=40,
)

gcp_bucket = load_env_var("GCP_BUCKET_NAME")


@dataclass
class Config:
    """General configuration."""

    gcp_bucket: str
    upload_interval: int
    output_dir: Path


config = Config(
    gcp_bucket=gcp_bucket,
    upload_interval=100,
    output_dir=Path("data"),
)
