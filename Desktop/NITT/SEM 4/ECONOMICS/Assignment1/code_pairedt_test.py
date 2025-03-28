import pandas as pd
from scipy import stats

# Load the dataset
merged_data = pd.read_csv('dataset.csv')

# Print the first few rows to check the data
print(merged_data.head())

# Remove commas and convert to numeric
merged_data['in_store_price'] = merged_data['in_store_price'].replace({',': ''}, regex=True).astype(float)
merged_data['amazon_price'] = merged_data['amazon_price'].replace({',': ''}, regex=True).astype(float)

# Check if any non-numeric values were converted to NaN
print(merged_data.isnull().sum())

# Drop rows with NaN values in the relevant columns (if any)
merged_data.dropna(subset=['in_store_price', 'amazon_price'], inplace=True)

# Perform the paired t-test
t_stat, p_value = stats.ttest_rel(merged_data['in_store_price'], merged_data['amazon_price'])

# Print the results
print(f"T-statistic: {t_stat}, P-value: {p_value}")

# Calculate the correlation between in-store prices and Amazon prices
correlation = merged_data['in_store_price'].corr(merged_data['amazon_price'])

# Print the correlation result
print(f"Correlation between in-store and Amazon prices: {correlation}")
