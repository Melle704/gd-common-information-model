@echo off

REM 1. create venv
if not exist venv (
    py -m venv venv
)
call venv\Scripts\activate

REM 3. install requirements
pip install -r requirements.txt

REM 4. launch fastapi server
py -m uvicorn api_ingest:app --reload --host 0.0.0.0 --port 8000
