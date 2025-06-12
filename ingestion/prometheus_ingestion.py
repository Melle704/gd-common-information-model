import os
import re

__all__ = ['parse_prometheus_text', 'ingest_prometheus_file', 'ingest_prometheus_dir']

# Regex.
LINE_RE = re.compile(
    r'^(?P<name>[a-zA-Z_:][a-zA-Z0-9_:]*)'
    r'(?:\{(?P<labels>[^}]*)\})?\s+'
    r'(?P<value>[-+eE0-9\.]+)'
    r'(?:\s+(?P<timestamp>\d+))?$'
)
LABEL_RE = re.compile(r'(?P<key>\w+?)="(?P<val>(?:\\.|[^"])+)"')


def parse_prometheus_text(path):
    metrics = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            # Skip empty lines.
            if not line or line.startswith('#'):
                continue
            
            # Attempt to match metric line regex, else skip that line.
            m = LINE_RE.match(line)
            if not m:
                continue
            name = m.group('name')
            labels_str = m.group('labels') or ''
            labels = {}
            for part in labels_str.split(','):
                lm = LABEL_RE.match(part)
                if lm:
                    labels[lm.group('key')] = lm.group('val')
                    
            # Convert values to floats and timestamp to ints.
            value = float(m.group('value'))
            ts = m.group('timestamp')
            timestamp = int(ts) if ts else None
            
            # Store metrics under lowercase metric name.
            metrics.setdefault(name.lower(), []).append({'labels': labels, 'value': value, 'timestamp': timestamp})
    return metrics


def ingest_prometheus_file(path):
    # Use the base filename (without extension) as the key
    base = os.path.splitext(os.path.basename(path))[0]
    return {base: parse_prometheus_text(path)}


def ingest_prometheus_dir(dir_path):
    data = {}
    for fname in os.listdir(dir_path):
        if not fname.endswith('.txt'):
            continue
        data.update(ingest_prometheus_file(os.path.join(dir_path, fname)))
    return data