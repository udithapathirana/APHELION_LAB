import pandas as pd

# Load dataset
print(" Loading exoplanet data...")
df = pd.read_csv("data/raw/exoplanets1.csv")

print("\n Data loaded successfully!")

# 1️ Basic shape of the data
print("\n Dataset shape (rows, columns):")
print(df.shape)

# 2️ Column names
print("\n Column names:")
print(list(df.columns))

# 3️ Preview first rows
print("\n First 5 rows:")
print(df.head())

# 4️ Data types
print("\n Data types:")
print(df.dtypes)

# 5 Missing values count
print("\n Missing values per column:")
print(df.isnull().sum())

# 6️ Basic statistics for numeric columns
print("\n Basic statistics:")
print(df.describe())
