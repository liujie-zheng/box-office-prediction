import os
import pandas as pd
import argparse
import numpy as np

dow_map = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
    'Sunday': 7
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_dir', default='../data_raw')
    parser.add_argument('--out_dir', default='../data_cleaned')
    return parser.parse_args()


def convert_percentage(value):
    if value == '-':
        return np.nan  # Convert '-' to NaN
    return float(value.replace('<', '').replace('%', '').replace('+', '').replace(',', ''))


def clean_and_save_csv(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            df = pd.read_csv(os.path.join(input_folder, filename))

            # seperate Date and Event
            df[['Date_Cleaned', 'Event']] = df['Date'].str.extract(r'(\b\S+ \d+)\s*(.*)', expand=True)
            df = df[['Date_Cleaned', 'Event'] + [col for col in df.columns if col not in ['Date_Cleaned', 'Event']]]
            df.drop(columns=['Date'], inplace=True)
            df.rename(columns = {'Date_Cleaned' : 'Date'}, inplace = True)

            # convert $ and , to numeric
            if 'Daily' in df.columns:
                df['Daily'] = df['Daily'].replace('[\$,]', '', regex=True).astype(int)
            if 'Avg' in df.columns:
                df['Avg'] = df['Avg'].replace('[\$,]', '', regex=True).astype(int)
            if 'To Date' in df.columns:
                df['To Date'] = df['To Date'].replace('[\$,]', '', regex=True).astype(int)
            if 'Theaters' in df.columns:
                df['Theaters'] = df['Theaters'].replace('[\$,]', '', regex=True).astype(int)

            # convert % to numeric
            if '%± YD' in df.columns:
                df['%± YD'] = df['%± YD'].apply(convert_percentage)
                df.rename(columns={'%± YD': 'YD%'}, inplace=True)
            if '%± LW' in df.columns:
                df['%± LW'] = df['%± LW'].apply(convert_percentage)
                df.rename(columns={'%± LW': 'LW%'}, inplace=True)

            # convert Day to numeric
            if 'DOW' in df.columns:
                df['DOW'] = df['DOW'].map(dow_map)

            cleaned_filename = filename.split('.')[0] + '_cleaned.csv'
            out_path = os.path.join(output_folder, cleaned_filename)
            df.to_csv(out_path, index=False)
            print("clean filed saved to", out_path)


if __name__ == "__main__":
    args = parse_args()
    clean_and_save_csv(args.in_dir, args.out_dir)