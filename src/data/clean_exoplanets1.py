import pandas as pd

print("Cleaning exoplanet dataset...")

df = pd.read_csv("data/raw/exoplanets1.csv")

print("Original shape:", df.shape)

# Select relevant columns
df = df[["pl_name", "pl_rade", "pl_orbper", "disc_year"]]

# i'll drop rows with missing orbital period or radius
df = df.dropna(subset=["pl_rade", "pl_orbper"])

# Remove extreme outliers (physically unrealistic)
df = df[df["pl_rade"] < 50]        # planets larger than this are suspicious, could be gas giants, binary stars, etc.
df = df[df["pl_orbper"] < 100000]  # ~273 years

print("After cleaning shape:", df.shape)
print(df.head())

# Save
df.to_csv("data/processed/exoplanets1_clean.csv", index=False)

print("Clean dataset saved to data/processed/exoplanets1_clean.csv")
