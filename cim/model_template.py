"""
Define the common information model template to be filled in.
"""

TEMPLATE = {
  "metrics_summary": {
    "Energy_Metrics": {
      "total_energy_consumed_kwh": None,
      "daily_energy_consumed_kwh": None,
      "energy_reuse_factor": None,
      "cooling_peak_load_kw": None
    },
    "Efficiency_Metrics": {
      "pue": None,
      "ere": None,
      "cer": None
    },
    "Carbon_Emission_Metrics": {
      "cue": None,
      "gec": None,
      "total_co2_emissions_kg": None
    },
    "Water_Usage_Metrics": {
      "wue": None,
      "total_water_consumption": None,
      "water_reuse": None
    },
    "Resource_Utilisation_Metrics": {
      "cpu_utilization_percent": None,
      "server_utilization_percent": None,
      "memory_total_gb": None,
      "memory_avg_used_gb": None,
      "storage_total_tb": None,
      "storage_avg_used_tb": None,
      "storage_iops": None,
      "network_efficiency": None
    },
    "Lifecycle_Metrics": {
      "equipment_age": None,
      "sustainability_rating": None,
      "embedded_carbon_footprint": None
    },
    "Data_Movement_Metrics": {
      "data_volume_transferred": None,
      "carbon_per_gb": None,
      "inter_site_transfers": None
    }
  }
}