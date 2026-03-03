# CoPaw Documentation

> **CoPaw** (Co Personal Agent Workstation) - A high-performance personal AI agent workstation open-sourced by Alibaba

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![GitHub](https://img.shields.io/github/stars/agentscope-ai/CoPaw)](https://github.com/agentscope-ai/CoPaw)

---

## 📖 What is CoPaw?

CoPaw is not just another chatbot—it's a **comprehensive workstation framework** designed to streamline the deployment and management of personal AI agents. It bridges high-level autonomous agent logic with real-world applications, providing a standardized platform for building, extending, and maintaining personal AI assistants.

### Key Characteristics

- 🤖 **Multi-Agent System** - Built on AgentScope for collaborative task orchestration
- 💾 **Persistent Memory** - ReMe module enables long-term experience retention
- 🔌 **Extensible Skills** - Python-based modular skill system
- 🌐 **Omni-Channel** - Unified access across DingTalk, Lark, QQ, Discord, iMessage, **Telegram**
- 🔒 **Privacy-First** - Local model support with full data sovereignty
- ☁️ **Cloud-Native** - One-click deployment to cloud platforms

---

## 🚀 Quick Start

### Installation (One-Click)

**macOS / Linux:**
```bash
curl -fsSL https://copaw.agentscope.io/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://copaw.agentscope.io/install.ps1 | iex
```

**Initialize and Run:**
```bash
copaw init
copaw app
```

Access the web console at: **http://127.0.0.1:8088/**

### Quick Telegram Setup

Want to use CoPaw on Telegram? (5 minutes)

```bash
# 1. Create bot via @BotFather in Telegram
# 2. Install dependencies
pip install python-telegram-bot==20.7

# 3. Add to ~/.copaw/config.yaml
# channels:
#   telegram:
#     enabled: true
#     bot_token: "YOUR_BOT_TOKEN"
#     mode: "polling"
#     allow_all_users: true

# 4. Start CoPaw
copaw app

# 5. Chat with your bot on Telegram!
```

See [Telegram Channel Guide](docs/channels/telegram/README.md) for complete setup.

---

## 📚 Documentation Structure

| Section | Description |
|---------|-------------|
| [📦 Installation](docs/installation/README.md) | Complete installation guides for all platforms |
| [⚙️ Configuration](docs/configuration/README.md) | Model setup, channel configuration, environment settings |
| [🏗️ Architecture](docs/architecture/README.md) | System architecture, components, and design principles |
| [🔧 Skills Development](docs/skills/README.md) | Creating and extending skills |
| [📝 Use Cases](docs/use-cases/README.md) | Real-world examples and scenarios |
| [❓ FAQ & Troubleshooting](docs/faq/README.md) | Common issues and solutions |

---

## 🎯 Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Multi-Channel Support** | Native integration with DingTalk, Lark, QQ, Discord, iMessage, **Telegram** |
| **Skill Extension System** | Modular Python-based functions for custom functionality |
| **ReMe Memory** | Persistent memory management (local/cloud) |
| **AgentScope Runtime** | Stable execution and resource management |
| **Local Model Support** | MLX and llama.cpp backends for offline operation |
| **Cloud Deployment** | ModelScope Studio, Alibaba Cloud ECS support |

### Supported Models

- **Qwen Series** (通义千问) - Full support
- **Mainstream LLMs** - Via API configuration
- **Local Models** - GGUF format with MLX/llama.cpp

---

## 🛠️ Installation Methods

| Method | Best For | Command |
|--------|----------|---------|
| **One-Click Script** | General users | `curl -fsSL https://copaw.agentscope.io/install.sh \| bash` |
| **pip** | Developers | `pip install copaw` |
| **Docker** | Enterprise/Ops | `docker pull agentscope/copaw:latest` |
| **Cloud** | Remote deployment | ModelScope Studio / Alibaba Cloud ECS |

See [Installation Guide](docs/installation/README.md) for detailed instructions.

---

## 📋 System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **Python** | 3.10+ | 3.11+ |
| **RAM** | 8GB | 16GB+ (for local models) |
| **OS** | macOS, Linux, Windows | macOS (Apple Silicon) |
| **Storage** | 2GB | 10GB+ (for local models) |

---

## 🔗 Resources

### Official Links
- **GitHub Repository**: [agentscope-ai/CoPaw](https://github.com/agentscope-ai/CoPaw)
- **Official Website**: [copaw.agentscope.io](https://copaw.agentscope.io)
- **ModelScope**: [ModelScope Studio](https://modelscope.cn)

### Community
- **Skills Hub**: [skills.sh](https://skills.sh)
- **ClawHub**: [clawhub.ai](https://clawhub.ai)
- **GitHub Issues**: [Report bugs & request features](https://github.com/agentscope-ai/CoPaw/issues)

---

## 📄 License

CoPaw is released under the [Apache 2.0 License](LICENSE).

---

## 📞 Support & Resources

- **Documentation**: Browse this repository for comprehensive guides
- **Framework Comparison**: [AgentScope vs qwen-agent](docs/AGENTSCOPE-VS-QWEN-AGENT.md) - Understand Alibaba's agent frameworks
- **Issues**: Check [GitHub Issues](https://github.com/agentscope-ai/CoPaw/issues) for known problems
- **FAQ**: See [FAQ & Troubleshooting](docs/faq/README.md) for common solutions

---

*Last updated: March 2026*
