
# ============================================================
# Fleet Incident & Telemetry Analytics Platform
# Script: generate_data.py
# Purpose: Generate synthetic fleet datasets
# ============================================================

from pathlib import Path
import pandas as pd
import numpy as np

# ------------------------------------------------------------
# 1. Project configuration
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Create output directory if it does not exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

print("Fleet Incident Analytics Platform")
print("----------------------------------")

# ------------------------------------------------------------
# 2. Plant catalog
# ------------------------------------------------------------

plants = [
    ["PLT-5101", "Monterrey Plant", "Northeast", "Mexico"],
    ["PLT-5176", "Santa Catarina Plant", "Northeast", "Mexico"],
    ["PLT-5203", "Saltillo Plant", "Northeast", "Mexico"],
    ["PLT-5288", "Ramos Arizpe Plant", "Northeast", "Mexico"],
    ["PLT-5355", "Torreon Plant", "North", "Mexico"],
    ["PLT-5402", "Chihuahua Plant", "North", "Mexico"],
    ["PLT-6104", "Dallas Plant", "South", "USA"],
    ["PLT-6207", "Houston Plant", "South", "USA"],
    ["PLT-6309", "Atlanta Plant", "Southeast", "USA"],
    ["PLT-6412", "Miami Plant", "Southeast", "USA"]
]

plant_columns = [
    "Plant_ID",
    "Plant_Name",
    "Region",
    "Country"
]

df_plants = pd.DataFrame(
    plants,
    columns=plant_columns
)

# ------------------------------------------------------------
# 3. Export catalog
# ------------------------------------------------------------

output_file = RAW_DATA_DIR / "dim_plant.csv"

df_plants.to_csv(
    output_file,
    index=False,
    encoding="utf-8"
)

print(f"\nPlant catalog generated: {len(df_plants)} plants")
print(f"Saved to: {output_file}")

print("\nPlant catalog preview:")
print(df_plants.head())
