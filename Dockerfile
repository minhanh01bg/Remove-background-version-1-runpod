# Dockerfile

# Stage 1: Build dependencies
# Base image with Python 3.10.6
# FROM python:3.10.6
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# RUN apt-get update && apt-get install -y \
#     git \
#     wget \
#     && rm -rf /var/lib/apt/lists/*

# Install CUDA (if you're using GPU)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy the application files (including models directory)
COPY . /app

# Copy requirements files for BiRefNet and LAMA
COPY requirements_birefnet.txt /app/requirements_birefnet.txt

# Install PyTorch and related packages for GPU with CUDA 12.1
RUN pip install --no-cache-dir torch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 --index-url https://download.pytorch.org/whl/cu121
# Install BiRefNet dependencies
RUN pip install --no-cache-dir -r requirements_birefnet.txt
# Install Runpod
RUN pip install --no-cache-dir runpod

# Preload the BiRefNet model from Hugging Face during the build
RUN python -c "from models.birefnet import BiRefNet; BiRefNet.from_pretrained('ZhengPeng7/BiRefNet')"

# Stage 2: Final minimal image
# FROM python:3.10-slim

# WORKDIR /app

# Copy only necessary files from the build stage
# COPY --from=builder /app /app

CMD ["python", "-u", "main.py"]
