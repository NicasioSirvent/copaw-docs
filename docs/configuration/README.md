# CoPaw Configuration Guide

This guide covers all configuration aspects of CoPaw, including model setup, channel integration, and environment settings.

---

## Table of Contents

- [Configuration Overview](#configuration-overview)
- [Model Configuration](#model-configuration)
- [Channel Configuration](#channel-configuration)
- [Memory Settings](#memory-settings)
- [Environment Variables](#environment-variables)
- [Advanced Configuration](#advanced-configuration)

---

## Configuration Overview

CoPaw uses a flexible configuration system that supports:

- **Interactive CLI setup** via `copaw init`
- **Web console** configuration at `http://127.0.0.1:8088/`
- **Environment variables** for Docker and cloud deployments
- **Configuration files** in the working directory

### Configuration Files Location

| Platform | Location |
|----------|----------|
| **macOS/Linux** | `~/.copaw/config.yaml` |
| **Windows** | `%USERPROFILE%\.copaw\config.yaml` |
| **Docker** | `/app/working/config.yaml` |

---

## Model Configuration

### Cloud LLM Configuration

#### Using DashScope (Qwen Models)

**Method 1: CLI Setup**

```bash
copaw init
```

Follow the prompts to enter your API key.

**Method 2: Web Console**

1. Open `http://127.0.0.1:8088/`
2. Navigate to **Settings → Model**
3. Select "DashScope" as provider
4. Enter your API key
5. Click "Save"

**Method 3: Environment Variable**

```bash
export DASHSCOPE_API_KEY=your_api_key_here
```

Or in `.env` file:

```env
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxx
```

**Method 4: Configuration File**

Edit `~/.copaw/config.yaml`:

```yaml
models:
  default:
    provider: dashscope
    api_key: sk-xxxxxxxxxxxxxxxx
    model_name: qwen-max
```

#### Supported Cloud Providers

| Provider | Environment Variable | Models |
|----------|---------------------|--------|
| **DashScope** | `DASHSCOPE_API_KEY` | Qwen series |
| **OpenAI** | `OPENAI_API_KEY` | GPT-4, GPT-3.5 |
| **Anthropic** | `ANTHROPIC_API_KEY` | Claude series |

### Local Model Configuration

#### MLX Backend (Apple Silicon)

1. Install MLX support:

```bash
pip install copaw[mlx]
```

2. Download a model:

```bash
copaw models download Qwen/Qwen3-4B-GGUF
```

3. Configure in `config.yaml`:

```yaml
models:
  local:
    provider: mlx
    model_path: ~/.copaw/models/Qwen3-4B-GGUF
    backend: mlx
```

#### llama.cpp Backend (Cross-Platform)

1. Install llama.cpp support:

```bash
pip install copaw[llamacpp]
```

2. Download a GGUF model:

```bash
copaw models download Qwen/Qwen2.5-7B-Instruct-GGUF
```

3. Configure in `config.yaml`:

```yaml
models:
  local:
    provider: llamacpp
    model_path: ~/.copaw/models/Qwen2.5-7B-Instruct.Q4_K_M.gguf
    n_ctx: 4096
    n_threads: 8
```

#### Model Configuration Options

```yaml
models:
  # Default model for general tasks
  default:
    provider: dashscope
    model_name: qwen-max
    temperature: 0.7
    max_tokens: 2048
  
  # Fast model for quick responses
  fast:
    provider: dashscope
    model_name: qwen-turbo
    temperature: 0.5
  
  # Local model for privacy
  local:
    provider: llamacpp
    model_path: ~/.copaw/models/model.gguf
    n_ctx: 8192
    n_gpu_layers: 0  # Set >0 for GPU acceleration
```

---

## Channel Configuration

CoPaw supports multiple communication channels. Each channel requires specific credentials.

### DingTalk Configuration

1. **Create a Bot Application**
   - Visit [DingTalk Developer Console](https://open-dev.dingtalk.com/)
   - Create a new application
   - Select "Chat Bot" type

2. **Get Credentials**
   - Obtain `AppKey` and `AppSecret`
   - Configure webhook URL (if needed)

3. **Configure in CoPaw**
   - Open web console: `http://127.0.0.1:8088/`
   - Navigate to **Settings → Channels**
   - Select "DingTalk"
   - Enter AppKey and AppSecret
   - Click "Save"

4. **Test**
   - Add the bot to a DingTalk group
   - Use `@CoPaw` to interact

### Lark (Feishu) Configuration

1. **Create Application**
   - Visit [Lark Developer Platform](https://open.feishu.cn/)
   - Create a new app
   - Enable "Bot" capability

2. **Get Credentials**
   - App ID
   - App Secret
   - Verification Token

3. **Configure in CoPaw**

```yaml
channels:
  lark:
    enabled: true
    app_id: cli_xxxxxxxxxxxxx
    app_secret: xxxxxxxxxxxxxxx
    verification_token: xxxxxxxxxxxxxxx
```

### Discord Configuration

1. **Create Discord Application**
   - Visit [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to "Bot" section
   - Create bot and copy token

2. **Get Bot Token**
   - Copy the bot token
   - Enable required intents (Message Content, etc.)

3. **Configure in CoPaw**

```yaml
channels:
  discord:
    enabled: true
    bot_token: xxxxxxxxxxxxxxx
    intents:
      - message_content
      - messages
```

4. **Invite Bot to Server**
   - Generate OAuth2 URL with `bot` scope
   - Invite to your server

### QQ Configuration

1. **Setup QQ Bot**
   - Use QQ Open Platform
   - Create bot application
   - Get AppID and AppKey

2. **Configure**

```yaml
channels:
  qq:
    enabled: true
    app_id: xxxxxxxxxxxxxxx
    app_key: xxxxxxxxxxxxxxx
```

### iMessage Configuration

**Note:** iMessage integration requires additional setup due to Apple's restrictions.

```yaml
channels:
  imessage:
    enabled: true
    account: your_apple_id@example.com
    # Additional configuration may be required
```

---

## Memory Settings

CoPaw uses ReMe (Persistent Memory) for long-term context retention.

### Memory Configuration

```yaml
memory:
  # Storage type: local or cloud
  type: local
  
  # Local storage path
  path: ~/.copaw/memory
  
  # Memory format
  format: jsonl+md
  
  # Enable semantic search
  semantic_search: true
  
  # Maximum memory entries
  max_entries: 10000
  
  # Auto-cleanup old entries
  cleanup:
    enabled: true
    days: 30
```

### Memory Locations

| Type | Path |
|------|------|
| **Local** | `~/.copaw/memory/` |
| **Docker** | `/app/working/memory/` |
| **Cloud** | Configured via cloud provider |

### Memory Backup

```bash
# Export memory
copaw memory export backup.jsonl

# Import memory
copaw memory import backup.jsonl
```

---

## Environment Variables

### Core Variables

```env
# API Keys
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-xxxxxxxxxxxxxxxx

# CoPaw Settings
COPAW_PORT=8088
COPAW_HOST=127.0.0.1
COPAW_WORKING_DIR=~/.copaw

# Memory Settings
COPAW_MEMORY_PATH=~/.copaw/memory
COPAW_MEMORY_TYPE=local

# Logging
COPAW_LOG_LEVEL=info
COPAW_LOG_FILE=~/.copaw/copaw.log
```

### Docker Environment

```yaml
# docker-compose.yml
services:
  copaw:
    environment:
      - DASHSCOPE_API_KEY=${DASHSCOPE_API_KEY}
      - COPAW_PORT=8088
      - COPAW_LOG_LEVEL=info
```

---

## Advanced Configuration

### Multi-Model Routing

Configure different models for different tasks:

```yaml
models:
  routing:
    # Use fast model for simple queries
    simple_queries:
      model: qwen-turbo
      max_tokens: 512
    
    # Use powerful model for complex tasks
    complex_tasks:
      model: qwen-max
      max_tokens: 4096
    
    # Use local model for sensitive data
    sensitive_data:
      model: local
      provider: llamacpp
```

### Custom Skills Path

```yaml
skills:
  # Additional skills directories
  paths:
    - ~/.copaw/skills
    - ~/my-copaw-skills
  
  # Auto-load skills on startup
  auto_load: true
  
  # Community skills hub
  hub_url: https://skills.sh
```

### Agent Configuration

```yaml
agents:
  # Default agent settings
  default:
    name: CoPaw
    personality: helpful
    language: en
  
  # Custom agents
  custom:
    - name: Research Assistant
      model: qwen-max
      skills:
        - web_search
        - summarization
    
    - name: Code Helper
      model: qwen-coder
      skills:
        - code_analysis
        - debugging
```

### Network Configuration

```yaml
network:
  # Proxy settings
  proxy:
    http: http://proxy.example.com:8080
    https: http://proxy.example.com:8080
  
  # Timeout settings
  timeout:
    request: 30
    connection: 10
  
  # Retry settings
  retry:
    max_attempts: 3
    backoff: exponential
```

---

## Configuration Validation

### Check Configuration

```bash
# Validate config file
copaw config validate

# Show current configuration
copaw config show

# Test model connection
copaw config test-model

# Test channel connection
copaw config test-channel dingtalk
```

### Reset Configuration

```bash
# Reset to defaults
copaw init --reset

# Clear all settings
copaw config clear
```

---

## Troubleshooting Configuration

### Common Issues

#### API Key Not Working

**Symptoms:** Authentication errors, 401 responses

**Solutions:**
1. Verify API key is correct
2. Check key hasn't expired
3. Ensure sufficient quota/credits
4. Test with: `copaw config test-model`

#### Channel Not Connecting

**Symptoms:** No responses in chat platforms

**Solutions:**
1. Verify credentials in developer console
2. Check webhook URLs are accessible
3. Ensure bot permissions are correct
4. Test with: `copaw config test-channel <channel>`

#### Memory Issues

**Symptoms:** Context not persisting, memory errors

**Solutions:**
1. Check memory directory permissions
2. Verify disk space
3. Clear corrupted memory: `copaw memory clear`
4. Check config: `copaw config show memory`

---

## Next Steps

- [Architecture Overview](../architecture/README.md) - Understand CoPaw's structure
- [Skills Development](../skills/README.md) - Create custom skills
- [Use Cases](../use-cases/README.md) - Real-world examples

---

*Last updated: March 2026*
