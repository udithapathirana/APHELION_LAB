import pandas as pd

print("🧹 Cleaning exoplanet data...")

df = pd.read_csv("data/raw/exoplanets_api1.csv")

# Keep only useful columns
columns = ["pl_name", "pl_rade", "pl_orbper", "disc_year"]
df = df[columns]

# Drop rows with missing critical values
df = df.dropna(subset=["pl_rade", "pl_orbper"])

print("After cleaning:", df.shape)
print(df.head())

# Save cleaned data
df.to_csv("data/processed/exoplanets_clean.csv", index=False)

print("✅ Clean data saved to data/processed/exoplanets_clean.csv")
