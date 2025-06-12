import os
import json
import csv
import re
import xml.etree.ElementTree as ET
from .prometheus_ingestion import parse_prometheus_text

__all__ = ['ingest_all', 'ingest_file']

# All simple parser implementations.

def parse_json(path):
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, dict) and len(data) == 1 and isinstance(list(data.values())[0], dict):
        return list(data.values())[0]
    return data


def parse_yaml(path):
    with open(path) as f:
        raw = yaml.safe_load(f)
    sys = raw.get('system', {})
    return {
        'cpu': sys.get('cpu'),
        'mem': sys.get('memory', {}).get('usage'),
        'net_in': sys.get('network', {}).get('in'),
        'net_out': sys.get('network', {}).get('out'),
    }


def parse_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return {
        'cpu':             float(root.findtext('compute/cpu') or 0),
        'mem':             float(root.findtext('hardware/memory/used') or 0),
        'energy_kwh':      float(root.findtext('elec/power') or 0),
        'energy_renewable':float(root.findtext('power/solar') or 0),
        'net_in':          float(root.findtext('network/incoming') or 0),
        'net_out':         float(root.findtext('network/outgoing') or 0),
        'storage_read':    float(root.findtext('disk/readIO') or 0),
        'storage_write':   float(root.findtext('disk/writeIO') or 0),
        'temp_int':        float(root.findtext('env/internalTemp') or 0),
        'temp_ext':        float(root.findtext('env/externalTemp') or 0),
    }


def parse_csv(path):
    with open(path) as f:
        reader = csv.DictReader(f)
        row = next(reader)
    return {k: float(v) for k, v in row.items()}


def parse_txt(path):
    text = open(path).read()
    def find(pattern):
        m = re.search(pattern, text, re.IGNORECASE)
        return float(m.group(1)) if m else None

    return {
        'cpu':     find(r'CPU.*?([\d.]+)%'),
        'mem':     find(r'Memory.*?([\d.]+)\s*GB'),
        'power_w': find(r'(?:Power draw|PowerDraw):\s*([\d.]+)W'),
        'net_in':  find(r'(?:Incoming net|network in):\s*([\d.]+)'),
        'net_out': find(r'(?:Outgoing net|network out):\s*([\d.]+)'),
        'temp':    find(r'Temp.*?([\d.]+)°?C'),
    }

# Extension to parser map.
_PARSERS = {
    '.json': parse_json,
    '.yaml': parse_yaml,
    '.yml':  parse_yaml,
    '.xml':  parse_xml,
    '.csv':  parse_csv,
    '.txt':  parse_txt,
}


def ingest_file(path):
    base, ext = os.path.splitext(os.path.basename(path))
    ext = ext.lower()
    # Try to detect Prometheus text format.
    if ext == '.txt':
        with open(path) as f:
            first = f.read(8)
        if first.lstrip().startswith('# HELP'):
            return {base: parse_prometheus_text(path)}
        # Fallback to unstructured TXT.
        return {base: parse_txt(path)}

    parser = _PARSERS.get(ext)
    if not parser:
        raise ValueError(f"Unsupported file type: {ext}")
    return {base: parser(path)}


def ingest_all(data_dir):
    data = {}
    for fname in os.listdir(data_dir):
        base, ext = os.path.splitext(fname)
        ext = ext.lower()
        path = os.path.join(data_dir, fname)
        try:
            if ext == '.txt':
                # Parse Prometheus or unstructured.
                data.update(ingest_file(path))
                continue
            parser = _PARSERS.get(ext)
            if not parser:
                continue
            data[base] = parser(path)
        except Exception as e:
            print(f"Failed to parse {fname}: {e}")
    return data