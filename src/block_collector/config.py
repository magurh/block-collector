from dataclasses import dataclass


@dataclass
class Config:
    """General configuration."""

    network: str
    explorer_url: str
    wait_time: int


flr_config = Config(
    network="flare",
    explorer_url="https://flare-explorer.flare.network/api/v2/blocks?type=block",
    wait_time=70,
)

sgb_config = Config(
    network="songbird",
    explorer_url="https://songbird-explorer.flare.network/api/v2/blocks?type=block",
    wait_time=40,
)
