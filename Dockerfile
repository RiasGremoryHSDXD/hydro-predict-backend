# Use a lightweight Python image that matches your local version (3.12)
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed for some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements first to leverage Docker caching
COPY requirements.txt .

# Install your specific library versions
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your backend files (main.py, pkl files)
COPY . .

# Render uses port 10000 by default for Web Services
EXPOSE 10000

# Start the FastAPI server using the same command you used locally (py -m uvicorn)
# We map it to 0.0.0.0 so it's accessible outside the container
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]