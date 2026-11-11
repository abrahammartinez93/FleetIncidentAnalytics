
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

# ------------------------------------------------------------
# 4. Incident type catalog
# ------------------------------------------------------------

incident_types = [
    ["IT-001", "Communication", "Connectivity"],
    ["IT-002", "GPS", "Tracking"],
    ["IT-003", "Sensor", "Hardware"],
    ["IT-004", "Tablet", "Hardware"],
    ["IT-005", "Authentication", "Application"],
    ["IT-006", "Synchronization", "Data"],
    ["IT-007", "Assignment", "Operations"],
    ["IT-008", "Application", "Software"],
    ["IT-009", "Hardware", "Hardware"],
    ["IT-010", "Carrier", "Connectivity"]
]

incident_columns = [
    "Incident_Type_ID",
    "Incident_Type",
    "Incident_Category"
]

df_incident_types = pd.DataFrame(
    incident_types,
    columns=incident_columns
)

# ------------------------------------------------------------
# 5. Export incident type catalog
# ------------------------------------------------------------

output_file = RAW_DATA_DIR / "dim_incident_type.csv"

df_incident_types.to_csv(
    output_file,
    index=False,
    encoding="utf-8"
)

print(f"\nIncident type catalog generated: {len(df_incident_types)} types")
print(f"Saved to: {output_file}")

print("\nIncident type catalog preview:")
print(df_incident_types.to_string(index=False))


# ------------------------------------------------------------
# 6. Carrier catalog
# ------------------------------------------------------------

carriers = [
    ["CAR-001", "Carrier_A"],
    ["CAR-002", "Carrier_B"],
    ["CAR-003", "Carrier_C"],
    ["CAR-004", "Carrier_D"]
]

carrier_columns = [
    "Carrier_ID",
    "Carrier_Name"
]

df_carriers = pd.DataFrame(
    carriers,
    columns=carrier_columns
)

# ------------------------------------------------------------
# 7. Export carrier catalog
# ------------------------------------------------------------

output_file = RAW_DATA_DIR / "dim_carrier.csv"

df_carriers.to_csv(
    output_file,
    index=False,
    encoding="utf-8"
)

print(f"\nCarrier catalog generated: {len(df_carriers)} carriers")
print(f"Saved to: {output_file}")

print("\nCarrier catalog preview:")
print(df_carriers.to_string(index=False))


# ------------------------------------------------------------
# 8. GPS provider catalog
# ------------------------------------------------------------

gps_providers = [
    ["GPS-001", "Provider_A"],
    ["GPS-002", "Provider_B"],
    ["GPS-003", "Provider_C"]
]

gps_columns = [
    "GPS_Provider_ID",
    "GPS_Provider_Name"
]

df_gps_providers = pd.DataFrame(
    gps_providers,
    columns=gps_columns
)

# ------------------------------------------------------------
# 9. Export GPS provider catalog
# ------------------------------------------------------------

output_file = RAW_DATA_DIR / "dim_gps_provider.csv"

df_gps_providers.to_csv(
    output_file,
    index=False,
    encoding="utf-8"
)

print(f"\nGPS provider catalog generated: {len(df_gps_providers)} providers")
print(f"Saved to: {output_file}")

print("\nGPS provider catalog preview:")
print(df_gps_providers.to_string(index=False))



# ------------------------------------------------------------
# 10. Device catalog
# ------------------------------------------------------------

devices = [
    ["DEV-001", "Tracker_X"],
    ["DEV-002", "Tracker_Y"],
    ["DEV-003", "Tracker_Z"]
]

device_columns = [
    "Device_ID",
    "Device_Type"
]

df_devices = pd.DataFrame(
    devices,
    columns=device_columns
)

# ------------------------------------------------------------
# 11. Export device catalog
# ------------------------------------------------------------

output_file = RAW_DATA_DIR / "dim_device.csv"

df_devices.to_csv(
    output_file,
    index=False,
    encoding="utf-8"
)

print(f"\nDevice catalog generated: {len(df_devices)} devices")
print(f"Saved to: {output_file}")

print("\nDevice catalog preview:")
print(df_devices.to_string(index=False))



# ------------------------------------------------------------
# 12. Vehicle catalog
# ------------------------------------------------------------

NUMBER_OF_VEHICLES = 500

vehicle_ids = [
    f"TRK-{number}"
    for number in range(10001, 10001 + NUMBER_OF_VEHICLES)
]

truck_plates = np.arange(10000001, 10000001 + NUMBER_OF_VEHICLES)

vehicle_types = [
    "Concrete Mixer",
    "Transit Mixer",
    "Heavy Duty Mixer"
]

vehicle_models = [
    "Model_A",
    "Model_B",
    "Model_C",
    "Model_D"
]

df_vehicles = pd.DataFrame({
    "Vehicle_ID": vehicle_ids,
    "TruckPlate": truck_plates,
    "Plant_ID": np.random.choice(
        df_plants["Plant_ID"],
        size=NUMBER_OF_VEHICLES
    ),
    "Vehicle_Type": np.random.choice(
        vehicle_types,
        size=NUMBER_OF_VEHICLES
    ),
    "Vehicle_Model": np.random.choice(
        vehicle_models,
        size=NUMBER_OF_VEHICLES
    ),
    "Model_Year": np.random.randint(
        2015,
        2027,
        size=NUMBER_OF_VEHICLES
    ),
    "Is_Active": np.random.choice(
        [True, False],
        size=NUMBER_OF_VEHICLES,
        p=[0.95, 0.05]
    )
})

# ------------------------------------------------------------
# 13. Export vehicle catalog
# ------------------------------------------------------------

output_file = RAW_DATA_DIR / "dim_vehicle.csv"

df_vehicles.to_csv(
    output_file,
    index=False,
    encoding="utf-8"
)

print(f"\nVehicle catalog generated: {len(df_vehicles)} vehicles")
print(f"Saved to: {output_file}")

print("\nVehicle catalog preview:")
print(df_vehicles.head(10).to_string(index=False))

print("\nVehicles by plant:")
print(
    df_vehicles.groupby("Plant_ID")
    .size()
    .sort_values(ascending=False)
)



# ------------------------------------------------------------
# 14. Data quality validation
# ------------------------------------------------------------

print("\n===================================")
print("DATA QUALITY VALIDATION")
print("===================================")

catalogs = {
    "dim_plant": (df_plants, "Plant_ID", 10),
    "dim_incident_type": (df_incident_types, "Incident_Type_ID", 10),
    "dim_carrier": (df_carriers, "Carrier_ID", 4),
    "dim_gps_provider": (df_gps_providers, "GPS_Provider_ID", 3),
    "dim_device": (df_devices, "Device_ID", 3),
    "dim_vehicle": (df_vehicles, "Vehicle_ID", 500)
}

for name, (df, key, expected) in catalogs.items():

    actual = len(df)
    duplicates = df[key].duplicated().sum()

    print(f"\n{name}")
    print(f"Expected records: {expected}")
    print(f"Actual records: {actual}")
    print(f"Duplicate IDs: {duplicates}")

    if actual == expected and duplicates == 0:
        print("Validation: PASSED")
    else:
        print("Validation: FAILED")

# Validate vehicle-to-plant relationships

invalid_plants = ~df_vehicles["Plant_ID"].isin(
    df_plants["Plant_ID"]
)

print("\nVehicle-Plant relationship")
print(f"Invalid plant references: {invalid_plants.sum()}")

if invalid_plants.sum() == 0:
    print("Relationship validation: PASSED")
else:
    print("Relationship validation: FAILED")

print("\n===================================")
print("DATA QUALITY VALIDATION COMPLETED")
print("===================================")


