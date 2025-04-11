# Use Python base image
FROM python:3.12-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt /app/

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Set the port and expose it
ENV PORT=8501
EXPOSE $PORT

# Run the Streamlit app
CMD ["bash", "-c", "streamlit run app.py --server.port=$PORT --server.headless=true"]
