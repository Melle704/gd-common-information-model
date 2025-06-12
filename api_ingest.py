"""
api_ingest.py: A REST API wrapper for Prometheus ingestion CLI and JSON-LD querying.
Run with: uvicorn api_ingest:app --host 0.0.0.0 --port 8000
"""

import os
import uuid
import shutil
import subprocess
import re
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, Response

app = FastAPI()

# Output directories.
temp_dir = os.path.join(os.getcwd(), "temp_uploads")
output_dir = os.path.join(os.getcwd(), "crate_output")

@app.post("/ingest/", response_class=FileResponse)
async def ingest_prometheus(file: UploadFile = File(...)):
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Save upload in temp_dir.
    unique_name = f"{uuid.uuid4()}_{file.filename}"
    input_path = os.path.join(temp_dir, unique_name)
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    before = set(os.listdir(output_dir))

    # Run the ingestion.
    cmd = ["python", "run_ingestion.py", "--input", input_path]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")

    # Detect the new output file.
    after = set(os.listdir(output_dir))
    new_files = after - before
    if not new_files:
        raise HTTPException(status_code=500, detail="Output file not found")

    # Choose newest version if multiple exist.
    if len(new_files) > 1:
        new_paths = [os.path.join(output_dir, f) for f in new_files]
        new_paths.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        output_path = new_paths[0]
    else:
        output_path = os.path.join(output_dir, new_files.pop())

    return FileResponse(path=output_path, media_type="application/ld+json", filename=os.path.basename(output_path))

@app.post("/query/")
async def query_jsonld(query: str = Form(...)):
    if not os.path.isdir(output_dir):
        raise HTTPException(status_code=500, detail="Output directory not found")

    # Clean up windows escape carets if present.
    cleaned = query.replace('^<', '<').replace('^>', '>')

    # Format SPARQL query: place each PREFIX on its own line.
    formatted = re.sub(r"(PREFIX\s+\w+:\s+<[^>]+>)", r"\1\n", cleaned)

    # Construct command to run query_jsonld.py.
    cmd = [
        "python",
        "query_jsonld.py",
        output_dir,
        "--query",
        formatted
    ]
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.strip() if e.stderr else str(e)
        raise HTTPException(status_code=500, detail=f"Query failed: {stderr}")

    # Return the raw output.
    return Response(content=result.stdout, media_type="application/json")
