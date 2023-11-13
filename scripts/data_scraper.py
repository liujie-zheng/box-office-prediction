import pandas as pd
import argparse
import requests
from bs4 import BeautifulSoup
import csv
import os

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--metadata', default='../metadata.csv')
    parser.add_argument('--out', default='../data')
    return parser.parse_args()


def extract_data(url, out_path):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        div = soup.find('div', class_='a-section imdb-scroll-table-inner')
        headers = [th.get_text(strip=True) for th in div.find_all('th')]

        rows = []
        for tr in div.find_all('tr'):
            cells = tr.find_all('td')
            row_data = [cell.get_text(strip=True) for cell in cells]
            if row_data:
                rows.append(row_data)

        all_data = [headers] + rows

        with open(out_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(all_data)
        print("csv written to", out_path)
        return all_data
    except:
        print("Error loading", url)
        return None


if __name__ == "__main__":
    args = parse_args()

    df = pd.read_csv(args.metadata)
    metadata = df[['Movie', 'Url']].to_dict(orient='records')

    for movie in metadata:
        name = movie.get('Movie')
        url = movie.get('Url')
        out_path = os.path.join(args.out, f'{name}.csv')
        data = extract_data(url, out_path)