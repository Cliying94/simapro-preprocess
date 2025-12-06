import os
import pandas as pd
import re

CATEGORIES = [
    'Resources', 'Materials/fuels', 'Electricity/heat', 'Emissions to air',
    'Emissisions to water', 'Emissions to water', 'emissions to soil',
    'Final waste flows', 'final waste flows',
    'Non material emissions', 'Non material emissisions',
    'Social issues', 'Economic issues', 'Econcmic issues',
    'Waste to treatment'
]

KNOWN_CODES = set([
    # 兩碼
    'CN', 'US', 'JP', 'IN', 'DE', 'FR', 'GB', 'IT', 'CA', 'BR', 'RU', 'KR', 'ES', 'AU', 'MX', 'ID', 'NL', 'TR', 'SA', 'CH', 'SE', 'PL', 'BE', 'TH', 'IR', 'NG', 'AR', 'NO', 'AT', 'ZA', 'DK', 'PH', 'CO', 'MY', 'UA', 'RO', 'SG', 'PT', 'CZ', 'HU', 'IL', 'HK', 'CL', 'FI', 'PK', 'PE', 'NZ', 'IE', 'GR', 'QA', 'KZ', 'DZ', 'MA', 'EC', 'BD', 'LY', 'IQ', 'OM', 'TM', 'TT', 'UZ', 'BA', 'AZ', 'NP', 'MK', 'MA', 'RS', 'TZ', 'UA', 'WEU', 'VN', 'ZM', 'GB', 'AE', 'EG', 'BD', 'BO',
    'TN', 'KW', 'VE',  # 新增
    # 三碼
    'GLO', 'RER', 'ROW', 'RAF', 'RAS', 'RNA', 'RLA', 'RoW', 'SAS', 'EUU', 'UCTE', 'IL', 'BRN', 'BRG', 'BRM', 'BRB', 'INW', 'INE', 'UNA', 'UNM', 'UNF', 'UNN', 'UNT', 'UNK', 'UNA', 'SAF',
])

KNOWN_AREA_STRINGS = [
    'Europe without Switzerland', 'Europe without Switzerland and Austria',
    'Europe without Austria', 'Europe without Quebec', 'North America without Quebec',
    'Canada without Quebec', 'IAI Area, Africa', 'IAI Area, Asia, without China and GCC',
    'IAI Area, EU27 & EFTA', 'IAI Area, Gulf Cooperation Council', 'IAI Area, Russia & RER w/o EU27 & EFTA',
    'IAI Area, South America', 'RER w/o RU', 'UN-SEASIA', 'UN-OCEANIA', 'UN-EASIA',
    'WECC', 'NORDEL', 'RoE', 'RNA', 'RER', 'RLA', 'RAF', 'RAS', 'SAS', 'UCTE', 'UCTE without Germany'
    # 可依需求自行增加
]


def strip_country_code(name):
    val = str(name).strip()
    # 先移除 {...}，若內容是國家/地區/電網/片語名單就拿掉
    val = re.sub(
        r'\{([^{}]+)\}',
        lambda m: '' if (m.group(1).strip() in KNOWN_CODES or m.group(
            1).strip() in KNOWN_AREA_STRINGS) else m.group(0),
        val
    )
    # 清掉多餘逗號
    val = re.sub(r',\s*,', ',', val)
    val = val.strip().strip(',')

    # 再檢查是否為已知國家/區域尾碼
    m = re.match(r"(.+),\s*([^,]+)$", val)
    if m:
        main, tail = m.group(1).strip(), m.group(2).strip()
        if tail in KNOWN_CODES:
            return main
        if re.match(r"^(US|IN|CA|CN|BR|AU|RU|ZA|MX|EG|DE|FR|IT|KR|JP|TW|CH|TR|NL|BE|SE|AT|ES|NO|PL|DK|GR|FI|PT|HU|CZ|IE|SG|UA|AR|CO|CL|MY|PH|RO|TH|IL|ID|PE|NG|SA|IR|PK|BD|RS|KZ|QA|AE|NZ|LK|GH|MA|DO|EC|BO|SK|BG|HR|SI|LT|LV|EE|LU|MT|CY|IS)-[A-Z0-9]+$", tail):
            return main
        for area in KNOWN_AREA_STRINGS:
            if tail == area:
                return main
        if tail.startswith('Europe without') or tail.startswith('North America without') or tail.startswith('Canada without'):
            return main
    return val


def is_number(val):
    try:
        return re.fullmatch(r"[\d,.]+", str(val).replace(" ", "")) is not None
    except:
        return False


def find_category_blocks(df, categories):
    block_indices = []
    for i, row in df.iterrows():
        val = str(row[0]).strip()
        if val in categories:
            block_indices.append((i, val))
    return block_indices


def extract_category_data(df, start_idx, end_idx, category_name):
    block = df.iloc[start_idx+1:end_idx]
    result = []
    for _, row in block.iterrows():
        name = row[0]
        if pd.isna(name) or str(name).strip() in CATEGORIES:
            break
        name = strip_country_code(name)
        if is_number(name):
            continue

        # Electricity/heat 欄位選法等同 Materials/fuels
        if category_name in ['Materials/fuels', 'Electricity/heat']:
            unit = row[2] if len(row) > 2 else ''
            subcompartment = ''
        else:  # Resources 及其他大類
            unit = row[1] if len(row) > 1 else ''
            subcompartment = row[3] if len(row) > 3 else ''
        result.append({
            "Category": category_name,
            "Name": name,
            "Unit": unit,
            "Subcompartment": subcompartment
        })
    return result


def clean_one_excel(path):
    df = pd.read_excel(path, header=None)
    blocks = find_category_blocks(df, CATEGORIES)
    records = []
    for idx, (start, cat) in enumerate(blocks):
        end = blocks[idx+1][0] if idx+1 < len(blocks) else len(df)
        records.extend(extract_category_data(df, start, end, cat))
    result_df = pd.DataFrame(records)
    return result_df


def batch_clean_and_merge(input_dir, output_path):
    all_records = []
    for fname in os.listdir(input_dir):
        if fname.lower().endswith(('.xlsx', '.xls', 'XLSX', '.XLS')):
            full_path = os.path.join(input_dir, fname)
            print(f"Processing {fname} ...")
            df = clean_one_excel(full_path)
            print(f"{fname} -> {len(df)} records")
            if not df.empty:
                all_records.append(df)
    if all_records:
        merged = pd.concat(all_records, ignore_index=True)
        merged = merged.drop_duplicates(
            subset=["Category", "Name", "Unit", "Subcompartment"])
        merged.to_excel(output_path, index=False)
        print(f"Done! All results saved to {output_path}")
    else:
        print("No valid data found in any Excel files.")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', required=True,
                        help='Folder containing Excel files')
    parser.add_argument('--output', required=True,
                        help='Path for merged output excel')
    args = parser.parse_args()
    batch_clean_and_merge(args.input_dir, args.output)
