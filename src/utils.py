import re
import pandas as pd
import os
from datetime import datetime



def link_extractor(input_string):
    pattern = re.compile(r'https://www.screener.in/screens/\d+/.*')
    links = [match.group(0) for match in pattern.finditer(input_string)]
    cleaned_links = [re.sub(r'\?page.*$', '', link, flags=re.MULTILINE)
                     for link in links if link.startswith('https://')]
    return cleaned_links


def fetch_data(link):
    cache_index = None
    data = pd.DataFrame()
    current_page = 1
    page_limit = 100
    while current_page < page_limit:
        url = f'{link}?page={current_page}'
        all_tables = pd.read_html(url, flavor='bs4')
        combined_df = pd.concat(all_tables)
        combined_df = combined_df.drop(
            combined_df[combined_df['S.No.'].isnull()].index)
        if cache_index == combined_df.iloc[-2]['S.No.']:
            break
        cache_index = combined_df.iloc[-2]['S.No.']
        combined_df['URL'] = url
        data = pd.concat([data, combined_df], axis=0)
        current_page += 1
    data = data.iloc[0:].drop(data[data['S.No.'] == 'S.No.'].index)
    return data


def generate_excel(links):
    if not os.path.exists('output'):
        os.makedirs('output')
    _output_df = pd.DataFrame()
    DT_STRING = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    for link in links:
        _output_df = pd.concat([_output_df, fetch_data(link)], axis=0)
    if not _output_df.empty:
        url_col = _output_df.pop('URL')
        _output_df.insert(len(_output_df.columns), 'URL', url_col)
        _output_df.to_excel(f"output/out_{DT_STRING}.xlsx", index=None)
        print(f"[+] File is saves with the name out_{DT_STRING}.xlsx")
    else:
        print("[+] Unable to extract the data for the given links")
