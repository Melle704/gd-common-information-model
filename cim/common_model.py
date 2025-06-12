import copy
from cim.model_template import TEMPLATE
from cim.metric_mapping import MAPPINGS


def fill_common_model(raw_data):
    """
    Populate the TEMPLATE using metric patterns defined in metric_mappings.py,
    handling values, lists (Prometheus samples), nested dicts, and converters.
    """
    model = copy.deepcopy(TEMPLATE)

    # Ensure the categories exist in the model.
    for m in MAPPINGS:
        model['metrics_summary'].setdefault(m['category'], {})

    # Flatten single-key wrappers
    flat = {}
    for dc, vals in raw_data.items():
        if isinstance(vals, dict) and len(vals) == 1 and isinstance(list(vals.values())[0], dict):
            flat[dc] = list(vals.values())[0]
        else:
            flat[dc] = vals

    # Collect metrics with name, value and timestamp.
    items = []
    for v in flat.values():
        if isinstance(v, dict):
            for k, val in v.items():
                key = k.lower()
                if isinstance(val, list):  # Prometheus samples
                    for sample in val:
                        items.append((key, sample['value'], sample.get('timestamp')))
                elif isinstance(val, dict):  # nested unified
                    for subk, subv in val.items():
                        if isinstance(subv, (int, float)):
                            items.append((subk.lower(), subv, None))
                elif isinstance(val, (int, float)):
                    items.append((key, val, None))

    # Apply the mappings to matching metrics.
    for m in MAPPINGS:
        vals = []
        for key, val, ts in items:
            if m['pattern'] in key:
                # Convert metrics between units specified in the mappings.
                v = val
                if m.get('convert') == 'f2c':
                    v = (v - 32) * 5.0 / 9.0
                if 'factor' in m:
                    v = v * m['factor']
                vals.append((v, ts))

        # Skip metrics with no data found.
        if not vals:
            continue

        # Compute aggregates.
        if m['agg'] == 'sum':
            result = sum(v for v, _ in vals)
        elif m['agg'] == 'max':
            result = max(v for v, _ in vals)
        elif m['agg'] == 'mean':
            result = sum(v for v, _ in vals) / len(vals)
        elif m['agg'] == 'ratio':
            num = sum(v for v, _ in vals)
            den = sum(v2 for k2, v2, _ in items if m.get('denominator_pattern') and m['denominator_pattern'] in k2)
            result = (num / den) if den else None
        elif m['agg'] == 'timestamp_ratio':
            num = sum(v for v, _ in vals)
            ts = vals[0][1]
            result = (num / ts) if ts else None
        else:
            result = None

        # Assign to the model.
        model['metrics_summary'][m['category']][m['field']] = result

    return model
