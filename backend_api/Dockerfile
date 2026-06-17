# 1. Start with an official, lightweight Python base image running on Linux
FROM python:3.12-slim

# 2. Set the working directory inside the container's isolated file system
WORKDIR /workspace

# 3. Environment variables: prevent Python from writing .pyc files and buffer logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Copy just the requirements file first to take advantage of Docker caching layers
COPY requirements.txt .

# 5. Install the Python packages inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy your entire local 'app' directory (including main.py and your 6GB model weights)
COPY ./app ./app

# 7. Expose port 8000 so your laptop can communicate with the container
EXPOSE 8000

# 8. Command to execute when the container starts up
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]