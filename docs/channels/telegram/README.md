# CoPaw Telegram Channel Integration

Complete guide for integrating Telegram with CoPaw, adapted from OpenClaw's mature implementation.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Configuration Options](#configuration-options)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)

---

## Overview

CoPaw now supports **Telegram** as a messaging channel! This integration is adapted from **OpenClaw's mature Telegram implementation**, bringing proven features to CoPaw.

### What You Get

| Feature | Status |
|---------|--------|
| **Bot API Integration** | ✅ Full support |
| **Webhook Mode** | ✅ Supported |
| **Polling Mode** | ✅ Supported |
| **Group Chats** | ✅ With mention filtering |
| **Direct Messages** | ✅ With pairing system |
| **Media Messages** | ✅ Images, files, voice |
| **Message Chunking** | ✅ Auto-split long responses |
| **Access Control** | ✅ Allowlist, DM policies |

---

## Features

### Core Capabilities

- **🤖 Bot Integration**: Full Telegram Bot API support via `python-telegram-bot`
- **🔗 Webhook Support**: Real-time message delivery (port 8787)
- **📡 Polling Mode**: Alternative to webhook, no public IP needed
- **👥 Group Support**: Multi-user groups with mention-based triggering
- **💬 DM Support**: Private conversations with pairing authentication
- **📎 Media Handling**: Images, documents, voice messages
- **✂️ Message Chunking**: Automatic splitting for long responses
- **🔐 Access Control**: User allowlists, group policies, DM modes

### DM Policies (adapted from OpenClaw)

| Policy | Behavior |
|--------|----------|
| **pairing** (default) | Unknown users get pairing code (1h expiry) |
| **allowlist** | Block unknown users without pairing |
| **open** | Allow any DM (set `allowFrom: ["*"]`) |
| **disabled** | Ignore all direct messages |

### Group Policies

- **allowlist**: Restrict to specific group IDs
- **requireMention**: Bot must be @mentioned to respond
- **allowAll**: Respond to all messages in allowed groups

---

## Architecture

### System Design

Adapted from OpenClaw's proven hub-and-spoke architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    CoPaw Core                               │
│              (AgentScope + ReMe Memory)                     │
└─────────────────────────────────────────────────────────────┘
                              ↑
                              │ Internal Message Format
                              ↓
┌─────────────────────────────────────────────────────────────┐
│               TELEGRAM CHANNEL ADAPTER                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  Auth       │  │  Inbound    │  │  Outbound           │ │
│  │  (Token)    │→ │  Parser     │→ │  Formatter          │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
│         ↑                ↑                    ↑              │
│  TELEGRAM_BOT     Standardize         Markdown → Telegram   │
│  _TOKEN           text/media/         + Message Chunking    │
│                   attachments       + Media Upload          │
└─────────────────────────────────────────────────────────────┘
                              ↑
                              │
                    ┌─────────────────┐
                    │  Telegram API   │
                    │ (python-telegram│
                    │      -bot)      │
                    └─────────────────┘
```

### Message Flow

```
1. User sends message on Telegram
         │
         ▼
2. Telegram API → Webhook/Polling
         │
         ▼
3. TelegramChannel.receive()
         │
         ▼
4. Parse to CoPaw internal format
         │
         ▼
5. ChannelManager → AgentScope
         │
         ▼
6. AI processes and generates response
         │
         ▼
7. TelegramChannel.send()
         │
         ▼
8. Format and send to Telegram
         │
         ▼
9. User receives response
```

### Session Key Format

Similar to OpenClaw, CoPaw uses hierarchical session keys:

```
agent:<agentId>:telegram:<type>:<identifier>
```

Examples:
- `agent:main:telegram:group:-1001234567890` — Group chat
- `agent:main:telegram:dm:123456789` — Direct message

---

## Quick Start

### 5-Minute Setup (Polling Mode)

**1. Create Telegram Bot**
```
1. Open Telegram, search for @BotFather
2. Send: /newbot
3. Name: "CoPaw Assistant"
4. Username: "MyCoPawBot" (must end with _bot)
5. Save the token: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

**2. Install Dependencies**
```bash
pip install python-telegram-bot==20.7
```

**3. Configure CoPaw**

Add to `~/.copaw/config.yaml`:

```yaml
channels:
  telegram:
    enabled: true
    bot_token: "YOUR_BOT_TOKEN_HERE"
    mode: "polling"  # or "webhook"
    allow_all_users: true  # For testing only!
```

**4. Start CoPaw**
```bash
copaw app
```

**5. Test**
```
1. Open Telegram
2. Search for your bot: @MyCoPawBot
3. Send: /start
4. Send: "Hello!"
5. Bot should respond!
```

---

## Detailed Setup

### Step 1: Create Telegram Bot

**Via @BotFather:**

1. **Open Telegram** and search for `@BotFather`
2. **Start conversation**: Send `/start`
3. **Create new bot**: Send `/newbot`
4. **Choose name**: `CoPaw AI Assistant` (display name)
5. **Choose username**: `CoPawTestBot` (must end with `_bot`)
6. **Save token**: BotFather responds with:
   ```
   Done! Congratulations on your new bot.
   
   Name: CoPaw AI Assistant
   Username: CoPawTestBot
   
   Use this token to access the bot:
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   
   ```

**Security Note:** Keep your bot token secret! Never commit it to Git.

### Step 2: Configure Bot Privacy

For full functionality, adjust bot privacy:

```
1. Send to @BotFather: /setprivacy
2. Select your bot
3. Send: "Disable"
```

This allows the bot to read all group messages (not just those with @mentions).

### Step 3: Choose Deployment Mode

#### **Mode A: Polling (Recommended for Testing)**

**Pros:**
- ✅ No public IP required
- ✅ Works behind NAT/firewall
- ✅ Simpler setup

**Cons:**
- ❌ Slight delay in message delivery
- ❌ Continuous API calls

**Configuration:**
```yaml
channels:
  telegram:
    enabled: true
    bot_token: "YOUR_TOKEN"
    mode: "polling"
    polling_interval: 1.0  # seconds
```

#### **Mode B: Webhook (Recommended for Production)**

**Pros:**
- ✅ Real-time message delivery
- ✅ More efficient (no polling overhead)

**Cons:**
- ❌ Requires public IP/domain
- ❌ Needs SSL certificate (Telegram requires HTTPS)

**Configuration:**
```yaml
channels:
  telegram:
    enabled: true
    bot_token: "YOUR_TOKEN"
    mode: "webhook"
    webhook_port: 8787
    webhook_url: "https://your-domain.com:8787/telegram/callback"
    ssl_cert: "/path/to/cert.pem"
    ssl_key: "/path/to/key.pem"
```

### Step 4: Install Channel Plugin

**Option A: Using pip**
```bash
pip install copaw-channel-telegram
```

**Option B: From source**
```bash
git clone https://github.com/your-org/copaw-telegram-channel.git
cd copaw-telegram-channel
pip install -e .
```

**Option C: Manual installation**
```bash
# Copy telegram_channel.py to CoPaw channels directory
cp telegram_channel.py ~/.copaw/channels/

# Install dependencies
pip install python-telegram-bot==20.7
```

### Step 5: Configure Access Control

#### **For Testing (Allow All)**
```yaml
channels:
  telegram:
    allow_all_users: true
```

#### **For Production (Restricted)**
```yaml
channels:
  telegram:
    allow_all_users: false
    allow_from:
      - "123456789"  # Your Telegram user ID
      - "987654321"  # Other allowed users
    dm_policy: "pairing"
```

**Get Your Telegram User ID:**
```
1. Search for @userinfobot in Telegram
2. Start the bot
3. It will show your ID (e.g., 123456789)
```

### Step 6: Test Connection

**Via CLI:**
```bash
copaw channel test telegram
```

**Via Telegram:**
```
1. Send /start to your bot
2. Send: "Hello, CoPaw!"
3. You should receive an AI response
```

---

## Configuration Options

### Complete Configuration Reference

```yaml
channels:
  telegram:
    # === Required ===
    enabled: true
    bot_token: "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
    
    # === Connection Mode ===
    mode: "polling"  # or "webhook"
    
    # === Polling Settings ===
    polling_interval: 1.0  # Check for messages every 1 second
    
    # === Webhook Settings ===
    webhook_port: 8787
    webhook_url: "https://your-domain.com:8787/telegram/callback"
    ssl_cert: "/etc/ssl/certs/your-cert.pem"
    ssl_key: "/etc/ssl/private/your-key.pem"
    
    # === Access Control ===
    allow_all_users: false  # Set true for testing only!
    allow_from:
      - "123456789"  # Allowed user IDs
    dm_policy: "pairing"  # pairing | allowlist | open | disabled
    
    # === Group Settings ===
    group_policy: "allowlist"
    group_allow_from:
      - "-1001234567890"  # Allowed group IDs
    require_mention: true  # Must @mention bot to respond
    group_auto_reply: false  # Auto-reply in groups
    
    # === Message Handling ===
    command_prefix: "/"  # Command prefix (e.g., /ai)
    max_message_length: 4096  # Telegram max message length
    chunk_messages: true  # Auto-split long messages
    parse_mode: "Markdown"  # Markdown | HTML | None
    
    # === Session Management ===
    session_memory: true  # Remember conversation context
    session_ttl: 3600  # Session timeout in seconds
    
    # === Advanced ===
    timeout: 30  # API timeout in seconds
    retry_limit: 3  # Max retry attempts
    log_messages: false  # Log all messages (debug)
```

### Configuration Examples

#### **Basic Testing Setup**
```yaml
channels:
  telegram:
    enabled: true
    bot_token: "YOUR_TOKEN"
    mode: "polling"
    allow_all_users: true
```

#### **Production Setup (Webhook + SSL)**
```yaml
channels:
  telegram:
    enabled: true
    bot_token: "YOUR_TOKEN"
    mode: "webhook"
    webhook_port: 8787
    webhook_url: "https://copaw.example.com:8787/telegram/callback"
    ssl_cert: "/etc/letsencrypt/live/copaw.example.com/fullchain.pem"
    ssl_key: "/etc/letsencrypt/live/copaw.example.com/privkey.pem"
    allow_all_users: false
    allow_from:
      - "123456789"
    dm_policy: "pairing"
    require_mention: true
```

#### **Group Chat Bot**
```yaml
channels:
  telegram:
    enabled: true
    bot_token: "YOUR_TOKEN"
    mode: "polling"
    allow_all_users: false
    group_policy: "allowlist"
    group_allow_from:
      - "-1001234567890"  # Your group ID
    require_mention: true
    group_auto_reply: false
```

---

## Advanced Features

### 1. Command System

Define custom commands:

```yaml
channels:
  telegram:
    commands:
      - command: "ai"
        description: "Ask AI a question"
        example: "/ai What is quantum computing?"
      
      - command: "help"
        description: "Show help message"
      
      - command: "status"
        description: "Show bot status"
```

**Usage:**
```
/ai Explain quantum entanglement
/help
/status
```

### 2. Message Chunking

For responses exceeding Telegram's 4096 character limit:

```yaml
channels:
  telegram:
    chunk_messages: true
    max_message_length: 4096
    chunk_separator: "\n\n---\n\n"
```

**Behavior:**
```
Long response (5000 chars)
         │
         ▼
    Split into chunks
         │
         ▼
    Chunk 1 (4096 chars) → Sent
    Chunk 2 (904 chars)  → Sent
```

### 3. Media Message Handling

**Receive Media:**
```yaml
channels:
  telegram:
    handle_images: true
    handle_documents: true
    handle_voice: true
    download_path: "~/.copaw/media/"
```

**Send Media:**
```python
# In your skill
return {
    "type": "photo",
    "caption": "Here's your image",
    "path": "/path/to/image.jpg"
}
```

### 4. DM Policy Examples

#### **Pairing Mode (Default)**
```yaml
channels:
  telegram:
    dm_policy: "pairing"
    pairing_timeout: 3600  # 1 hour
```

**Flow:**
```
1. Unknown user sends message
         │
         ▼
2. Bot sends pairing code
         │
         ▼
3. User sends code to bot
         │
         ▼
4. Bot approves pairing
         │
         ▼
5. User can now DM bot
```

#### **Open Mode**
```yaml
channels:
  telegram:
    dm_policy: "open"
    allow_from: ["*"]  # Allow all users
```

⚠️ **Warning:** Only use for public bots!

### 5. Group Chat Features

#### **Mention-Based Triggering**
```yaml
channels:
  telegram:
    require_mention: true
    mention_prefix: "@CoPawBot"
```

**Usage:**
```
User: "@CoPawBot What's the weather today?"
Bot: [Responds]

User: "What's the weather?"  (no mention)
Bot: [Ignores]
```

#### **Group Auto-Reply**
```yaml
channels:
  telegram:
    group_auto_reply: true
    group_reply_keywords:
      - "copaw"
      - "ai"
      - "bot"
```

Bot responds when keywords are detected.

---

## Troubleshooting

### Common Issues

#### **Bot Not Responding**

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
- ✅ Verify bot token is correct (no extra spaces)
- ✅ Ensure bot is not blocked by user
- ✅ Check `allow_all_users` or `allow_from` settings
- ✅ Verify bot privacy is disabled in @BotFather

#### **Webhook Not Working**

**Check:**
```bash
# 1. Verify port is open
sudo netstat -tlnp | grep 8787

# 2. Test webhook URL
curl -X POST https://your-domain.com:8787/telegram/callback

# 3. Check SSL certificate
openssl s_client -connect your-domain.com:8787
```

**Solutions:**
- ✅ Ensure port 8787 is open in firewall
- ✅ Verify SSL certificate is valid (not self-signed)
- ✅ Check webhook_url matches your domain exactly
- ✅ Restart CoPaw after config changes

#### **Polling Mode Slow**

**Solutions:**
```yaml
channels:
  telegram:
    polling_interval: 0.5  # Reduce from 1.0 to 0.5
    timeout: 10  # Reduce API timeout
```

#### **Messages Being Truncated**

**Solutions:**
```yaml
channels:
  telegram:
    chunk_messages: true
    max_message_length: 4096
```

#### **Group Chat Not Working**

**Check:**
```bash
# Get group ID
# 1. Add bot to group
# 2. Send message in group
# 3. Check logs for group ID (starts with -100)
```

**Solutions:**
- ✅ Add group ID to `group_allow_from`
- ✅ Disable bot privacy in @BotFather
- ✅ Ensure `require_mention` is configured correctly

### Debug Mode

Enable detailed logging:

```yaml
channels:
  telegram:
    log_messages: true
    debug: true
```

**View logs:**
```bash
copaw logs --follow --level DEBUG | grep telegram
```

### Get Help

1. **Check documentation**: This guide
2. **GitHub Issues**: [agentscope-ai/CoPaw/issues](https://github.com/agentscope-ai/CoPaw/issues)
3. **Community**: Telegram groups, Discord

---

## Comparison: OpenClaw vs CoPaw Telegram

| Feature | OpenClaw | CoPaw |
|---------|----------|-------|
| **Library** | grammY (Node.js) | python-telegram-bot (Python) |
| **Webhook Port** | 18789 | 8787 |
| **Session Format** | `agent:<id>:telegram:<type>:<id>` | Same |
| **DM Policies** | pairing, allowlist, open, disabled | Same |
| **Group Policies** | allowlist + mention | Same |
| **Message Format** | JSON Schema frames | CoPaw internal dict |
| **Configuration** | YAML + env vars | YAML config |

---

## Next Steps

- [Configuration Guide](../../configuration/README.md) - General CoPaw configuration
- [Skills Development](../../skills/README.md) - Create Telegram-aware skills
- [Use Cases](../../use-cases/BUSINESS-RESEARCH-PERSONAL.md) - Telegram use cases

---

*Last updated: March 2026*
