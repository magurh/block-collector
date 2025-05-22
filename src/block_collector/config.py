from dataclasses import dataclass
from pathlib import Path


@dataclass
class NetworkConfig:
    """General Network configuration."""

    network: str
    explorer_url: str
    wait_time: int


flr_config = NetworkConfig(
    network="flare",
    explorer_url="https://flare-explorer.flare.network/api/v2/blocks?type=block",
    wait_time=70,
)

sgb_config = NetworkConfig(
    network="songbird",
    explorer_url="https://songbird-explorer.flare.network/api/v2/blocks?type=block",
    wait_time=40,
)


@dataclass
class Config:
    """General configuration."""

    gcp_bucket: str
    upload_interval: int
    output_dir: Path


config = Config(
    gcp_bucket="block-collector",
    upload_interval=100,
    output_dir=Path("data"),
)
