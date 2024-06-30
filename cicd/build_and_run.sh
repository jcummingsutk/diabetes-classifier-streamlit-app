#!/bin/bash
docker build -t diabetes-classifier-streamlit-app ./ && docker run -p 8000:8000 diabetes-classifier-streamlit-app:latest