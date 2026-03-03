# CoPaw Installation Guide

This guide covers all installation methods for CoPaw, from quick one-click setup to enterprise deployments.

---

## Table of Contents

- [System Requirements](#system-requirements)
- [Method 1: One-Click Installation](#method-1-one-click-installation)
- [Method 2: pip Installation](#method-2-pip-installation)
- [Method 3: Docker Deployment](#method-3-docker-deployment)
- [Method 4: Cloud Deployment](#method-4-cloud-deployment)
- [Local Model Integration](#local-model-integration)
- [Post-Installation Setup](#post-installation-setup)

---

## System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **Python** | 3.10 or higher |
| **RAM** | 8GB (16GB recommended for local models) |
| **Storage** | 2GB free space |
| **OS** | macOS, Linux, or Windows |

### Recommended for Local Models

| Component | Recommendation |
|-----------|----------------|
| **RAM** | 16GB or more |
| **GPU** | Dedicated GPU (Windows) or Apple Silicon (M1/M2/M3/M4) |
| **Storage** | 10GB+ for model files |

---

## Method 1: One-Click Installation

**Best for:** General users who want the fastest setup

### macOS / Linux

```bash
curl -fsSL https://copaw.agentscope.io/install.sh | bash
```

### Windows (PowerShell)

```powershell
irm https://copaw.agentscope.io/install.ps1 | iex
```

### After Installation

```bash
# Initialize CoPaw
copaw init

# Start the application
copaw app
```

Access the web console at: **http://127.0.0.1:8088/**

---

## Method 2: pip Installation

**Best for:** Developers who want full control

### Prerequisites

Ensure Python 3.10+ is installed:

```bash
python3 --version
```

### Installation Steps

```bash
# Install CoPaw
pip install copaw

# Initialize with defaults
copaw init --defaults

# Start the application
copaw app
```

### Verify Installation

```bash
# Check CoPaw version
copaw --version

# List available commands
copaw --help
```

---

## Method 3: Docker Deployment

**Best for:** Enterprise and production environments

### Prerequisites

- Docker installed and running
- Docker Compose (optional, for advanced setups)

### Quick Start

```bash
# Pull the latest image
docker pull agentscope/copaw:latest

# Run CoPaw with persistent storage
docker run -d \
  -p 8088:8088 \
  -v copaw-data:/app/working \
  --name copaw \
  agentscope/copaw:latest
```

### Docker Compose

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  copaw:
    image: agentscope/copaw:latest
    container_name: copaw
    ports:
      - "8088:8088"
    volumes:
      - copaw-data:/app/working
    environment:
      - DASHSCOPE_API_KEY=${DASHSCOPE_API_KEY:-}
    restart: unless-stopped

volumes:
  copaw-data:
```

Run with:

```bash
docker-compose up -d
```

### Managing Docker Deployment

```bash
# View logs
docker logs -f copaw

# Stop CoPaw
docker stop copaw

# Restart CoPaw
docker restart copaw

# Remove deployment
docker rm -f copaw && docker volume rm copaw-data
```

---

## Method 4: Cloud Deployment

### ModelScope Studio

1. Visit [ModelScope Studio](https://modelscope.cn)
2. Search for "CoPaw" template
3. Click "One-Click Deploy"
4. **Important:** Set space visibility to **Private** for security

### Alibaba Cloud ECS

1. Visit the [CoPaw ECS deployment link](https://cs.console.aliyun.com/#/copaw)
2. Follow the prompts to configure your instance
3. Deploy with one click

### Security Considerations

- Always set cloud deployments to **Private**
- Never expose API keys in public spaces
- Use environment variables for sensitive data
- Enable firewall rules to restrict access

---

## Local Model Integration

**Recommended for:** Privacy-focused users and offline operation

### MLX Backend (Apple Silicon)

For M1/M2/M3/M4 Macs:

```bash
# During installation
bash install.sh --extras mlx

# Or after installation
pip install copaw[mlx]
```

### llama.cpp Backend (Cross-Platform)

```bash
# During installation
bash install.sh --extras llamacpp

# Or after installation
pip install copaw[llamacpp]
```

### Download Local Models

```bash
# Download a model
copaw models download Qwen/Qwen3-4B-GGUF

# List available models
copaw models

# Start CoPaw in offline mode
copaw app
```

### Supported Model Formats

| Format | Backend | Platform |
|--------|---------|----------|
| **GGUF** | llama.cpp | All platforms |
| **MLX** | MLX | Apple Silicon |
| **ONNX** | ONNX Runtime | All platforms |

---

## Post-Installation Setup

### 1. Initialize Configuration

```bash
copaw init
```

This interactive command will:
- Create configuration files
- Set up the working directory
- Prompt for API keys (optional)

### 2. Configure API Keys (Optional)

If using cloud LLMs:

```bash
# Method 1: Interactive setup
copaw init

# Method 2: Environment variable
export DASHSCOPE_API_KEY=your_api_key_here

# Method 3: .env file
echo "DASHSCOPE_API_KEY=your_api_key_here" >> .env
```

### 3. Verify Installation

Open your browser and navigate to:

```
http://127.0.0.1:8088/
```

You should see the CoPaw web console.

### 4. Test Basic Functionality

In the web console:
1. Navigate to the chat interface
2. Send a test message
3. Verify the response

---

## Troubleshooting Installation

### Common Issues

#### Python Version Error

```
Error: Python 3.10+ is required
```

**Solution:** Upgrade Python:

```bash
# Using pyenv
pyenv install 3.11.0
pyenv global 3.11.0

# Or download from python.org
```

#### Permission Denied (macOS/Linux)

```
Permission denied: /usr/local/bin/copaw
```

**Solution:**

```bash
# Install with user permissions
pip install --user copaw

# Or use sudo (not recommended)
sudo pip install copaw
```

#### Port Already in Use

```
Error: Port 8088 is already in use
```

**Solution:**

```bash
# Find and kill the process
lsof -i :8088
kill -9 <PID>

# Or use a different port
copaw app --port 8089
```

#### Docker Volume Issues

```
Error: Volume mount failed
```

**Solution:**

```bash
# Create volume manually
docker volume create copaw-data

# Check Docker permissions
docker info
```

---

## Next Steps

- [Configuration Guide](../configuration/README.md) - Set up models and channels
- [Architecture Overview](../architecture/README.md) - Understand CoPaw's structure
- [Skills Development](../skills/README.md) - Create custom skills

---

*Last updated: March 2026*
