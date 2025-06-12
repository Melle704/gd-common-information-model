"""
A simple CLI for loading all JSON-LD files in a directory into an RDF graph and querying them with SPARQL.
"""
import argparse
import os
import rdflib


def load_jsonld_files(directory: str, graph: rdflib.Graph = None) -> rdflib.Graph:
    """
    Recursively parse all .jsonld files in the given directory into the RDFLib graph.
    """
    if graph is None:
        graph = rdflib.Graph()
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jsonld', '.json', '.json-ld')):
                path = os.path.join(root, file)
                print(f"Parsing {path}...", end=' ')
                try:
                    graph.parse(path, format='json-ld')
                    count += 1
                    print("OK")
                except Exception as e:
                    print(f"Failed: {e}")
    print(f"Loaded {count} JSON-LD files into graph ({len(graph)} triples)")
    return graph


def main():
    parser = argparse.ArgumentParser(
        description="Load JSON-LD files and query via SPARQL."
    )
    parser.add_argument(
        'directory',
        help="Directory containing JSON-LD files"
    )
    parser.add_argument(
        '-q', '--query',
        help="SPARQL query to execute (wrap in quotes)",
        default=None
    )
    args = parser.parse_args()

    g = load_jsonld_files(args.directory)

    if args.query:
        print("Running query...\n")
        try:
            results = g.query(args.query)
            for row in results:
                print(row)
        except Exception as e:
            print(f"Query error: {e}")
    else:
        print("\nEntering interactive SPARQL shell. Type 'exit' or 'quit' to leave.")
        while True:
            inp = input("SPARQL> ")
            if inp.strip().lower() in ('exit', 'quit'):
                break
            if not inp.strip():
                continue
            try:
                results = g.query(inp)
                for row in results:
                    print(row)
            except Exception as e:
                print(f"Query error: {e}")


if __name__ == '__main__':
    main()