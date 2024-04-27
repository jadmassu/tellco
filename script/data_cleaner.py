import pandas as pd
import numpy as np
from scipy import stats

class DataCleaner:
    def __init__(self, df):
        if not isinstance(df, pd.DataFrame):
            print("Error, Input is not a DataFrame.")
            self.df = None
        else:
            self.df = df
    def get_missing_values(self):
        missing_values_count = self.df.isnull().sum()
        total_rows = self.df.shape[0]
        missing_values_percentage = (missing_values_count / total_rows) * 100
        missing_values_df = pd.DataFrame({'Missing Values': missing_values_count, 'Missing Values Percentage': missing_values_percentage})
        return missing_values_df

    def handle_missing_values_numbers(self, strategy='mean', axis=0):
        try:
            if strategy == 'mean':
                self.df.fillna(self.df.mean(), inplace=True, axis=axis)
            elif strategy == 'median':
                self.df.fillna(self.df.median(), inplace=True, axis=axis)
            elif strategy == 'mode':
                self.df.fillna(self.df.mode().iloc[0], inplace=True, axis=axis)
            elif strategy == 'drop':
                self.df.dropna(axis=axis, inplace=True)
            else:
                print("Invalid strategy. Defaulting to 'mean'.")
                self.df.fillna(self.df.mean(), inplace=True, axis=axis)
        except Exception as e:
            print(f"Error handling missing values: {e}")
        return self.df

    def handle_missing_values_strings(self, strategy='mode', axis=0, fill_value='Unknown'):
        try:
            if strategy == 'mode':
                self.df.fillna(self.df.mode().iloc[0], inplace=True, axis=axis)
            elif strategy == 'fill':
                self.df.fillna(fill_value, inplace=True, axis=axis)
            elif strategy == 'drop':
                self.df.dropna(axis=axis, inplace=True)
            else:
                print("Invalid strategy. Defaulting to 'mode'.")
                self.df.fillna(self.df.mode().iloc[0], inplace=True, axis=axis)
        except Exception as e:
            print(f"Error handling missing values: {e}")
        return self.df

    def remove_duplicates(self):
        try:
            self.df.drop_duplicates(inplace=True)
        except Exception as e:
            print(f"Error removing duplicates: {e}")
        return self.df
    
    def handle_outliers(self, method='z-score', threshold=3):
        try:
            # Exclude columns with string values
            numeric_columns = self.df.select_dtypes(include=[np.number]).columns
            
            if method == 'z-score':
                z_scores = np.abs(stats.zscore(self.df[numeric_columns]))
                self.df = self.df[(z_scores < threshold).all(axis=1)]
            elif method == 'iqr':
                Q1 = self.df[numeric_columns].quantile(0.25)
                Q3 = self.df[numeric_columns].quantile(0.75)
                IQR = Q3 - Q1
                self.df = self.df[~((self.df[numeric_columns] < (Q1 - 1.5 * IQR)) | (self.df[numeric_columns] > (Q3 + 1.5 * IQR))).any(axis=1)]
        except Exception as e:
            print(f"Error handling outliers: {e}")
        return self.df
    
    def standardize_textual_data(self, column):
        try:
            self.df[column] = self.df[column].str.lower()
            self.df[column] = self.df[column].str.strip()
        except Exception as e:
            print(f"Error standardizing textual data: {e}")
        return self.df
    
    def handle_inconsistencies(self, column, mapping):
        try:
            self.df[column] = self.df[column].replace(mapping)
        except Exception as e:
            print(f"Error handling inconsistencies: {e}")
        return self.df
    
    def convert_data_types(self, column, data_type):
        try:
            self.df[column] = self.df[column].astype(data_type)
        except Exception as e:
            print(f"Error converting data types: {e}")
        return self.df
    
    def normalize_numerical_data(self, method='min-max'):
        try:
            # Select only numeric columns
            numeric_columns = self.df.select_dtypes(include=[np.number]).columns
            
            if method == 'min-max':
                for col in numeric_columns:
                    self.df[col] = (self.df[col] - self.df[col].min()) / (self.df[col].max() - self.df[col].min())
            elif method == 'z-score':
                for col in numeric_columns:
                    self.df[col] = (self.df[col] - self.df[col].mean()) / self.df[col].std()
        except Exception as e:
            print(f"Error normalizing numerical data: {e}")
        return self.df
