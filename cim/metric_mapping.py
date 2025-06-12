MAPPINGS = [
    # Energy Metrics (existing)
    {'pattern': 'datacenter_power_usage_watts', 'category': 'Energy_Metrics', 'field': 'total_energy_consumed_kwh', 'agg': 'sum', 'factor': 1e-3},
    {'pattern': 'datacenter_power_usage_watts', 'category': 'Energy_Metrics', 'field': 'cooling_peak_load_kw', 'agg': 'max', 'factor': 1e-3},
    {'pattern': 'datacenter_pue', 'category': 'Efficiency_Metrics', 'field': 'pue', 'agg': 'mean'},
    {'pattern': 'datacenter_ere', 'category': 'Efficiency_Metrics', 'field': 'ere', 'agg': 'mean'},
    {'pattern': 'datacenter_cer', 'category': 'Efficiency_Metrics', 'field': 'cer', 'agg': 'mean'},
    {'pattern': 'datacenter_cue', 'category': 'Carbon_Emission_Metrics', 'field': 'cue', 'agg': 'mean'},
    {'pattern': 'datacenter_gec', 'category': 'Carbon_Emission_Metrics', 'field': 'gec', 'agg': 'mean'},
    {'pattern': 'datacenter_total_co2_emissions_kg', 'category': 'Carbon_Emission_Metrics', 'field': 'total_co2_emissions_kg', 'agg': 'sum'},
    {'pattern': 'datacenter_water_usage_liters', 'category': 'Water_Usage_Metrics', 'field': 'total_water_consumption', 'agg': 'sum'},
    {'pattern': 'datacenter_water_reuse_liters', 'category': 'Water_Usage_Metrics', 'field': 'water_reuse', 'agg': 'sum'},
    {'pattern': 'datacenter_wue', 'category': 'Water_Usage_Metrics', 'field': 'wue', 'agg': 'mean'},
    # Temperature (convert fahrenheit to celsius if detected)
    {'pattern': 'datacenter_temperature_celsius', 'category': 'Efficiency_Metrics', 'field': 'temperature_avg_celsius', 'agg': 'mean'},
    {'pattern': 'datacenter_temperature_fahrenheit', 'category': 'Efficiency_Metrics', 'field': 'temperature_avg_celsius', 'agg': 'mean', 'convert': 'f2c'},
    # Lifecycle Metrics
    {'pattern': 'datacenter_equipment_age_years', 'category': 'Lifecycle_Metrics', 'field': 'equipment_age', 'agg': 'mean'},
    {'pattern': 'datacenter_sustainability_rating', 'category': 'Lifecycle_Metrics', 'field': 'sustainability_rating', 'agg': 'mean'},
    {'pattern': 'datacenter_embedded_carbon_footprint_kg', 'category': 'Lifecycle_Metrics', 'field': 'embedded_carbon_footprint', 'agg': 'mean'},
    # Data Movement
    {'pattern': 'datacenter_carbon_per_gb', 'category': 'Data_Movement_Metrics', 'field': 'carbon_per_gb', 'agg': 'mean'},
    {'pattern': 'datacenter_inter_site_transfers_gb', 'category': 'Data_Movement_Metrics', 'field': 'inter_site_transfers', 'agg': 'sum'},
    {'pattern': 'node_network', 'category': 'Data_Movement_Metrics', 'field': 'data_volume_transferred', 'agg': 'sum', 'factor': 1e-9},
    # Resource Utilisation
    {'pattern': 'node_cpu_seconds_total', 'category': 'Resource_Utilisation_Metrics', 'field': 'cpu_utilization_percent', 'agg': 'timestamp_ratio'},
    {'pattern': 'node_cpu_usage_percent', 'category': 'Resource_Utilisation_Metrics', 'field': 'cpu_utilization_percent', 'agg': 'mean'},
    {'pattern': 'node_memory_memtotal_bytes', 'category': 'Resource_Utilisation_Metrics', 'field': 'memory_total_gb', 'agg': 'mean', 'factor': 1e-9},
    {'pattern': 'node_memory_active_bytes', 'category': 'Resource_Utilisation_Metrics', 'field': 'memory_avg_used_gb', 'agg': 'mean', 'factor': 1e-9},
    {'pattern': 'storage_node_capacity_bytes', 'category': 'Resource_Utilisation_Metrics', 'field': 'storage_total_tb', 'agg': 'sum', 'factor': 1e-12},
    {'pattern': 'node_disk_iops', 'category': 'Resource_Utilisation_Metrics', 'field': 'storage_iops', 'agg': 'mean'},
    {'pattern': 'datacenter_network_efficiency', 'category': 'Resource_Utilisation_Metrics', 'field': 'network_efficiency', 'agg': 'mean'},

    # Environmental Metrics
    {'pattern': 'datacenter_humidity_percent', 'category': 'Environmental_Metrics', 'field': 'humidity_avg_percent', 'agg': 'mean'},
    {'pattern': 'datacenter_fan_speed_rpm', 'category': 'Environmental_Metrics', 'field': 'fan_speed_avg_rpm', 'agg': 'mean'},
    {'pattern': 'dc_humidity', 'category': 'Environmental_Metrics', 'field': 'humidity_avg_percent', 'agg': 'mean'},

    # GPU Utilization
    {'pattern': 'gpu_utilization_percent', 'category': 'Resource_Utilisation_Metrics', 'field': 'gpu_utilization_percent', 'agg': 'mean'},

    # DC-specific Metrics (ap-south & us-west)
    {'pattern': 'dc_temp_c', 'category': 'Efficiency_Metrics', 'field': 'temperature_avg_celsius', 'agg': 'mean'},
    {'pattern': 'dc_power_w', 'category': 'Energy_Metrics', 'field': 'total_energy_consumed_kwh', 'agg': 'sum', 'factor': 1e-3},
    {'pattern': 'dc_pue', 'category': 'Efficiency_Metrics', 'field': 'pue', 'agg': 'mean'},
    {'pattern': 'dc_ere', 'category': 'Efficiency_Metrics', 'field': 'ere', 'agg': 'mean'},
    {'pattern': 'dc_cer', 'category': 'Efficiency_Metrics', 'field': 'cer', 'agg': 'mean'},
    {'pattern': 'dc_cue', 'category': 'Carbon_Emission_Metrics', 'field': 'cue', 'agg': 'mean'},
    {'pattern': 'dc_network_eff', 'category': 'Resource_Utilisation_Metrics', 'field': 'network_efficiency', 'agg': 'mean'},
    {'pattern': 'dc_inter_site_gb', 'category': 'Data_Movement_Metrics', 'field': 'inter_site_transfers', 'agg': 'sum'},
    {'pattern': 'dc_total_co2_kg', 'category': 'Carbon_Emission_Metrics', 'field': 'total_co2_emissions_kg', 'agg': 'sum'},
    {'pattern': 'dc_water_liters', 'category': 'Water_Usage_Metrics', 'field': 'total_water_consumption', 'agg': 'sum'},

    # US/EU West DataCenter metric aliases
    {'pattern': 'datacenter_temp_celsius', 'category': 'Efficiency_Metrics', 'field': 'temperature_avg_celsius', 'agg': 'mean'},
    {'pattern': 'datacenter_power_watts', 'category': 'Energy_Metrics', 'field': 'total_energy_consumed_kwh', 'agg': 'sum', 'factor': 1e-3},
    {'pattern': 'datacenter_power_watts', 'category': 'Energy_Metrics', 'field': 'cooling_peak_load_kw', 'agg': 'max', 'factor': 1e-3},
    # Storage Node Health
    {'pattern': 'storage_node_status', 'category': 'Storage_Metrics', 'field': 'storage_health', 'agg': 'mean'},

    # Additional Node Resource Utilisation
    {'pattern': 'node_cpu_usage', 'category': 'Resource_Utilisation_Metrics', 'field': 'cpu_utilization_percent', 'agg': 'mean'},
    {'pattern': 'node_memory_free_bytes', 'category': 'Resource_Utilisation_Metrics', 'field': 'memory_free_gb', 'agg': 'mean', 'factor': 1e-9},
    {'pattern': 'node_disk_read_ops_total', 'category': 'Resource_Utilisation_Metrics', 'field': 'disk_read_ops', 'agg': 'sum'},
    {'pattern': 'node_disk_write_ops_total', 'category': 'Resource_Utilisation_Metrics', 'field': 'disk_write_ops', 'agg': 'sum'},
    {'pattern': 'node_disk_read_bytes_total', 'category': 'Resource_Utilisation_Metrics', 'field': 'disk_read_bytes_gb', 'agg': 'sum', 'factor': 1e-9},
    {'pattern': 'node_disk_write_bytes_total', 'category': 'Resource_Utilisation_Metrics', 'field': 'disk_write_bytes_gb', 'agg': 'sum', 'factor': 1e-9},
    {'pattern': 'load_avg_1', 'category': 'Resource_Utilisation_Metrics', 'field': 'load_avg_1', 'agg': 'mean'},

    # Kubernetes
    {'pattern': 'kubernetes_pods_running', 'category': 'Orchestration_Metrics', 'field': 'pods_running', 'agg': 'sum'},

    # Service Metrics
    {'pattern': 'service_http_requests_total', 'category': 'Service_Metrics', 'field': 'http_requests_total', 'agg': 'sum'},
    {'pattern': 'api_requests_total', 'category': 'Service_Metrics', 'field': 'api_requests_total', 'agg': 'sum'},
    {'pattern': 'api_gateway_requests_total', 'category': 'Service_Metrics', 'field': 'api_gateway_requests_total', 'agg': 'sum'},
    {'pattern': 'load_balancer_http_requests_total', 'category': 'Service_Metrics', 'field': 'load_balancer_requests_total', 'agg': 'sum'},
    {'pattern': 'service_latency_seconds_sum', 'category': 'Service_Metrics', 'field': 'avg_latency_seconds', 'agg': 'ratio', 'denominator_pattern': 'service_latency_seconds_count'},

    # Database Metrics
    {'pattern': 'database_queries_total', 'category': 'Database_Metrics', 'field': 'db_queries_total', 'agg': 'sum'},
    {'pattern': 'database_connection_pool_active', 'category': 'Database_Metrics', 'field': 'db_connections_active', 'agg': 'mean'},
    {'pattern': 'db_conn_active', 'category': 'Database_Metrics', 'field': 'db_connections_active', 'agg': 'mean'},

    # Etcd
    {'pattern': 'etcd_server_has_leader', 'category': 'Orchestration_Metrics', 'field': 'etcd_leader_present', 'agg': 'mean'},
]
