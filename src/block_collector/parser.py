import json
from pathlib import Path

import pandas as pd

CSV_FIELDS = [
    "height",
    "base_fee_per_gas",
    "burnt_fees",
    "burnt_fees_percentage",
    "difficulty",
    "gas_limit",
    "gas_target_percentage",
    "gas_used",
    "gas_used_percentage",
    "hash",
    "parent_hash",
    "priority_fee",
    "size",
    "timestamp",
    "transaction_count",
    "transaction_fees",
]


def parse_block(item: dict) -> dict[str, str]:
    """Extracts only the desired fields from the full JSON block."""
    row: dict[str, str] = {}
    for field in CSV_FIELDS:
        # Pull nested or missing values safely
        value = item.get(field, "")
        # if it is not a str/int/float, convert to JSON string
        if not isinstance(value, (str, int, float)):
            value = json.dumps(value)
        row[field] = str(value)
    return row


def append_blocks(
    csv_path: Path,
    blocks: list[dict],
    prev_max_height: int = -1,
) -> int:
    """Parse list of blocks."""
    # Parse blocks
    parsed = pd.DataFrame([parse_block(b) for b in blocks])
    parsed["height"] = parsed["height"].astype(int)
    new_rows = parsed[parsed["height"] > prev_max_height]

    if new_rows.empty:
        return prev_max_height

    new_rows = new_rows.sort_values("height")

    # Write to csv
    write_header = not csv_path.exists()
    new_rows.to_csv(
        csv_path,
        mode="a",
        index=False,
        header=write_header,
        columns=CSV_FIELDS,
    )

    return new_rows.iloc[-1]["height"]
