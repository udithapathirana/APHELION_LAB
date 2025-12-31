import pandas as pd

print("Starting NASA Exoplanet fetch (REST API)...")

# TAP
url = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    "?query=select+pl_name,pl_rade,pl_orbper,sy_snum,sy_pnum,disc_year"
    "+from+ps+where+pl_rade+is+not+null"
    "&format=csv"
)

print("FETCH URL:", url)

try:
    df = pd.read_csv(url)
    
    # Check if we got an error message instead of data
    if 'ERROR' in df.columns or len(df.columns) == 1:
        print("❌ API returned an error. Trying alternative method...")
        
        # Alternative:  simpler PSCompPars table equivalent
        url_alt = (
            "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
            "?query=select+pl_name,pl_rade,pl_orbper,disc_year"
            "+from+pscomppars"
            "&format=csv"
        )
        
        print("Alternative URL:", url_alt)
        df = pd.read_csv(url_alt)
    
    print("✅ Data fetched successfully!")
    print(f"Total exoplanets: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print("\nFirst few rows:")
    print(df.head())
    
    df.to_csv("data/exoplanets.csv", index=False)
    print("\n📁 Saved to data/exoplanets.csv")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTrying direct download without query...")
    
    # Fallback: Simple query
    url_simple = (
        "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
        "?query=select+*+from+ps+where+rownum<100"
        "&format=csv"
    )
    
    df = pd.read_csv(url_simple)
    print("Available columns:", list(df.columns)[:20])  #first 20 columns