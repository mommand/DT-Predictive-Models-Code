import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import autocorrelation_plot
import pandas as pd

class DataUnderstanding:
    
    def descriptive_statistics(self, df):
        print("Descriptive Statistics:")
        print(df['bpm'].describe())

    def distribution_analysis(self, df):
        sns.histplot(df['bpm'], bins=20, kde=True)
        plt.title('Heart Rate Distribution')
        plt.xlabel('BPM')
        plt.ylabel('Frequency')
        plt.show()

    def time_series_analysis(self, df):
        if 'dateTime' not in df.columns:
            df['dateTime'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'].astype(str))

        plt.figure(figsize=(12, 6))
        plt.plot(df['dateTime'], df['bpm'])
        plt.title('Heart Rate Over Time')
        plt.xlabel('Time')
        plt.ylabel('BPM')
        plt.show()

        rolling_mean = df['bpm'].rolling(window=60).mean()
        rolling_std = df['bpm'].rolling(window=60).std()

        plt.figure(figsize=(12, 6))
        plt.plot(df['dateTime'], rolling_mean, label='Rolling Mean')
        plt.plot(df['dateTime'], rolling_std, label='Rolling Std', color='red')
        plt.title('Rolling Mean and Standard Deviation of Heart Rate')
        plt.legend()
        plt.show()

    def correlation_analysis(self, df):
        autocorrelation_plot(df['bpm'])
        plt.title('Autocorrelation of Heart Rate')
        plt.show()

    def outlier_detection(self, df):
        sns.boxplot(x=df['bpm'])
        plt.title('Box Plot of Heart Rate')
        plt.show()

    def seasonal_trend_analysis(self, df):
        df['hour'] = df['dateTime'].dt.hour
        hourly_avg = df.groupby('hour')['bpm'].mean()

        plt.figure(figsize=(10, 6))
        hourly_avg.plot()
        plt.title('Average Heart Rate by Hour of the Day')
        plt.xlabel('Hour')
        plt.ylabel('Average BPM')
        plt.show()

    def missing_data_analysis(self, df):
        sns.heatmap(df.isnull(), cbar=False)
        plt.title('Missing Data Heatmap')
        plt.show()

    def confidence_level_analysis(self, df):
        if 'confidence' in df.columns:
            sns.histplot(df['confidence'], bins=10)
            plt.title('Distribution of Confidence Levels')
            plt.xlabel('Confidence')
            plt.ylabel('Frequency')
            plt.show()
        else:
            print("The 'confidence' column is missing from the DataFrame. Skipping confidence level analysis.")
