
from pathlib import Path
import pandas as pd
import numpy as np

# Project configuration
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Incident generation settings
NUM_INCIDENTS = 10_000

START_DATE = "2025-01-01"
END_DATE = "2025-12-31"

# Generate random incident dates
incident_dates = pd.to_datetime(
    np.random.choice(
        pd.date_range(start=START_DATE, end=END_DATE),
        size=NUM_INCIDENTS
    )
)


# Generate incident opening times
incident_hours = np.random.randint(0, 24, size=NUM_INCIDENTS)
incident_minutes = np.random.randint(0, 60, size=NUM_INCIDENTS)
incident_seconds = np.random.randint(0, 60, size=NUM_INCIDENTS)

opened_datetimes = (
    incident_dates
    + pd.to_timedelta(incident_hours, unit="h")
    + pd.to_timedelta(incident_minutes, unit="m")
    + pd.to_timedelta(incident_seconds, unit="s")
)


print("\nINCIDENT DATE GENERATION")
print("------------------------")
print(f"Generated dates: {len(incident_dates)}")
print(f"First date: {incident_dates.min()}")
print(f"Last date: {incident_dates.max()}")

print("\nINCIDENT GENERATION SETTINGS")
print("----------------------------")
print(f"Target incidents: {NUM_INCIDENTS:,}")
print(f"Start date: {START_DATE}")
print(f"End date: {END_DATE}")

# Load dimension tables
df_vehicles = pd.read_csv(RAW_DATA_DIR / "dim_vehicle.csv")
df_plants = pd.read_csv(RAW_DATA_DIR / "dim_plant.csv")
df_incident_types = pd.read_csv(RAW_DATA_DIR / "dim_incident_type.csv")
df_carriers = pd.read_csv(RAW_DATA_DIR / "dim_carrier.csv")
df_gps_providers = pd.read_csv(RAW_DATA_DIR / "dim_gps_provider.csv")
df_devices = pd.read_csv(RAW_DATA_DIR / "dim_device.csv")


# Assign vehicles to incidents

# Give PLT-5176 a higher probability of incident occurrence
vehicle_weights = np.where(
    df_vehicles["Plant_ID"] == "PLT-5176",
    3,
    1
)

vehicle_probabilities = vehicle_weights / vehicle_weights.sum()

# Randomly select vehicles with replacement
selected_vehicles = df_vehicles.iloc[
    np.random.choice(
        len(df_vehicles),
        size=NUM_INCIDENTS,
        replace=True,
        p=vehicle_probabilities
    )
].reset_index(drop=True)

# Keep vehicle and plant relationship
incident_vehicles = pd.DataFrame({
    "Vehicle_ID": selected_vehicles["Vehicle_ID"],
    "Plant_ID": selected_vehicles["Plant_ID"]
})

incident_vehicles["Opened_DateTime"] = opened_datetimes

print("\nINCIDENT OPENING DATETIME")
print("-------------------------")
print(incident_vehicles["Opened_DateTime"].head())

incident_vehicles["Opened_DateTime"] = opened_datetimes
print("\nVEHICLE AND PLANT ASSIGNMENT")
print("----------------------------")
print(f"Assigned incidents: {len(incident_vehicles)}")
print(f"Unique vehicles: {incident_vehicles['Vehicle_ID'].nunique()}")

print("\nIncidents by plant:")
print(incident_vehicles["Plant_ID"].value_counts().sort_index())


# Assign incident types

# Base probability for each incident type
base_type_probabilities = np.array([
    0.22,  # Communication
    0.18,  # GPS
    0.12,  # Sensor
    0.08,  # Tablet
    0.10,  # Authentication
    0.10,  # Synchronization
    0.06,  # Assignment
    0.06,  # Application
    0.04,  # Hardware
    0.04   # Carrier
])

incident_type_ids = []

for plant_id in incident_vehicles["Plant_ID"]:
    probabilities = base_type_probabilities.copy()

    # Increase Communication and GPS probability for PLT-5176
    if plant_id == "PLT-5176":
        probabilities[0] *= 1.8
        probabilities[1] *= 1.8

    # Normalize probabilities
    probabilities = probabilities / probabilities.sum()

    selected_type = np.random.choice(
        df_incident_types["Incident_Type_ID"],
        p=probabilities
    )

    incident_type_ids.append(selected_type)

# Store incident types
incident_vehicles["Incident_Type_ID"] = incident_type_ids


# Assign carriers to incidents

carrier_ids = df_carriers["Carrier_ID"].to_numpy()

assigned_carriers = []

for incident_type in incident_vehicles["Incident_Type_ID"]:

    # Communication incidents have higher probability of Carrier_A
    if incident_type == "IT-001":
        probabilities = [0.50, 0.20, 0.17, 0.13]

    else:
        probabilities = [0.25, 0.25, 0.25, 0.25]

    selected_carrier = np.random.choice(
        carrier_ids,
        p=probabilities
    )

    assigned_carriers.append(selected_carrier)

incident_vehicles["Carrier_ID"] = assigned_carriers


# Assign error codes to incidents

error_codes = [
    "CODE_17",
    "CODE_33",
    "CODE_50",
    "CODE_71",
    "CODE_82"
]

assigned_error_codes = []

for _, incident in incident_vehicles.iterrows():

    incident_type = incident["Incident_Type_ID"]
    carrier = incident["Carrier_ID"]

    # Communication + Carrier_A
    if incident_type == "IT-001" and carrier == "CAR-001":
        probabilities = [0.45, 0.10, 0.05, 0.25, 0.15]

    # Other Communication incidents
    elif incident_type == "IT-001":
        probabilities = [0.20, 0.10, 0.15, 0.15, 0.40]

    # GPS incidents
    elif incident_type == "IT-002":
        probabilities = [0.05, 0.05, 0.05, 0.10, 0.75]

    # Authentication incidents
    elif incident_type == "IT-005":
        probabilities = [0.10, 0.65, 0.10, 0.05, 0.10]

    # Synchronization incidents
    elif incident_type == "IT-006":
        probabilities = [0.05, 0.10, 0.65, 0.10, 0.10]

    # Other incident types
    else:
        probabilities = [0.15, 0.15, 0.20, 0.10, 0.40]

    selected_error = np.random.choice(
        error_codes,
        p=probabilities
    )

    assigned_error_codes.append(selected_error)

incident_vehicles["Error_Code"] = assigned_error_codes



# Assign GPS providers
gps_provider_ids = df_gps_providers["GPS_Provider_ID"].to_numpy()

incident_vehicles["GPS_Provider_ID"] = np.random.choice(
    gps_provider_ids,
    size=NUM_INCIDENTS
)

# Assign devices
device_ids = df_devices["Device_ID"].to_numpy()

incident_vehicles["Device_ID"] = np.random.choice(
    device_ids,
    size=NUM_INCIDENTS
)


# Assign incident severity
severity_levels = ["Low", "Medium", "High", "Critical"]

severity_probabilities = [0.15, 0.45, 0.30, 0.10]

incident_vehicles["Severity"] = np.random.choice(
    severity_levels,
    size=NUM_INCIDENTS,
    p=severity_probabilities
)


# Assign incident status
incident_statuses = ["Open", "In Progress", "Resolved", "Closed"]

status_probabilities = [0.05, 0.10, 0.55, 0.30]

incident_vehicles["Status"] = np.random.choice(
    incident_statuses,
    size=NUM_INCIDENTS,
    p=status_probabilities
)

# Generate incident resolution time based on error code

resolution_minutes = np.full(NUM_INCIDENTS, np.nan)

resolved_mask = incident_vehicles["Status"].isin(
    ["Resolved", "Closed"]
).to_numpy()

error_code_array = incident_vehicles["Error_Code"].to_numpy()

duration_ranges = {
    "CODE_17": (60, 361),
    "CODE_33": (30, 241),
    "CODE_50": (15, 181),
    "CODE_71": (240, 1441),
    "CODE_82": (30, 361)
}

for code, (min_minutes, max_minutes) in duration_ranges.items():

    mask = resolved_mask & (error_code_array == code)

    resolution_minutes[mask] = np.random.randint(
        min_minutes,
        max_minutes,
        size=mask.sum()
    )

incident_vehicles["Resolution_Minutes"] = resolution_minutes

# Generate incident resolution datetime

incident_vehicles["Resolved_DateTime"] = (
    incident_vehicles["Opened_DateTime"]
    + pd.to_timedelta(
        incident_vehicles["Resolution_Minutes"],
        unit="m"
    )
)

print("\nSTATUS ASSIGNMENT")
print("-----------------")
print(incident_vehicles["Status"].value_counts().sort_index())
print("\nSEVERITY ASSIGNMENT")
print("-------------------")
print(incident_vehicles["Severity"].value_counts().sort_index())


print("\nGPS PROVIDER ASSIGNMENT")
print("-----------------------")
print(incident_vehicles["GPS_Provider_ID"].value_counts().sort_index())
print("\nDEVICE ASSIGNMENT")
print("-----------------")
print(incident_vehicles["Device_ID"].value_counts().sort_index())


print("\nERROR CODE ASSIGNMENT")
print("---------------------")
print(f"Assigned error codes: {len(assigned_error_codes)}")


print("\nIncidents by error code:")
print(
    incident_vehicles["Error_Code"]
    .value_counts()
    .sort_index()
)

print("\nCOMMUNICATION + CARRIER_A ERROR ANALYSIS")
print("----------------------------------------")

print(
    incident_vehicles[
        (incident_vehicles["Incident_Type_ID"] == "IT-001") &
        (incident_vehicles["Carrier_ID"] == "CAR-001")
    ]["Error_Code"].value_counts().sort_index()    
)


print("\nCARRIER ASSIGNMENT")
print("------------------")
print(f"Assigned carriers: {len(assigned_carriers)}")

print("\nIncidents by carrier:")
print(
    incident_vehicles["Carrier_ID"]
    .value_counts()
    .sort_index()
)

print("\nCommunication incidents by carrier:")
print(
    incident_vehicles[
        incident_vehicles["Incident_Type_ID"] == "IT-001"
    ]["Carrier_ID"].value_counts().sort_index()
)


print("\nINCIDENT TYPE ASSIGNMENT")
print("------------------------")
print(f"Assigned incident types: {len(incident_type_ids)}")

print("\nIncidents by type:")
print(
    incident_vehicles["Incident_Type_ID"]
    .value_counts()
    .sort_index()
)

print("\nCommunication and GPS incidents at PLT-5176:")
print(
    incident_vehicles[
        (incident_vehicles["Plant_ID"] == "PLT-5176") &
        (incident_vehicles["Incident_Type_ID"].isin(["IT-001", "IT-002"]))
    ].shape[0]
)

# Display loaded records
print("DIMENSION TABLES LOADED SUCCESSFULLY")
print("-----------------------------------")

print(f"Vehicles: {len(df_vehicles)}")
print(f"Plants: {len(df_plants)}")
print(f"Incident Types: {len(df_incident_types)}")
print(f"Carriers: {len(df_carriers)}")
print(f"GPS Providers: {len(df_gps_providers)}")
print(f"Devices: {len(df_devices)}")
print("\nINCIDENT TYPE CATALOG")
print("\nCARRIER CATALOG")
print("---------------")
print(df_carriers.to_string(index=False))
print("---------------------")
print(df_incident_types.to_string(index=False))
# Resolution time validation

print("\nRESOLUTION TIME VALIDATION")
print("---------------------------")

print("\nAverage resolution time by error code:")
print(
    incident_vehicles
    .groupby("Error_Code")["Resolution_Minutes"]
    .mean()
    .round(1)
)

print("\nResolution status validation:")
print(
    incident_vehicles
    .groupby("Status")["Resolved_DateTime"]
    .count()
)
# Datetime consistency validation

invalid_dates = incident_vehicles[
    incident_vehicles["Resolved_DateTime"]
    < incident_vehicles["Opened_DateTime"]
]

print("\nDATETIME CONSISTENCY VALIDATION")
print("--------------------------------")
print("Invalid resolution dates:", len(invalid_dates))
# Final incident table preparation

incident_vehicles.insert(
    0,
    "Incident_ID",
    [f"INC-{i:05d}" for i in range(1, len(incident_vehicles) + 1)]
)

incident_vehicles["Incident_Date"] = (
    incident_vehicles["Opened_DateTime"].dt.date
)

incident_vehicles["Incident_Time"] = (
    incident_vehicles["Opened_DateTime"].dt.strftime("%H:%M:%S")
)

print("\nFACT INCIDENTS PREVIEW")
print("----------------------")

print("Total records:", len(incident_vehicles))
print("Total columns:", len(incident_vehicles.columns))

print("\nColumns:")
print(incident_vehicles.columns.tolist())

print("\nFirst 5 incidents:")
print(incident_vehicles.head())
# Save fact incidents table

output_file = RAW_DATA_DIR / "fact_incidents.csv"

incident_vehicles.to_csv(
    output_file,
    index=False
)

print("\nFACT INCIDENTS EXPORT")
print("---------------------")
print("File saved to:", output_file)
print("Records exported:", len(incident_vehicles))

# Exported data integrity validation

df_check = pd.read_csv(output_file)

print("\nEXPORTED DATA INTEGRITY VALIDATION")
print("----------------------------------")

print("Total records:", len(df_check))
print("Duplicate Incident_ID:", df_check["Incident_ID"].duplicated().sum())
print("Missing Incident_ID:", df_check["Incident_ID"].isna().sum())

print(
    "Open/In Progress with resolution date:",
    df_check.loc[
        df_check["Status"].isin(["Open", "In Progress"]),
        "Resolved_DateTime"
    ].notna().sum()
)

print(
    "Resolved/Closed without resolution date:",
    df_check.loc[
        df_check["Status"].isin(["Resolved", "Closed"]),
        "Resolved_DateTime"
    ].isna().sum()
)