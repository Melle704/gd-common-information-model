# Program guide: Common Information Model for the European GreenDIGIT project

A command-line and API tool to ingest Prometheus-style telemetry data from datacenters, convert it into a Common Information Model (CIM) JSON-LD representation, and run SPARQL queries against it, using RDFLib.

This is the public version of the repo.

---

## 1. Overview

#### 2. List of metrics  

#### 3. Command-Line Interface (without API)

#### 4. Setting up the API server.

#### 5. Using the API

#### 6. File structure

---

## 2. List of all Metrics
The definitions of all the metrics and the standards they are derived from, can be found in the metric_definitons.json file.

To add new metrics to the Common Information Model, add them manually in the metric_definitons.json file and run scripts/generate_cim_template.py to generate the new template. After that you need to add them to the cim/metric_mapping.py pattern list, with how the metric should be handled by the framework.

**Energy_Metrics**  
- `total_energy_consumed_kwh`  
- `daily_energy_consumed_kwh`  
- `energy_reuse_factor`  
- `cooling_peak_load_kw`  

**Efficiency_Metrics**  
- `pue` (Power Usage Effectiveness)  
- `ere` (Energy Reuse Effectiveness)  
- `cer` (Cooling Efficiency Ratio)  

**Carbon_Emission_Metrics**  
- `cue` (Carbon Usage Effectiveness)  
- `gec` (Grid Emissions Coefficient)  
- `total_co2_emissions_kg`  

**Water_Usage_Metrics**  
- `wue` (Water Usage Effectiveness)  
- `total_water_consumption`  
- `water_reuse`  

**Resource_Utilisation_Metrics**  
- `cpu_utilization_percent`  
- `server_utilization_percent`  
- `memory_total_gb`  
- `memory_avg_used_gb`  
- `storage_total_tb`  
- `storage_avg_used_tb`  
- `storage_iops`  
- `network_efficiency`  

**Lifecycle_Metrics**  
- `equipment_age`  
- `sustainability_rating`  
- `embedded_carbon_footprint`  

**Data_Movement_Metrics**  
- `data_volume_transferred`  
- `carbon_per_gb`  
- `inter_site_transfers`  

---

## 3. Command-Line Interface (without API)

### 3.1 Ingest Prometheus Data  
```bash
py run_ingestion.py \
  --input sample_data/prometheus/datacenter-4.txt
```
- input: Path to the Prometheus-format text file.
- Output: A JSON-LD file is written to the crate_output/ directory.

### 3.2 Query the CIM graph
```bash
py query_jsonld.py crate_output \
  --query "PREFIX ex: <http://example.org/metrics#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> \ 
  SELECT (STR(?entry) AS ?id) WHERE { ?entry ex:metrics_summary/ex:Energy_Metrics/ex:total_energy_consumed_kwh ?energy . FILTER(xsd:decimal(?energy)>40) }"
```
This looks intimidating at first, but it is just a python command, some needed prefix definitions and then the sparql query. This particular example query returns the @id's of all the datacenters with a total power consumption in kwh over 40.

---

## 4. Setting up the API server.
The api server can be setup using the start_api.bat script in the scripts directory, or using the following command line input.

#### 1. Create a python virtual environment in ./venv.
py -m venv venv

#### 2. Activate it.
venv\Scripts\activate

#### 3. Install all dependencies from requirements.txt.
py -m pip install -r requirements.txt

#### 4. Launch the FastAPI server (for local use).
py -m uvicorn api_ingest:app --reload --host 0.0.0.0 --port 8000

### Non-local usage

To host the server for lan/wan use, the ip in the last step can be changed to your lan ip-address. Other systems on the same lan can then make api requests using your lan ip-address:8000. For outside network API request, you also need to port forward port 8000 to your local ip-address, and systems can connect using your public ip-address.

---

## 5. Using the API

### Query using the API
```bash
curl -X POST "http://localhost:8000/ingest/" \
        -F "file=@sample_data/prometheus/datacenter-4.txt" \
        -o output.jsonld 
```
- -F "file=@…": Sends the Prometheus file as multipart/form-data.
- -o output.jsonld: Writes the returned JSON-LD to output.jsonld.

### Query using the API
```bash
curl.exe -X POST "http://localhost:8000/query/" \
         -F "query=PREFIX ex: ^<http://example.org/metrics#^> PREFIX xsd: ^<http://www.w3.org/2001/XMLSchema#^> \
         SELECT (STR(?entry) AS ?id) WHERE { ?entry ex:metrics_summary/ex:Energy_Metrics/ex:total_energy_consumed_kwh ?energy . FILTER(xsd:decimal(?energy)>40) }"
```
Same format as before but instead of python we use a curl command with the ip-address and port, again some needed prefix definitions, and the SPARQL query.

RDFLib is required on Windows 11, else you will get a error.

---

## 6. File structure
```bash
├── metric_definitions.json
├── requirements.txt
├── run_ingestion.py
├── query_jsonld.py
├── api_ingest.py
├── cim
│   ├── common_model.py
│   ├── context.py
│   ├── metric_mapping.py
│   └── model_template.py
├── crate_output
│   ├── ro-crate-metadata.json
│   └── *.jsonld
├── ingestion
│   ├── prometheus_ingestion.py
│   └── unified_ingestion.py
├── sample_data
│   ├── prometheus
|   |   ├── datacenter-4.txt
|   |   └── ...
│   └── simple-formats
|       ├── datacenter_A.json
|       └── ...
└── scripts
    ├── generate_cim_template.py
    └── start_api.bat
```
