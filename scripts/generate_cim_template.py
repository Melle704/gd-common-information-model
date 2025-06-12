"""
Generate the common information model template with placeholder values
in the exact structure provided.
"""

import json
import re
from collections import OrderedDict

# Load and categorize flat metrics.
with open('../metrics_definitions.json') as f:
    metrics = json.load(f)
categories_order = [
    "Energy_Metrics",
    "Efficiency_Metrics",
    "Carbon_Emission_Metrics",
    "Water_Usage_Metrics",
    "Resource_Utilisation_Metrics",
    "Lifecycle_Metrics",
    "Data_Movement_Metrics"
]

# Map each metricID in the CIM.
category_map = {
    # Energy_Metrics
    "iso30134:TotalEnergyConsumedKWh": "Energy_Metrics",
    "iso30134:DailyEnergyConsumedKWh": "Energy_Metrics",
    "iso30134:EnergyReuseFactor":       "Energy_Metrics",
    "en50600:CoolingPeakLoadKw":        "Energy_Metrics",

    # Efficiency_Metrics
    "iso30134:PUE": "Efficiency_Metrics",
    "iso30134:ERE": "Efficiency_Metrics",
    "iso30134:CER": "Efficiency_Metrics",

    # Carbon_Emission_Metrics
    "iso30134:CUE":                 "Carbon_Emission_Metrics",
    "jrc:GEC":                      "Carbon_Emission_Metrics",
    "jrc:TotalCo2EmissionsKg":      "Carbon_Emission_Metrics",

    # Water_Usage_Metrics
    "iso30134:WUE":                 "Water_Usage_Metrics",
    "iso30134:TotalWaterConsumption": "Water_Usage_Metrics",
    "iso30134:WaterReuse":            "Water_Usage_Metrics",

    # Resource_Utilisation_Metrics
    "iso30134:CPUUtilizationPercent":    "Resource_Utilisation_Metrics",
    "iso30134:ServerUtilizationPercent": "Resource_Utilisation_Metrics",
    "egi:MemoryTotalGB":                 "Resource_Utilisation_Metrics",
    "egi:MemoryAvgUsedGB":               "Resource_Utilisation_Metrics",
    "egi:StorageTotalTB":                "Resource_Utilisation_Metrics",
    "egi:StorageAvgUsedTB":              "Resource_Utilisation_Metrics",
    "egi:StorageIOPS":                   "Resource_Utilisation_Metrics",
    "egi:NetworkEfficiency":             "Resource_Utilisation_Metrics",

    # Lifecycle_Metrics
    "jrc:EquipmentAge":                 "Lifecycle_Metrics",
    "jrc:SustainabilityRating":         "Lifecycle_Metrics",
    "jrc:EmbeddedCarbonFootprint":      "Lifecycle_Metrics",

    # Data_Movement_Metrics
    "jrc:DataVolumeTransferred": "Data_Movement_Metrics",
    "jrc:CarbonPerGB":           "Data_Movement_Metrics",
    "jrc:InterSiteTransfers":    "Data_Movement_Metrics",
}

# Convert camelcase to snakecase.
def camel_to_snake(name):
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

# Template dict.
template = {
    "metrics_summary": OrderedDict(
        (cat, OrderedDict()) for cat in categories_order
    )
}

for m in metrics:
    mid = m["metricID"]
    cat = category_map.get(mid)
    if not cat:
        continue
    local = mid.split(":", 1)[1]
    key = camel_to_snake(local)
    template["metrics_summary"][cat][key] = None

print('"""\nDefine the common information model template with placeholder values in the exact structure provided.\n"""\n')
print("TEMPLATE = " + json.dumps(template, indent=2))
