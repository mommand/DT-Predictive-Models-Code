import numpy as np
import pandas as pd
import json
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from scipy import stats

class DataPreprocessing:
    
    def load_data(self, json_file_path, date_format='%m/%d/%y %H:%M:%S'):
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        if not all('dateTime' in entry for entry in data):
            raise KeyError("The 'dateTime' field is missing in the JSON data.")

        df = pd.DataFrame([{
            'dateTime': datetime.strptime(entry['dateTime'], date_format),
            'bpm': entry['value']['bpm'],
            'confidence': entry['value']['confidence']
        } for entry in data])

        df['date'] = df['dateTime'].dt.date
        df['time'] = df['dateTime'].dt.time
        df['minute'] = df['dateTime'].dt.minute
        df['second'] = df['dateTime'].dt.second
        df['week'] = df['dateTime'].dt.isocalendar().week

        return df

    def filter_by_confidence(self, df, confidence_threshold=2):
        df = df[df['confidence'] >= confidence_threshold].reset_index(drop=True)
        return df

    def sort_data(self, df):
        df = df.sort_values('dateTime').reset_index(drop=True)
        return df

    def check_time_interval(self, df, expected_interval_seconds=60):
        df['time_diff'] = df['dateTime'].diff().dt.total_seconds()
        inconsistent = df[df['time_diff'] != expected_interval_seconds]

        if not inconsistent.empty:
            print("Inconsistent time intervals found:")
            print(inconsistent[['dateTime', 'time_diff']])
        else:
            print("All time intervals are consistent.")

        df.drop('time_diff', axis=1, inplace=True)
        return df

    def handle_missing_values(self, df):
        df['bpm'].fillna(method='ffill', inplace=True)
        return df

    def remove_outliers(self, df, z_threshold=3):
        df['z_score'] = np.abs(stats.zscore(df['bpm']))
        df = df[df['z_score'] < z_threshold].reset_index(drop=True)
        df.drop('z_score', axis=1, inplace=True)
        return df

    def remove_noise(self, df, window_size=3):
        df['bpm'] = df['bpm'].rolling(window=window_size, center=True).mean()
        df['bpm'].fillna(method='bfill', inplace=True)
        df['bpm'].fillna(method='ffill', inplace=True)
        return df

    def normalize_data(self, df):
        scaler = MinMaxScaler(feature_range=(0, 1))
        df['bpm_normalized'] = scaler.fit_transform(df['bpm'].values.reshape(-1, 1))
        return df, scaler
