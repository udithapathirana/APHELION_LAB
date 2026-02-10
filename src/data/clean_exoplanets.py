import pandas as pd

print("Cleaning extended exoplanet dataset...")

# load raw extended  exoplanet dataset
INPUT_PATH = "data/raw/exoplanets.csv"
OUTPUT_PATH = "data/processed/clean_exoplanets_extended.csv"

df = pd.read_csv(INPUT_PATH)
print(f"Raw dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")

# select relevant columns and clean data

selected_columns = [
    # Identity
    "pl_name",
    "pl_letter",

    # Planet properties
    "pl_rade",
    "pl_masse",
    "pl_dens",
    "pl_orbper",
    "pl_eqt",
    "pl_insol",

    # Star properties (habitability-lite; because life depends on so many stellar factors)
    "st_teff",
    "st_rad",
    "st_mass",
    "st_spectype",

    # Discovery & trends
    "disc_year",
    "discoverymethod",
    "disc_facility",
    "tran_flag",

    # Position 
    "ra",
    "dec"
]

df = df[selected_columns]
print(f"After column selection: {df.shape}")

# handle missing values
# Drop rows with missing critical values

critical_columns = [
    "pl_name",
    "pl_rade",
    "disc_year",
    "discoverymethod"
]

df = df.dropna(subset=critical_columns)
print(f"After dropping critical nulls: {df.shape}")

# derive new columns

def classify_planet_size(radius):
    if radius < 1.25:
        return "Earth-like"
    elif radius < 2.0:
        return "Super-Earth"
    elif radius < 6.0:
        return "Neptune-like"
    else:
        return "Gas Giant"

df["planet_size_class"] = df["pl_rade"].apply(classify_planet_size)

# --------------------------------------------------

def classify_discovery_era(year):
    if year < 2010:
        return "Pre-2010"
    elif year <= 2015:
        return "2010–2015"
    else:
        return "2016+"

df["discovery_era"] = df["disc_year"].apply(classify_discovery_era)

# --------------------------------------------------

df["habitable_candidate"] = (
    (df["pl_rade"] <= 2.0) &
    (df["pl_eqt"] >= 200) &
    (df["pl_eqt"] <= 350)
)

#final overview

print("\n✅ Clean dataset created!")
print(f"Final shape: {df.shape}")
print("\nPlanet size distribution:")
print(df["planet_size_class"].value_counts())

print("\nDiscovery era distribution:")
print(df["discovery_era"].value_counts())

print("\nHabitable-lite candidates:")
print(df["habitable_candidate"].value_counts())

# save

df.to_csv(OUTPUT_PATH, index=False)
print(f"\n📁 Saved clean dataset to: {OUTPUT_PATH}")
