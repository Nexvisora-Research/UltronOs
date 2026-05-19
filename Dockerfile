FROM ubuntu:noble

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Install only essential packages
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    git \
    cmake \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Create development user
RUN useradd -m -s /bin/bash developer && \
    echo "developer:ultron" | chpasswd && \
    adduser developer sudo && \
    echo "developer ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set working directory
WORKDIR /home/developer/ultron

# Keep the container running
CMD ["tail", "-f", "/dev/null"]