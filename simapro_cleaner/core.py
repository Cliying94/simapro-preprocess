"""Core cleaning workflow for SimaPro Excel exports."""

import os
from pathlib import Path
from typing import Iterable, List, Optional

import pandas as pd

from .config import (
    CATEGORIES,
    FINAL_WASTE_CATEGORIES,
    MATERIAL_LIKE,
    OUTPUT_COLUMNS,
    WASTE_CATEGORY,
)
from .parser import find_category_blocks, load_excel
from .utils import is_number, strip_country_code


def _extract_category_data(df: pd.DataFrame, start_idx: int, end_idx: int, category_name: str) -> List[dict]:
    """Extract cleaned rows for a specific category block."""
    block = df.iloc[start_idx + 1:end_idx]
    records: List[dict] = []
    for _, row in block.iterrows():
        raw_name = row[0]
        if pd.isna(raw_name):
            break
        if str(raw_name).strip() in CATEGORIES:
            break
        name = strip_country_code(raw_name)
        if is_number(name):
            continue
        subcompartment, unit = _extract_fields_for_category(category_name, row)
        records.append({
            'Category': category_name,
            'Name': name,
            'Subcompartment': subcompartment,
            'Unit': unit,
        })
    return records


def clean_one_excel(path: str) -> pd.DataFrame:
    """Clean a single Excel file and return the normalized dataframe."""
    df = load_excel(path)
    blocks = find_category_blocks(df, CATEGORIES)
    records: List[dict] = []
    for idx, (start, category) in enumerate(blocks):
        end = blocks[idx + 1][0] if idx + 1 < len(blocks) else len(df)
        records.extend(_extract_category_data(df, start, end, category))
    return pd.DataFrame(records, columns=OUTPUT_COLUMNS)


def _concat_records(frames: Iterable[pd.DataFrame]) -> pd.DataFrame:
    dataframes = [frame for frame in frames if not frame.empty]
    if not dataframes:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)
    merged = pd.concat(dataframes, ignore_index=True)
    merged = merged.drop_duplicates(subset=OUTPUT_COLUMNS)
    return merged.reset_index(drop=True)


def _extract_fields_for_category(category_name: str, row: pd.Series) -> tuple[str, str]:
    """Return (subcompartment, unit) values per category rules."""

    def _value(idx: int) -> str:
        return row[idx] if len(row) > idx and pd.notna(row[idx]) else ''

    if category_name == 'Resources':
        return _value(1), _value(3)
    if category_name in MATERIAL_LIKE:
        return '', _value(2)
    if category_name == WASTE_CATEGORY:
        return '', _value(2)
    if category_name in FINAL_WASTE_CATEGORIES:
        return '', _value(3)
    if str(category_name).lower().startswith('emissions'):
        return _value(1), _value(3)
    return _value(3), _value(1)


def clean_directory(input_dir: str) -> pd.DataFrame:
    """Process all Excel files inside the given directory."""
    frames: List[pd.DataFrame] = []
    for fname in sorted(os.listdir(input_dir)):
        if not fname.lower().endswith(('.xlsx', '.xls')):
            continue
        full_path = os.path.join(input_dir, fname)
        frames.append(clean_one_excel(full_path))
    return _concat_records(frames)


def _ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def batch_clean_and_merge(input_dir: str, output_path: Optional[str] = None) -> pd.DataFrame:
    """Clean a directory of Excel files and optionally persist the merged results."""
    merged = clean_directory(input_dir)
    if output_path and not merged.empty:
        output_file = Path(output_path)
        _ensure_parent_dir(output_file)
        merged.to_excel(output_file, index=False)
    return merged

