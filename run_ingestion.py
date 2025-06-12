import argparse
import os
import json
import pprint

from ingestion.unified_ingestion import ingest_all, ingest_file
from cim.common_model         import fill_common_model
from cim.context              import CONTEXT

RO_CRATE_FILENAME = "ro-crate-metadata.json"


# Placeholder ro_crate.
def build_ro_crate_manifest(output_dir, jsonld_files):
    return {
        "@context": "https://w3id.org/ro/crate/1.1/context",
        "@id":      "./",
        "@type":    "Dataset",
        "name":     "Data Center Metrics Summary Crate",
        "hasPart": [
            {"@id": f"./{fname}", "@type": "File", "encodingFormat": "application/ld+json"}
            for fname in jsonld_files
        ]
    }


def main():
    parser = argparse.ArgumentParser(
        description="Ingest data, map to CIM, export as JSON-LD in an RO-Crate"
    )
    parser.add_argument(
        "-i", "--input", required=True,
        help="Path to a file or directory to ingest"
    )
    parser.add_argument(
        "-o", "--outdir", default="crate_output",
        help="Directory to write the RO-Crate"
    )
    args = parser.parse_args()

    input_path = args.input
    crate_dir  = args.outdir
    os.makedirs(crate_dir, exist_ok=True)

    # Ingest raw data.
    if os.path.isdir(input_path):
        raw = ingest_all(input_path)
    elif os.path.isfile(input_path):
        raw = ingest_file(input_path)
    else:
        raise FileNotFoundError(f"No such file or directory: {input_path}")

    jsonld_files = []

    # Map each dataset, fill out the CIM and generate the output file.
    for base, vals in raw.items():
        model = fill_common_model({base: vals})
        jsonld = {
            "@context": CONTEXT,
            "@id":      f"urn:metrics:{base}",
            "@type":    "MetricsSummary",
            **model
        }
        fname = f"{base}.jsonld"
        out_path = os.path.join(crate_dir, fname)
        with open(out_path, "w") as f:
            json.dump(jsonld, f, indent=2)
        jsonld_files.append(fname)
        pprint.pprint(jsonld)

    # Build and write RO-Crate metadata.
    crate_manifest = build_ro_crate_manifest(crate_dir, jsonld_files)
    manifest_path = os.path.join(crate_dir, RO_CRATE_FILENAME)
    with open(manifest_path, "w") as f:
        json.dump(crate_manifest, f, indent=2)

    print(f"RO-Crate written to {crate_dir}")


if __name__ == "__main__":
    main()