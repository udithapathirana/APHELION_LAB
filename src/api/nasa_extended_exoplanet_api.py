import pandas as pd

print("Starting NASA Exoplanet fetch (Comprehensive Dataset)...")

# Comprehensive query with all scientifically relevant columns
url = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    "?query=select+"
    # Planet Properties
    "pl_name,pl_letter,"
    "pl_rade,pl_radeerr1,pl_radeerr2,"  # Radius + uncertainties
    "pl_masse,pl_masseerr1,pl_masseerr2,"  # Mass + uncertainties
    "pl_dens,pl_denserr1,pl_denserr2,"  # Density
    "pl_orbper,pl_orbpererr1,pl_orbpererr2,"  # Orbital period
    "pl_orbsmax,pl_orbsmaxerr1,pl_orbsmaxerr2,"  # Semi-major axis
    "pl_orbeccen,pl_orbeccenerr1,pl_orbeccenerr2,"  # Eccentricity
    "pl_eqt,pl_eqterr1,pl_eqterr2,"  # Equilibrium temperature
    "pl_insol,pl_insolerr1,pl_insolerr2,"  # Insolation flux
    # Stellar Properties
    "st_teff,st_tefferr1,st_tefferr2,"  # Star temperature
    "st_rad,st_raderr1,st_raderr2,"  # Star radius
    "st_mass,st_masserr1,st_masserr2,"  # Star mass
    "st_met,st_meterr1,st_meterr2,"  # Metallicity
    "st_logg,st_loggerr1,st_loggerr2,"  # Surface gravity
    "st_age,st_ageerr1,st_ageerr2,"  # Star age
    "st_lum,st_lumerr1,st_lumerr2,"  # Luminosity
    "st_spectype,"  # Spectral type
    # System Properties
    "sy_snum,sy_pnum,"  # Number of stars/planets
    "sy_dist,sy_disterr1,sy_disterr2,"  # Distance from Earth
    # Discovery Information
    "disc_year,disc_facility,discoverymethod,"
    # Sky Coordinates
    "ra,dec,"
    # Transit/Detection Data
    "tran_flag,"  # Has transit data
    # Classification
    "pl_controv_flag"  # Controversial/disputed
    "+from+ps"
    "&format=csv"
)

print("FETCH URL (truncated):", url[:150] + "...")

try:
    df = pd.read_csv(url)
    
    print("✅ Data fetched successfully!")
    print(f"\n📊 Dataset Statistics:")
    print(f"   Total exoplanets: {len(df)}")
    print(f"   Total columns: {len(df.columns)}")
    print(f"   Date range: {df['disc_year'].min():.0f} - {df['disc_year'].max():.0f}")
    
    # Show data completeness
    print(f"\n📈 Data Completeness:")
    key_cols = ['pl_rade', 'pl_masse', 'pl_dens', 'pl_eqt', 'st_teff', 'st_mass']
    for col in key_cols:
        if col in df.columns:
            completeness = (df[col].notna().sum() / len(df)) * 100
            print(f"   {col}: {completeness:.1f}%")
    
    print(f"\n🔭 Discovery Methods:")
    if 'discoverymethod' in df.columns:
        print(df['discoverymethod'].value_counts().head())
    
    print("\n📋 Sample Data:")
    display_cols = ['pl_name', 'pl_rade', 'pl_masse', 'pl_orbper', 'pl_eqt', 'st_teff', 'disc_year']
    available_display = [col for col in display_cols if col in df.columns]
    print(df[available_display].head(10))
    
    # Save to CSV
    df.to_csv("data/exoplanets.csv", index=False)
    print("\n📁 Saved to data/exoplanets.csv")
    
    # Create a summary report
    print("\n🎯 Potential Analysis Opportunities:")
    print("   1. Habitability Zone Analysis (pl_eqt, pl_insol, st_teff)")
    print("   2. Mass-Radius Relationships (pl_masse vs pl_rade)")
    print("   3. Density Classification (pl_dens → rocky, gas giant, ice giant)")
    print("   4. Orbital Dynamics (pl_orbeccen, pl_orbper)")
    print("   5. Host Star Correlations (st_met, st_age, st_mass)")
    print("   6. Discovery Method Biases (discoverymethod)")
    print("   7. Multi-planet System Architecture (sy_pnum)")
    print("   8. Distance/Detection Limits (sy_dist vs planet properties)")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTrying simplified query...")
    
    # Fallback query
    url_simple = (
        "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
        "?query=select+pl_name,pl_rade,pl_masse,pl_dens,pl_orbper,"
        "pl_eqt,st_teff,st_mass,sy_snum,sy_pnum,disc_year,discoverymethod"
        "+from+ps"
        "&format=csv"
    )
    
    df = pd.read_csv(url_simple)
    print("✅ Simplified data fetched successfully!")
    print(df.head())
    df.to_csv("data/exoplanets.csv", index=False)
    print("📁 Saved to data/exoplanets.csv")