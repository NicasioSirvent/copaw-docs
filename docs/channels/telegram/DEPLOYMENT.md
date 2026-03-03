# CoPaw Telegram Channel - Complete Deployment Guide

Step-by-step deployment guide adapted from OpenClaw's proven Telegram integration.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Phase 1: Bot Creation](#phase-1-bot-creation)
- [Phase 2: Installation](#phase-2-installation)
- [Phase 3: Configuration](#phase-3-configuration)
- [Phase 4: Deployment](#phase-4-deployment)
- [Phase 5: Testing](#phase-5-testing)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **OS** | Linux/macOS/Windows | Linux (Ubuntu 22.04+) |
| **RAM** | 2GB | 4GB+ |
| **Storage** | 1GB | 5GB+ |
| **Python** | 3.10+ | 3.11+ |
| **Network** | Outbound HTTPS | Public IP (for webhook) |

### Required Accounts

- ✅ Telegram account
- ✅ CoPaw installed and configured
- ✅ Domain name (for webhook mode, optional)

---

## Phase 1: Bot Creation

### Step 1.1: Create Telegram Bot

1. **Open Telegram** on your device

2. **Search for @BotFather**
   ```
   In Telegram search: @BotFather
   ```

3. **Start conversation**
   ```
   Send: /start
   ```

4. **Create new bot**
   ```
   Send: /newbot
   ```

5. **Choose bot name** (display name)
   ```
   Example: "CoPaw AI Assistant"
   ```

6. **Choose username** (must end with _bot)
   ```
   Example: "MyCoPawTestBot"
   ```

7. **Save the token**
   ```
   BotFather responds:
   
   Done! Congratulations on your new bot.
   
   Name: CoPaw AI Assistant
   Username: MyCoPawTestBot
   
   Use this token to access the bot:
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   
   ⚠️ IMPORTANT: Save this token securely!
   ```

### Step 1.2: Configure Bot Privacy

1. **Disable privacy mode** (for group chats)
   ```
   Send to @BotFather: /setprivacy
   ```

2. **Select your bot**
   ```
   @MyCoPawTestBot
   ```

3. **Disable privacy**
   ```
   Send: Disable
   ```

   This allows the bot to read all group messages, not just @mentions.

### Step 1.3: Get Your User ID

For access control, get your Telegram user ID:

1. **Search for @userinfobot**
   ```
   In Telegram: @userinfobot
   ```

2. **Start the bot**
   ```
   Send: /start
   ```

3. **Note your ID**
   ```
   Response: "Your ID is: 123456789"
   ```

---

## Phase 2: Installation

### Step 2.1: Install Python Dependencies

```bash
# Navigate to CoPaw working directory
cd ~/.copaw

# Install Telegram channel dependencies
pip install python-telegram-bot==20.7
```

### Step 2.2: Install Channel Plugin

**Option A: From Package (when published)**
```bash
pip install copaw-channel-telegram
```

**Option B: Manual Installation**
```bash
# Create channels directory
mkdir -p ~/.copaw/channels

# Copy telegram_channel.py
cp /path/to/telegram_channel.py ~/.copaw/channels/

# Verify installation
ls ~/.copaw/channels/
# Should show: telegram_channel.py
```

**Option C: From Git Repository**
```bash
# Clone repository
git clone https://github.com/your-org/copaw-telegram-channel.git
cd copaw-telegram-channel

# Install in development mode
pip install -e .
```

### Step 2.3: Verify Installation

```bash
# Check Python can import telegram
python -c "from telegram import Bot; print('✅ Telegram library installed')"

# Check CoPaw can find channel
copaw channels list
# Should show: telegram (if installed correctly)
```

---

## Phase 3: Configuration

### Step 3.1: Basic Configuration (Testing)

**File:** `~/.copaw/config.yaml`

```yaml
channels:
  telegram:
    enabled: true
    bot_token: "YOUR_BOT_TOKEN_HERE"
    mode: "polling"
    allow_all_users: true
```

**Replace:**
- `YOUR_BOT_TOKEN_HERE` with token from @BotFather

### Step 3.2: Secure Configuration (Production)

**File:** `~/.copaw/config.yaml`

```yaml
channels:
  telegram:
    enabled: true
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    mode: "polling"
    allow_all_users: false
    allow_from:
      - "YOUR_USER_ID"
    dm_policy: "pairing"
```

**Set environment variable:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Or create .env file
echo "TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz" >> ~/.copaw/.env
```

### Step 3.3: Webhook Configuration (Advanced)

**Prerequisites:**
- Public IP or domain
- SSL certificate (Let's Encrypt recommended)

**Configuration:**
```yaml
channels:
  telegram:
    enabled: true
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    mode: "webhook"
    webhook_port: 8787
    webhook_url: "https://your-domain.com:8787/telegram/callback"
    ssl_cert: "/etc/letsencrypt/live/your-domain.com/fullchain.pem"
    ssl_key: "/etc/letsencrypt/live/your-domain.com/privkey.pem"
```

**Get SSL Certificate:**
```bash
# Install certbot
sudo apt install certbot

# Get certificate
sudo certbot certonly --standalone -d your-domain.com

# Certificates location:
# /etc/letsencrypt/live/your-domain.com/fullchain.pem
# /etc/letsencrypt/live/your-domain.com/privkey.pem
```

---

## Phase 4: Deployment

### Step 4.1: Start CoPaw

```bash
# Start CoPaw with Telegram channel
copaw app
```

**Expected output:**
```
[INFO] Initializing channels...
[INFO] Telegram bot initialized (@MyCoPawTestBot)
[INFO] CoPaw web console: http://127.0.0.1:8088/
[INFO] Ready!
```

### Step 4.2: Verify Bot Status

**Via CLI:**
```bash
copaw channel test telegram
```

**Expected output:**
```
✅ Telegram channel is online
Bot: @MyCoPawTestBot
Mode: polling
Users allowed: all (testing mode)
```

**Via Telegram:**
```
1. Open Telegram
2. Search: @MyCoPawTestBot
3. Send: /start
4. Should receive welcome message
```

### Step 4.3: Test AI Response

```
1. Send to bot: "Hello, CoPaw!"
2. Bot should respond with AI-generated message
3. Try follow-up questions
```

---

## Phase 5: Testing

### Test Checklist

- [ ] Bot responds to `/start`
- [ ] Bot responds to `/help`
- [ ] Bot responds to `/status`
- [ ] Bot responds to regular messages
- [ ] Bot handles long messages (chunking)
- [ ] Access control works (if configured)
- [ ] Group chat works (if configured)

### Test Commands

```
/start          - Welcome message
/help           - Help information
/status         - Bot status
/test           - Test connection

Hello!          - Simple greeting
What is AI?     - Knowledge question
Write a poem    - Creative task
```

### Test Access Control

**For restricted access:**
```
1. From allowed user: Should work ✅
2. From non-allowed user: Should be blocked ❌
3. From allowed user in group: Should work ✅
```

---

## Production Deployment

### Option 1: Docker Deployment

**File:** `docker-compose.yml`

```yaml
version: '3.8'

services:
  copaw:
    image: agentscope/copaw:latest
    container_name: copaw
    ports:
      - "8088:8088"
      - "8787:8787"
    volumes:
      - ./config:/app/config
      - ./data:/app/working
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - DASHSCOPE_API_KEY=${DASHSCOPE_API_KEY}
    restart: unless-stopped
```

**Deploy:**
```bash
# Start
docker-compose up -d

# View logs
docker-compose logs -f copaw

# Stop
docker-compose down
```

### Option 2: Systemd Service (Linux)

**File:** `/etc/systemd/system/copaw.service`

```ini
[Unit]
Description=CoPaw AI Assistant
After=network.target

[Service]
Type=simple
User=copaw
WorkingDirectory=/opt/copaw
Environment="TELEGRAM_BOT_TOKEN=YOUR_TOKEN"
Environment="DASHSCOPE_API_KEY=YOUR_KEY"
ExecStart=/opt/copaw/venv/bin/copaw app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Deploy:**
```bash
# Copy service file
sudo cp copaw.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable copaw

# Start service
sudo systemctl start copaw

# Check status
sudo systemctl status copaw

# View logs
sudo journalctl -u copaw -f
```

### Option 3: Cloud Deployment (Alibaba Cloud)

**Steps:**

1. **Create ECS instance**
   - Ubuntu 22.04
   - 2GB RAM minimum
   - Open ports: 8088, 8787

2. **Install CoPaw**
   ```bash
   curl -fsSL https://copaw.agentscope.io/install.sh | bash
   ```

3. **Configure Telegram**
   ```bash
   copaw init
   # Follow prompts to configure Telegram
   ```

4. **Deploy**
   ```bash
   copaw app
   ```

5. **Set up SSL** (for webhook)
   ```bash
   sudo apt install certbot
   sudo certbot certonly --standalone -d your-domain.com
   ```

---

## Troubleshooting

### Bot Not Responding

**Check:**
```bash
# 1. Verify bot token
copaw config show telegram

# 2. Test connection
copaw channel test telegram

# 3. Check logs
copaw logs --follow | grep telegram
```

**Solutions:**
- ✅ Verify bot token is correct (no spaces)
- ✅ Ensure bot is not blocked
- ✅ Check `allow_all_users` setting
- ✅ Verify bot privacy is disabled in @BotFather

### Connection Errors

**Polling Mode:**
```bash
# Check network connectivity
curl https://api.telegram.org

# Check firewall
sudo ufw status

# Test with different network
```

**Webhook Mode:**
```bash
# Check port is open
sudo netstat -tlnp | grep 8787

# Test webhook URL
curl -X POST https://your-domain.com:8787/telegram/callback

# Check SSL certificate
openssl s_client -connect your-domain.com:8787
```

### Access Denied

**Check configuration:**
```yaml
channels:
  telegram:
    allow_all_users: false  # Change to true for testing
    allow_from:
      - "YOUR_USER_ID"
```

**Get user ID:**
```
1. Search @userinfobot in Telegram
2. Send /start
3. Note your ID
```

### Webhook Not Working

**Common issues:**

1. **Port not open**
   ```bash
   sudo ufw allow 8787/tcp
   ```

2. **SSL certificate invalid**
   ```bash
   # Renew certificate
   sudo certbot renew
   ```

3. **Webhook URL incorrect**
   ```bash
   # Check current webhook
   curl "https://api.telegram.org/botTOKEN/getWebhookInfo"
   ```

### Performance Issues

**Optimize polling:**
```yaml
channels:
  telegram:
    polling_interval: 0.5  # Faster (default: 1.0)
    timeout: 10            # Shorter timeout
```

**Optimize webhook:**
```yaml
channels:
  telegram:
    timeout: 30
    retry_limit: 5
```

---

## Next Steps

After successful deployment:

1. **Configure additional channels** (DingTalk, Discord, etc.)
2. **Create custom skills** for Telegram
3. **Set up monitoring** and alerts
4. **Configure backup** and recovery
5. **Document** your specific setup

---

## Resources

- **Telegram Bot API**: https://core.telegram.org/bots/api
- **python-telegram-bot**: https://docs.python-telegram-bot.org
- **CoPaw Documentation**: https://copaw.agentscope.io
- **OpenClaw Telegram Guide**: https://docs.openclaw.ai/channels/telegram

---

*Last updated: March 2026*
