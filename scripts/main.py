"""CLI entry-point for cleaning SimaPro Excel exports."""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from simapro_cleaner import batch_clean_and_merge 

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Clean SimaPro Excel exports and merge them into a single workbook.'
    )
    parser.add_argument('--input_dir', required=True, help='Folder containing Excel files exported from SimaPro')
    parser.add_argument('--output', required=True, help='Destination path for the merged Excel file')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    merged = batch_clean_and_merge(args.input_dir, args.output)
    if merged.empty:
        print('No valid data found in the provided directory.')
        return
    output_path = Path(args.output).resolve()
    print(f'Processed {len(merged)} rows from {args.input_dir}.')
    print(f'Merged results saved to {output_path}.')


if __name__ == '__main__':
    main()
