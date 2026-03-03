# CoPaw FAQ & Troubleshooting

Common questions, issues, and solutions for CoPaw.

---

## Table of Contents

- [General FAQ](#general-faq)
- [Installation Issues](#installation-issues)
- [Configuration Issues](#configuration-issues)
- [Model Issues](#model-issues)
- [Channel Issues](#channel-issues)
- [Skills Issues](#skills-issues)
- [Memory Issues](#memory-issues)
- [Performance Issues](#performance-issues)

---

## General FAQ

### What is CoPaw?

CoPaw (Co Personal Agent Workstation) is a high-performance personal AI agent workstation open-sourced by Alibaba. It's designed to streamline the deployment and management of personal AI agents across multiple channels.

### Is CoPaw free?

Yes, CoPaw is open-source under the Apache 2.0 license. You can use it freely for personal and commercial purposes.

### What platforms does CoPaw support?

CoPaw supports:
- **Operating Systems:** macOS, Linux, Windows
- **Chat Platforms:** DingTalk, Lark (Feishu), QQ, Discord, iMessage

### What AI models does CoPaw support?

CoPaw supports:
- **Cloud Models:** Qwen series (via DashScope), OpenAI GPT, Anthropic Claude
- **Local Models:** GGUF format (via llama.cpp), MLX format (Apple Silicon)

### Is my data private?

CoPaw is designed with privacy in mind:
- Local model support means no data leaves your machine
- Memory is stored locally by default
- You control your API keys and data

### Can I use CoPaw offline?

Yes! With local model support (MLX or llama.cpp), CoPaw can run completely offline.

### How do I update CoPaw?

```bash
# pip installation
pip install --upgrade copaw

# One-click installation
curl -fsSL https://copaw.agentscope.io/install.sh | bash
```

### Where can I get help?

- **Documentation:** This repository
- **GitHub Issues:** [agentscope-ai/CoPaw/issues](https://github.com/agentscope-ai/CoPaw/issues)
- **Community:** Skills hubs and forums

---

## Installation Issues

### Python Version Error

**Error:**
```
Error: Python 3.10+ is required, found Python 3.9
```

**Solution:**

Upgrade Python:

```bash
# Using pyenv (recommended)
pyenv install 3.11.0
pyenv global 3.11.0

# Verify
python3 --version  # Should show 3.11.0
```

Or download from [python.org](https://www.python.org/downloads/).

---

### Permission Denied (macOS/Linux)

**Error:**
```
Permission denied: /usr/local/bin/copaw
ERROR: Can't write to /usr/local/bin
```

**Solution 1: Install with user permissions**
```bash
pip install --user copaw
```

**Solution 2: Use sudo (not recommended)**
```bash
sudo pip install copaw
```

**Solution 3: Fix permissions**
```bash
sudo chown -R $(whoami) /usr/local/bin
```

---

### Installation Fails on Windows

**Error:**
```
ERROR: Could not find a version that satisfies the requirement copaw
```

**Solution:**

1. **Run PowerShell as Administrator**

2. **Enable script execution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. **Install Visual C++ Build Tools:**
   - Download from: [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - Install "Desktop development with C++"

4. **Retry installation:**
```powershell
irm https://copaw.agentscope.io/install.ps1 | iex
```

---

### Docker Installation Fails

**Error:**
```
ERROR: Cannot connect to the Docker daemon
```

**Solution:**

```bash
# Start Docker service
sudo systemctl start docker

# Enable Docker on boot
sudo systemctl enable docker

# Add user to docker group (avoid sudo)
sudo usermod -aG docker $USER
# Log out and back in
```

---

### Port Already in Use

**Error:**
```
Error: Port 8088 is already in use
OSError: [Errno 48] Address already in use
```

**Solution 1: Find and kill the process**

macOS/Linux:
```bash
lsof -i :8088
kill -9 <PID>
```

Windows:
```powershell
netstat -ano | findstr :8088
taskkill /PID <PID> /F
```

**Solution 2: Use a different port**
```bash
copaw app --port 8089
```

---

## Configuration Issues

### API Key Not Working

**Error:**
```
AuthenticationError: Invalid API key
401 Unauthorized
```

**Solution:**

1. **Verify API key format:**
   - DashScope keys start with `sk-`
   - OpenAI keys start with `sk-`
   - Check for typos

2. **Check key status:**
   - Log into your provider dashboard
   - Ensure the key is active
   - Check quota/credits

3. **Test the key:**
```bash
copaw config test-model
```

4. **Re-enter the key:**
```bash
copaw init --reset
```

---

### Configuration File Not Found

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: '~/.copaw/config.yaml'
```

**Solution:**

```bash
# Initialize configuration
copaw init

# Or create manually
mkdir -p ~/.copaw
touch ~/.copaw/config.yaml
```

---

### Environment Variables Not Loading

**Issue:** Environment variables set but not recognized.

**Solution:**

1. **Check variable is set:**
```bash
echo $DASHSCOPE_API_KEY
```

2. **Export properly:**
```bash
export DASHSCOPE_API_KEY=sk-xxxxxxxx
```

3. **Add to shell profile:**
```bash
# ~/.bashrc or ~/.zshrc
export DASHSCOPE_API_KEY=sk-xxxxxxxx
source ~/.bashrc  # or source ~/.zshrc
```

4. **For Docker, use .env file:**
```env
# .env
DASHSCOPE_API_KEY=sk-xxxxxxxx
```

---

## Model Issues

### Model Response Too Slow

**Issue:** Responses take a long time.

**Solutions:**

1. **Use a faster model:**
```yaml
models:
  default:
    provider: dashscope
    model_name: qwen-turbo  # Faster than qwen-max
```

2. **Reduce max tokens:**
```yaml
models:
  default:
    max_tokens: 1024  # Instead of 4096
```

3. **For local models, use quantization:**
```bash
# Download quantized model
copaw models download Qwen/Qwen2.5-7B-Instruct-GGUF-q4
```

---

### Local Model Out of Memory

**Error:**
```
RuntimeError: CUDA out of memory
Not enough memory to load model
```

**Solutions:**

1. **Use a smaller model:**
```bash
copaw models download Qwen/Qwen2.5-1.5B-Instruct-GGUF
```

2. **Use quantization:**
```bash
# Q4 quantization (smaller)
copaw models download Qwen/Qwen2.5-7B-Instruct-GGUF-q4
```

3. **Reduce context size:**
```yaml
models:
  local:
    n_ctx: 2048  # Instead of 8192
```

4. **Use CPU (slower but works):**
```yaml
models:
  local:
    n_gpu_layers: 0
```

---

### Model Returns Gibberish

**Issue:** Model output is nonsensical.

**Solutions:**

1. **Check model format:**
   - Ensure GGUF for llama.cpp
   - Ensure MLX for Apple Silicon

2. **Adjust temperature:**
```yaml
models:
  default:
    temperature: 0.7  # Lower = more focused
```

3. **Try a different model:**
```bash
copaw models download Qwen/Qwen2.5-7B-Instruct-GGUF
```

---

## Channel Issues

### DingTalk Bot Not Responding

**Issue:** Bot doesn't respond to messages.

**Solutions:**

1. **Check credentials:**
```bash
copaw config test-channel dingtalk
```

2. **Verify bot settings:**
   - AppKey and AppSecret correct
   - Bot added to group
   - Bot permissions enabled

3. **Check webhook:**
   - Webhook URL accessible
   - No firewall blocking

4. **Restart CoPaw:**
```bash
copaw app --restart
```

---

### Discord Bot Not Connecting

**Error:**
```
DiscordLoginFailure: Invalid token
```

**Solutions:**

1. **Verify bot token:**
   - Go to Discord Developer Portal
   - Copy token exactly (no spaces)

2. **Enable intents:**
   - Developer Portal → Bot → Privileged Gateway Intents
   - Enable: Message Content, Members, Presence

3. **Invite bot to server:**
   - OAuth2 → URL Generator
   - Select scopes: bot, applications.commands
   - Select permissions
   - Copy URL and invite

---

### Lark (Feishu) Bot Fails

**Issue:** Bot can't send or receive messages.

**Solutions:**

1. **Check app permissions:**
   - Lark Developer Platform
   - Ensure bot permissions granted

2. **Verify credentials:**
```yaml
channels:
  lark:
    app_id: cli_xxxxxxxxxxxxx
    app_secret: xxxxxxxxxxxxxxx
    verification_token: xxxxxxxxxxxxxxx
```

3. **Check event subscription:**
   - Enable event subscription
   - Verify verification token

---

## Skills Issues

### Skill Not Loading

**Error:**
```
ModuleNotFoundError: No module named 'my_skill'
Skill 'my_skill' not found
```

**Solutions:**

1. **Check skill path:**
```bash
ls ~/.copaw/skills/my_skill/
# Should contain: __init__.py, skill.py
```

2. **Verify config:**
```yaml
skills:
  custom:
    - name: my_skill
      path: /full/path/to/my_skill  # Use absolute path
```

3. **Reload skills:**
```bash
copaw skills reload
```

4. **Check dependencies:**
```bash
cd ~/.copaw/skills/my_skill
pip install -r requirements.txt
```

---

### Skill Execution Fails

**Error:**
```
Skill execution failed: my_skill
Error: Missing required parameter
```

**Solutions:**

1. **Check input format:**
```bash
copaw skills test my_skill --input '{"required_param": "value"}'
```

2. **Review skill code:**
   - Check validate() method
   - Verify required parameters

3. **Check permissions:**
```yaml
skills:
  my_skill:
    permissions:
      - read:input
      - write:output
```

---

### Skill Import Error

**Error:**
```
ImportError: No module named 'requests'
```

**Solution:**

Install missing dependencies:

```bash
cd ~/.copaw/skills/my_skill
pip install -r requirements.txt
```

Or add to requirements.txt:
```
requests
aiohttp
beautifulsoup4
```

---

## Memory Issues

### Memory Not Persisting

**Issue:** Conversations not saved between sessions.

**Solutions:**

1. **Check memory config:**
```yaml
memory:
  type: local
  path: ~/.copaw/memory
  enabled: true
```

2. **Verify directory exists:**
```bash
mkdir -p ~/.copaw/memory
```

3. **Check permissions:**
```bash
chmod 755 ~/.copaw/memory
```

4. **Test memory:**
```bash
copaw memory test
```

---

### Memory Search Not Working

**Issue:** Semantic search returns no results.

**Solutions:**

1. **Enable semantic search:**
```yaml
memory:
  semantic_search: true
```

2. **Rebuild index:**
```bash
copaw memory rebuild-index
```

3. **Check embedding model:**
```yaml
memory:
  embedding_model: all-MiniLM-L6-v2
```

---

### Memory Directory Full

**Error:**
```
No space left on device
Memory storage failed
```

**Solutions:**

1. **Clean old memories:**
```bash
copaw memory cleanup --days 30
```

2. **Export and clear:**
```bash
copaw memory export backup.jsonl
copaw memory clear
```

3. **Change storage location:**
```yaml
memory:
  path: /larger/disk/copaw/memory
```

---

## Performance Issues

### CoPaw Running Slow

**Issue:** General slowness in responses.

**Solutions:**

1. **Check system resources:**
```bash
# Memory
free -h

# CPU
top

# Disk
df -h
```

2. **Reduce concurrent channels:**
```yaml
channels:
  dingtalk:
    enabled: true
  discord:
    enabled: false  # Temporarily disable
```

3. **Use cloud models instead of local:**
```yaml
models:
  default:
    provider: dashscope
    model_name: qwen-turbo
```

4. **Increase resources (Docker):**
```yaml
# docker-compose.yml
services:
  copaw:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
```

---

### High CPU Usage

**Issue:** CoPaw using 100% CPU.

**Solutions:**

1. **Limit threads for local models:**
```yaml
models:
  local:
    n_threads: 4  # Limit CPU threads
```

2. **Disable unused features:**
```yaml
skills:
  auto_load: false  # Don't auto-load all skills
```

3. **Check for runaway processes:**
```bash
ps aux | grep copaw
kill <PID>  # If needed
```

---

### High Memory Usage

**Issue:** CoPaw using excessive RAM.

**Solutions:**

1. **Reduce context size:**
```yaml
models:
  local:
    n_ctx: 2048  # Smaller context
```

2. **Limit memory entries:**
```yaml
memory:
  max_entries: 5000  # Limit stored entries
```

3. **Use swap space:**
```bash
# Create swap file
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## Getting More Help

### Collect Debug Information

```bash
# CoPaw version
copaw --version

# Configuration
copaw config show

# Logs
tail -f ~/.copaw/copaw.log

# System info
python3 --version
uname -a
```

### Report an Issue

When reporting issues on GitHub, include:

1. **System information:**
   - OS and version
   - Python version
   - CoPaw version

2. **Error messages:**
   - Full error output
   - Stack trace

3. **Steps to reproduce:**
   - What you did
   - What you expected
   - What actually happened

4. **Configuration:**
   - Relevant config sections (remove API keys!)

### Useful Commands

```bash
# Test installation
copaw --version

# Test configuration
copaw config validate

# Test model
copaw config test-model

# Test channel
copaw config test-channel <channel>

# Test skill
copaw skills test <skill>

# View logs
copaw logs --tail 100

# Reset configuration
copaw init --reset

# Clear cache
copaw cache clear
```

---

## Next Steps

- [Installation Guide](../installation/README.md) - Reinstall if needed
- [Configuration Guide](../configuration/README.md) - Verify settings
- [Community Support](https://github.com/agentscope-ai/CoPaw/issues) - Get help

---

*Last updated: March 2026*
