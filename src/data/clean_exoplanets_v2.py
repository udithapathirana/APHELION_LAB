import pandas as pd
import numpy as np

print("Cleaning extended exoplanet dataset with enhanced features...")

# --------------------------------------------------

INPUT_PATH = "data/raw/exoplanets.csv"
OUTPUT_PATH = "data/processed/clean_exoplanets_extended_v2.csv"

df = pd.read_csv(INPUT_PATH)
print(f"Raw dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")

# --------------------------------------------------

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

    # Star properties
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

critical_columns = [
    "pl_name",
    "pl_rade",
    "disc_year",
    "discoverymethod"
]

df = df.dropna(subset=critical_columns)
print(f"After dropping critical nulls: {df.shape}")

# basic derived columns

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

df["habitable_candidate_basic"] = (
    (df["pl_rade"] <= 2.0) &
    (df["pl_eqt"] >= 200) &
    (df["pl_eqt"] <= 350)
)

# --------------------------------------------------

# Surface gravity relative to Earth (g ∝ mass / radius²)

df["surface_gravity_rel"] = (df["pl_masse"] / (df["pl_rade"] ** 2))

# escape velocity category based on simplified v_esc ∝ sqrt(mass / radius)

def classify_escape_velocity(mass, radius):
    if pd.isna(mass) or pd.isna(radius):
        return "Unknown"
    v_esc = (mass / radius) ** 0.5  # Simplified relative measure
    if v_esc < 0.8:
        return "Low (can't hold atmosphere)"
    elif v_esc <= 1.2:
        return "Earth-like"
    else:
        return "High (thick atmosphere)"

df["escape_velocity_class"] = df.apply(
    lambda row: classify_escape_velocity(row["pl_masse"], row["pl_rade"]), 
    axis=1
)

#density based composition approximation

def guess_composition(density):
    if pd.isna(density):
        return "Unknown"
    elif density < 2.0:
        return "Gas/Ice (Saturn-like)"
    elif density < 4.0:
        return "Water/Ice-rich"
    elif density < 6.0:
        return "Rocky (silicate)"
    else:
        return "Iron-rich core"

df["composition_approx"] = df["pl_dens"].apply(guess_composition)

# start luminosity classification based on Stefan-Boltzmann law (L ∝ R² × T⁴)

def classify_star_luminosity(radius, teff):
    if pd.isna(radius) or pd.isna(teff):
        return "Unknown"
    # Stefan-Boltzmann: L ∝ R² × T⁴ (relative to Sun)
    luminosity = (radius ** 2) * ((teff / 5778) ** 4)
    if luminosity < 0.1:
        return "Dim (Red dwarf)"
    elif luminosity <= 2.0:
        return "Sun-like"
    else:
        return "Bright (Giant)"

df["star_luminosity_class"] = df.apply(
    lambda row: classify_star_luminosity(row["st_rad"], row["st_teff"]), 
    axis=1
)

#habitable zone position based on insolation (Earth = 1.0)

def habitable_zone_position(insol):
    if pd.isna(insol):
        return "Unknown"
    elif insol < 0.25:
        return "Too cold (outer)"
    elif insol <= 1.1:
        return "Habitable zone"
    elif insol <= 4.0:
        return "Inner edge (hot)"
    else:
        return "Too hot (Venus-like)"

df["hz_position"] = df["pl_insol"].apply(habitable_zone_position)

# detction difficulty score (0-5 scale based on size, orbital period, and method)

def detection_difficulty(radius, orbper, method):
    score = 0
    # Smaller planets = harder to detect
    if radius < 1.0:
        score += 3
    elif radius < 2.0:
        score += 1
    
    # Longer orbital period = harder to detect
    if orbper > 365:
        score += 2
    elif orbper > 100:
        score += 1
    
    # Method-specific difficulty
    if method == "Radial Velocity":
        score += 1
    elif method == "Imaging":
        score += 2
    
    return score

df["detection_difficulty"] = df.apply(
    lambda row: detection_difficulty(row["pl_rade"], row["pl_orbper"], row["discoverymethod"]),
    axis=1
)

# discovery method category simplification

def method_category(method):
    if pd.isna(method):
        return "Unknown"
    if "Transit" in method:
        return "Transit"
    elif "Radial Velocity" in method:
        return "Radial Velocity"
    elif "Imaging" in method:
        return "Direct Imaging"
    elif "Microlensing" in method:
        return "Microlensing"
    else:
        return "Other"

df["discovery_method_category"] = df["discoverymethod"].apply(method_category)

#earth similarity index (0-1 scale based on radius and equilibrium temperature)

def earth_similarity_index(radius, eqt):
    if pd.isna(radius) or pd.isna(eqt):
        return 0.0
    
    # Simplified ESI calculation
    # Compares planetary radius and equilibrium temperature to Earth
    radius_term = 1 - abs(radius - 1.0) / (radius + 1.0)
    temp_term = 1 - abs(eqt - 288) / (eqt + 288)
    
    # Geometric mean
    esi = (radius_term * temp_term) ** 0.5
    return round(esi, 3)

df["earth_similarity_index"] = df.apply(
    lambda row: earth_similarity_index(row["pl_rade"], row["pl_eqt"]),
    axis=1
)

# planetary age proxy based on stellar temperature (cooler stars are generally older, hotter stars are younger)

# Cooler stars are generally older (rough proxy based on stellar temperature)
df["star_age_proxy"] = pd.cut(
    df["st_teff"],
    bins=[0, 4000, 5500, 7000, 50000],
    labels=["Old/Cool", "Mature", "Young/Hot", "Very Young"]
)

# extreme world classification based on temperature, size, and orbital period

def classify_extreme(eqt, rade, orbper):
    if pd.isna(eqt) or pd.isna(rade) or pd.isna(orbper):
        return "Unknown"
    
    if eqt > 1500:
        return "Lava world"
    elif eqt < 50:
        return "Ice world"
    elif orbper < 1:
        return "Hot Jupiter"
    elif rade > 10:
        return "Super Jupiter"
    elif rade < 0.5:
        return "Sub-Earth"
    else:
        return "Normal"

df["extreme_classification"] = df.apply(
    lambda row: classify_extreme(row["pl_eqt"], row["pl_rade"], row["pl_orbper"]),
    axis=1
)

# year since  discovery calculation

df["years_since_discovery"] = 2026 - df["disc_year"]

# multi-criteria habitable candidate (more stringent than basic)

df["habitable_candidate_multi"] = (
    # Size: Rocky planets only
    (df["pl_rade"] >= 0.5) & (df["pl_rade"] <= 1.5) &
    
    # Mass: Earth-like (if available)
    ((df["pl_masse"].isna()) | ((df["pl_masse"] >= 0.3) & (df["pl_masse"] <= 3.0))) &
    
    # Temperature: Conservative liquid water range
    (df["pl_eqt"] >= 273) & (df["pl_eqt"] <= 323) &
    
    # Insolation: Similar to Earth
    ((df["pl_insol"].isna()) | ((df["pl_insol"] >= 0.5) & (df["pl_insol"] <= 2.0))) &
    
    # Star: Sun-like types (if available)
    ((df["st_spectype"].isna()) | (df["st_spectype"].str[0].isin(['G', 'K']))) &
    
    # Density: Rocky composition (if available)
    ((df["pl_dens"].isna()) | ((df["pl_dens"] >= 4.0) & (df["pl_dens"] <= 7.0)))
)

# habitability score calculation based on multiple factors (size, temperature, insolation, star type, density)

def calculate_habitability_score(row):
    score = 0
    
    # Size similarity to Earth (max 25 points)
    if pd.notna(row["pl_rade"]):
        if 0.8 <= row["pl_rade"] <= 1.2:
            score += 25
        elif 0.5 <= row["pl_rade"] <= 1.5:
            score += 15
        elif 0.3 <= row["pl_rade"] <= 2.0:
            score += 5
    
    # Temperature in habitable zone (max 30 points)
    if pd.notna(row["pl_eqt"]):
        if 273 <= row["pl_eqt"] <= 323:
            score += 30
        elif 250 <= row["pl_eqt"] <= 350:
            score += 15
        elif 200 <= row["pl_eqt"] <= 400:
            score += 5
    
    # Insolation (max 20 points)
    if pd.notna(row["pl_insol"]):
        if 0.75 <= row["pl_insol"] <= 1.25:
            score += 20
        elif 0.5 <= row["pl_insol"] <= 2.0:
            score += 10
        elif 0.25 <= row["pl_insol"] <= 4.0:
            score += 5
    
    # Star type (max 15 points)
    if pd.notna(row["st_spectype"]):
        if row["st_spectype"][0] == 'G':
            score += 15
        elif row["st_spectype"][0] == 'K':
            score += 10
        elif row["st_spectype"][0] == 'F':
            score += 5
    
    # Density indicates rocky composition (max 10 points)
    if pd.notna(row["pl_dens"]):
        if 5.0 <= row["pl_dens"] <= 6.0:
            score += 10
        elif 4.0 <= row["pl_dens"] <= 7.0:
            score += 5
    
    return score

df["habitability_score"] = df.apply(calculate_habitability_score, axis=1)

# High confidence = score >= 70
df["high_confidence_habitable"] = df["habitability_score"] >= 70

# --------------------------------------------------
#  FINAL OVERVIEW
# --------------------------------------------------

print("\n Enhanced dataset created!")
print(f"Final shape: {df.shape}")

print("\n BASIC CLASSIFICATIONS:")
print("\nPlanet size distribution:")
print(df["planet_size_class"].value_counts())

print("\nDiscovery era distribution:")
print(df["discovery_era"].value_counts())

print("\n HABITABILITY METRICS:")
print("\nBasic habitable candidates:")
print(df["habitable_candidate_basic"].value_counts())

print("\nMulti-criteria habitable candidates:")
print(df["habitable_candidate_multi"].value_counts())

print("\nHigh confidence habitable (score ≥70):")
print(df["high_confidence_habitable"].value_counts())

print("\nHabitability score distribution:")
print(df["habitability_score"].describe())

print("\n COMPOSITION & PHYSICAL PROPERTIES:")
print("\nComposition approximation:")
print(df["composition_approx"].value_counts())

print("\nEscape velocity class:")
print(df["escape_velocity_class"].value_counts())

print("\n STELLAR CONTEXT:")
print("\nStar luminosity class:")
print(df["star_luminosity_class"].value_counts())

print("\nHabitable zone position:")
print(df["hz_position"].value_counts())

print("\n🔭 DISCOVERY INSIGHTS:")
print("\nDiscovery method category:")
print(df["discovery_method_category"].value_counts())

print("\nExtreme world classification:")
print(df["extreme_classification"].value_counts())

print("\n🏆 TOP 10 MOST EARTH-LIKE PLANETS (by ESI):")
top_esi = df.nlargest(10, "earth_similarity_index")[["pl_name", "earth_similarity_index", "habitability_score", "pl_rade", "pl_eqt"]]
print(top_esi.to_string(index=False))

# save

df.to_csv(OUTPUT_PATH, index=False)
print(f"\n Saved enhanced dataset to: {OUTPUT_PATH}")
print(f"Total columns: {len(df.columns)}")
print("\nNew derived columns added:")
derived_cols = [
    "planet_size_class", "discovery_era", "habitable_candidate_basic",
    "surface_gravity_rel", "escape_velocity_class", "composition_approx",
    "star_luminosity_class", "hz_position", "detection_difficulty",
    "discovery_method_category", "earth_similarity_index", "star_age_proxy",
    "extreme_classification", "years_since_discovery", "habitable_candidate_multi",
    "habitability_score", "high_confidence_habitable"
]
for col in derived_cols:
    print(f"  ✓ {col}")

print("\n Processing complete!")