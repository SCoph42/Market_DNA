import pandas as pd

# Load CSV data
df = pd.read_csv("../csv_docs/glbx-mdp3-20250729-20260728.csv")

# Display basic statistics
print("\nBasic Statistics:")
print(df.describe())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Show first 5 rows
print("\nFirst 5 rows:")
print(df.head())