#!/bin/bash

# Get the absolute path of the project root
PROJECT_ROOT=$(pwd)

# Add src to PYTHONPATH
export PYTHONPATH=$PROJECT_ROOT:$PYTHONPATH

# Start the FastAPI backend
cd $PROJECT_ROOT
uvicorn business_plan_creator.backend:app --reload --port 8000 &

# Wait for the backend to start
sleep 2

# Start the Streamlit frontend
streamlit run frontend.py 