"""Parsing helpers for SimaPro Excel exports."""

from typing import List, Sequence, Tuple

import pandas as pd


def load_excel(path: str) -> pd.DataFrame:
    """Read the provided Excel file into a raw dataframe."""
    return pd.read_excel(path, header=None)


def find_category_blocks(df: pd.DataFrame, categories: Sequence[str]) -> List[Tuple[int, str]]:
    """Return a list of (row_index, category_name) for category headers."""
    block_indices: List[Tuple[int, str]] = []
    for idx, value in df[0].items():
        cell_value = str(value).strip()
        if cell_value in categories:
            block_indices.append((idx, cell_value))
    return block_indices

