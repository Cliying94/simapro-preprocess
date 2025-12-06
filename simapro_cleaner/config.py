"""Configuration values for the SimaPro cleaner."""

CATEGORIES = [
    'Resources',
    'Materials/fuels',
    'Electricity/heat',
    'Emissions to air',
    'Emissisions to water',
    'Emissions to water',
    'emissions to soil',
    'Final waste flows',
    'final waste flows',
    'Non material emissions',
    'Non material emissisions',
    'Social issues',
    'Economic issues',
    'Econcmic issues',
    'Waste to treatment'
]

OUTPUT_COLUMNS = ['Category', 'Name', 'Subcompartment', 'Unit']
MATERIAL_LIKE = {'Materials/fuels', 'Electricity/heat'}
WASTE_CATEGORY = 'Waste to treatment'
FINAL_WASTE_CATEGORIES = {'Final waste flows', 'final waste flows'}

LOCATION_CODES = set([
    'CN', 'US', 'JP', 'IN', 'DE', 'FR', 'GB', 'IT', 'CA', 'BR', 'RU', 'KR', 'ES',
    'AU', 'MX', 'ID', 'NL', 'TR', 'SA', 'CH', 'SE', 'PL', 'BE', 'TH', 'IR', 'NG',
    'AR', 'NO', 'AT', 'ZA', 'DK', 'PH', 'CO', 'MY', 'UA', 'RO', 'SG', 'PT', 'CZ',
    'HU', 'IL', 'HK', 'CL', 'FI', 'PK', 'PE', 'NZ', 'IE', 'GR', 'QA', 'KZ', 'DZ',
    'MA', 'EC', 'BD', 'LY', 'IQ', 'OM', 'TM', 'TT', 'UZ', 'BA', 'AZ', 'NP', 'MK',
    'RS', 'TZ', 'WEU', 'VN', 'ZM', 'AE', 'EG', 'BO', 'TN', 'KW', 'VE', 'GLO',
    'RER', 'ROW', 'RAF', 'RAS', 'RNA', 'RLA', 'RoW', 'SAS', 'EUU', 'UCTE', 'BRN',
    'BRG', 'BRM', 'BRB', 'INW', 'INE', 'UNA', 'UNM', 'UNF', 'UNN', 'UNT', 'UNK',
    'SAF',  # base codes
    'TW', 'LK', 'GH', 'DO', 'SK', 'BG', 'HR', 'SI', 'LT', 'LV', 'EE', 'LU', 'MT',
    'CY', 'IS'  # subdivision prefixes not already listed above
])

KNOWN_AREA_STRINGS = [
    'Europe without Switzerland',
    'Europe without Switzerland and Austria',
    'Europe without Austria',
    'Europe without Quebec',
    'North America without Quebec',
    'Canada without Quebec',
    'IAI Area, Africa',
    'IAI Area, Asia, without China and GCC',
    'IAI Area, EU27 & EFTA',
    'IAI Area, Gulf Cooperation Council',
    'IAI Area, Russia & RER w/o EU27 & EFTA',
    'IAI Area, South America',
    'RER w/o RU',
    'UN-SEASIA',
    'UN-OCEANIA',
    'UN-EASIA',
    'WECC',
    'NORDEL',
    'RoE',
    'RNA',
    'RER',
    'RLA',
    'RAF',
    'RAS',
    'SAS',
    'UCTE',
    'UCTE without Germany'
]

