import utils.util as util
import pandas as pd
import numpy as np

def summarize_data(df):
    
    if not util.is_dataframe(df):
        print("Input is not a DataFrame.")
        return None
    numeric_stats = df.describe().transpose()
    missing_values = df.isnull().sum()
    summary_df = pd.DataFrame(index=df.columns)
    summary_df['Data Type'] = df.dtypes
    summary_df['Missing Values'] = missing_values
    summary_df['Unique Values'] = df.nunique()
    summary_df = summary_df.join(numeric_stats[['mean', 'std', 'min', '25%', '50%', '75%', 'max']])
    return summary_df

#categorize or group each column by dtype
def categorical_summary(df,dtype='object'):
    if not isinstance(df, pd.DataFrame):
        print("Input is not a DataFrame.")
        return None

    categorical_columns = df.select_dtypes(include=[dtype]).columns 

    if len(categorical_columns) == 0:
        print("No categorical columns found in the DataFrame.")
    
    pd.set_option('display.width', 100)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    categorical_summary_df = pd.DataFrame(index=categorical_columns, columns=['Unique Values', 'Value Counts'])

    for column in categorical_columns:
        value_counts = df[column].value_counts()
        categorical_summary_df.at[column, 'Unique Values'] = len(value_counts)
        categorical_summary_df.at[column, 'Value Counts'] = value_counts

    return categorical_summary_df



def value_counts_summary(df, column, display_columns=None):
    if not isinstance(df, pd.DataFrame):
        print("Input is not a DataFrame.")
        return None
    
    value_counts = df[column].value_counts().reset_index()
    value_counts.columns = [column, 'count']
    
    if display_columns:
        value_counts = value_counts.merge(df[display_columns], left_on=column, right_on=display_columns, how='left')
    
    return value_counts




def detect_outliers(data, threshold=1.5):
    # Filter numeric columns in the DataFrame
    numeric_columns = data.select_dtypes(include=np.number).columns
    
    outlier_indices = []
    
    for column in numeric_columns:
        # Convert the column to a NumPy array
        data_array = np.array(data[column])
        
        # Calculate the first quartile (Q1) and third quartile (Q3)
        Q1 = np.percentile(data_array, 25)
        Q3 = np.percentile(data_array, 75)
        
        # Calculate the interquartile range (IQR)
        IQR = Q3 - Q1
        
        # Define the lower and upper bounds for outliers
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        
        # Find the indices of outliers
        column_outliers = np.where((data_array < lower_bound) | (data_array > upper_bound))[0]
        
        # Append the column outliers to the list of outlier indices
        outlier_indices.extend(column_outliers)
    
    return outlier_indices

def group_and_aggregate(df, group_column, agg_columns):
    #(df, GroupColumn', {'Column': 'mean', 'AnotherColumn': 'sum'})
    if not isinstance(df, pd.DataFrame):
        print("Input is not a DataFrame.")
        return None
    grouped_df = df.groupby(group_column).agg(agg_columns)
    return grouped_df


def analyze_dataset(df):
    result = pd.DataFrame(columns=['Column', 'Mean', 'Median', 'Mode', 'Range', 'Standard Deviation'])
    
    for column in df.columns:
        column_data = df[column]
        
        # Convert column data to numeric values if possible
        try:
            column_data = pd.to_numeric(column_data, errors='coerce')
        except ValueError:
            print(f"Warning: Column '{column}' contains non-numeric values.")
            continue
        
        # Calculate mean
        mean = np.mean(column_data)
        
        # Calculate median
        median = np.median(column_data)
        
        # Calculate mode if column data is numeric
        if np.issubdtype(column_data.dtype, np.number):
            mode = stats.mode(column_data)
        else:
            mode = "Mode calculation not applicable for non-numeric data"
        
        # Calculate range
        data_range = np.max(column_data) - np.min(column_data)
        
        # Calculate standard deviation
        std_dev = np.std(column_data)
        
        # Append the analysis results as a new row to the result DataFrame
        result = result.append({
            'Column': column,
            'Mean': mean,
            'Median': median,
            'Mode': mode,
            'Range': data_range,
            'Standard Deviation': std_dev
        }, ignore_index=True)
    
    return result


def calculate_correlation(df):
    if not isinstance(df, pd.DataFrame):
        print("Input is not a DataFrame.")
        return None
    correlation_matrix = df.corr()
    return correlation_matrix

def create_crosstab(df, column1, column2):
    if not isinstance(df, pd.DataFrame):
        print("Input is not a DataFrame.")
        return None
    crosstab_table = pd.crosstab(df[column1], df[column2])
    return crosstab_table

def create_pivot_table(df, numeric_column, index_column, columns_column, aggfunc='mean'):
    if not isinstance(df, pd.DataFrame):
        print("Input is not a DataFrame.")
        return None
        
    pivot_table = pd.pivot_table(df, values=numeric_column,
                                 index=index_column, columns=columns_column,
                                 aggfunc=aggfunc)
    return pivot_table

def find_min_max_in(df, col):
    if not isinstance(df, pd.DataFrame):
        print("Input is not a DataFrame.")
        return None
    top = df[col].idxmax()
    top_df = pd.DataFrame(df.loc[top])
    bottom = df[col].idxmin()
    bottom_df = pd.DataFrame(df.loc[bottom])
    info_df = pd.concat([top_df, bottom_df], axis=1)
    return info_df
