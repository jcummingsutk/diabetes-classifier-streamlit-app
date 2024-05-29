FROM continuumio/miniconda3
WORKDIR /app
COPY ./conda.yaml ./
RUN conda env create -f conda.yaml
COPY st_app st_app
SHELL ["conda", "run", "-n", "diabetes-classifier-streamlit-app", "/bin/bash", "-c"]
CMD ["conda", "run", "-n", "diabetes-classifier-streamlit-app", "python", "-m", "streamlit", "run", "st_app/main.py", "--server.port", "8000", "--server.address", "0.0.0.0"]