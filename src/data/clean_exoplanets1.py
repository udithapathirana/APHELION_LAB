import pandas as pd

print("🧹 Cleaning exoplanet dataset...")

# Load raw data
df = pd.read_csv("data/exoplanets1.csv")

print("Original shape:", df.shape)

# Select relevant columns
df = df[["pl_name", "pl_rade", "pl_orbper", "disc_year"]]

# Drop rows with missing orbital period or radius
df = df.dropna(subset=["pl_rade", "pl_orbper"])

# Remove extreme outliers (physically unrealistic)
df = df[df["pl_rade"] < 50]        # planets larger than this are suspicious
df = df[df["pl_orbper"] < 100000]  # ~273 years

print("After cleaning shape:", df.shape)
print(df.head())

# Save cleaned dataset
df.to_csv("data/processed/exoplanets_clean.csv", index=False)

print("✅ Clean dataset saved to data/processed/exoplanets_clean.csv")
