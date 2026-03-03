# CoPaw Overview

Visual overview and quick reference for CoPaw.

---

## What is CoPaw?

```
┌─────────────────────────────────────────────────────────────────┐
│                         CoPaw                                    │
│              (Co Personal Agent Workstation)                     │
│                                                                  │
│  Your personal AI agent that connects to all your chat apps     │
│  and helps you automate tasks with persistent memory.           │
└─────────────────────────────────────────────────────────────────┘
```

**In Simple Terms:** CoPaw is like having a smart assistant that lives in all your chat apps (DingTalk, Discord, etc.) and remembers everything, learns from you, and can do tasks automatically.

---

## Architecture at a Glance

```
┌──────────────────────────────────────────────────────────────────┐
│                        USER INTERFACES                            │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌────────┐ │
│  │DingTalk │  │  Lark   │  │   QQ    │  │Discord  │  │iMessage│ │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └───┬────┘ │
└───────┼───────────┼───────────┼───────────┼───────────┼───────┘
        │           │           │           │           │
        └───────────┴─────┬─────┴───────────┴───────────┘
                          │
        ┌─────────────────▼─────────────────┐
        │      CONNECTIVITY LAYER            │
        │   (Channel Adapters & Routing)     │
        └─────────────────┬─────────────────┘
                          │
        ┌─────────────────▼─────────────────┐
        │       AGENT LOGIC LAYER            │
        │     (AgentScope Framework)         │
        │  ┌─────────────────────────────┐  │
        │  │  Planner → Executor → Eval  │  │
        │  └─────────────────────────────┘  │
        └─────────────────┬─────────────────┘
                          │
        ┌─────────────────▼─────────────────┐
        │       RUNTIME LAYER                │
        │   (Resource & Safety Management)   │
        └─────────────────┬─────────────────┘
                          │
        ┌─────────────────▼─────────────────┐
        │        MEMORY LAYER                │
        │      (ReMe - Persistent)           │
        │   Local Storage │ Cloud Storage   │
        └─────────────────┬─────────────────┘
                          │
        ┌─────────────────▼─────────────────┐
        │       SKILLS LAYER                 │
        │  (Web, Files, APIs, Custom Code)   │
        └───────────────────────────────────┘
```

---

## Key Features

```
┌─────────────────────────────────────────────────────────┐
│  🌐 OMNI-CHANNEL                                        │
│  One assistant across all your chat platforms           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  💾 PERSISTENT MEMORY                                   │
│  Remembers conversations and learns over time           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  🔌 EXTENSIBLE SKILLS                                   │
│  Add custom functionality with Python modules           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  🤖 MULTI-AGENT SYSTEM                                  │
│  Multiple specialized agents working together           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  🔒 PRIVACY-FOCUSED                                     │
│  Local models and storage for full data control         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  ☁️ CLOUD-NATIVE                                        │
│  Deploy anywhere: local, Docker, or cloud platforms     │
└─────────────────────────────────────────────────────────┘
```

---

## Quick Start Flow

```
1. INSTALL
   ┌──────────────────────────────────────┐
   │ macOS/Linux:                         │
   │ curl -fsSL https://copaw.agentscope. │
   │ io/install.sh | bash                 │
   │                                      │
   │ Windows:                             │
   │ irm https://copaw.agentscope.io/     │
   │ install.ps1 | iex                    │
   └──────────────────────────────────────┘
              │
              ▼
2. INITIALIZE
   ┌──────────────────────────────────────┐
   │ copaw init                           │
   │ (Follow prompts to configure)        │
   └──────────────────────────────────────┘
              │
              ▼
3. RUN
   ┌──────────────────────────────────────┐
   │ copaw app                            │
   │                                      │
   │ Open: http://127.0.0.1:8088/         │
   └──────────────────────────────────────┘
              │
              ▼
4. CONFIGURE CHANNELS
   ┌──────────────────────────────────────┐
   │ Settings → Channels                  │
   │ Add DingTalk, Discord, etc.          │
   └──────────────────────────────────────┘
              │
              ▼
5. USE
   ┌──────────────────────────────────────┐
   │ @CoPaw in your chat apps             │
   │ Start automating! 🚀                 │
   └──────────────────────────────────────┘
```

---

## Use Case Examples

### Personal Assistant
```
User: "@CoPaw, what's on my schedule today?"
       │
       ▼
CoPaw checks calendar → Formats response → Sends to chat
       │
       ▼
"📅 Today's Schedule:
 • 10:00 AM - Team Standup
 • 2:00 PM - Client Meeting
 • 4:00 PM - Code Review"
```

### Team Collaboration
```
Developer: "@CoPaw, what's the status of PR #45?"
       │
       ▼
CoPaw checks GitHub → Analyzes status → Responds
       │
       ▼
"✅ PR #45 Status:
 • 2 approvals received
 • All checks passing
 • Ready to merge"
```

### Automated Workflows
```
Scheduled Task: Daily Briefing (8:00 AM)
       │
       ▼
CoPaw gathers: Weather + News + Calendar + Tasks
       │
       ▼
Sends formatted briefing to all configured channels
```

---

## Component Relationships

```
┌─────────────────────────────────────────────────────────┐
│                    HOW IT ALL CONNECTS                   │
└─────────────────────────────────────────────────────────┘

    USER MESSAGE (via chat app)
            │
            ▼
    ┌───────────────┐
    │   Channel     │ ← Connects to DingTalk, Discord, etc.
    │   Adapter     │
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │   AgentScope  │ ← Routes to appropriate agent
    │   Router      │
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │    Memory     │ ← Retrieves context (ReMe)
    │   (ReMe)      │
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │      LLM      │ ← Generates response (Local/Cloud)
    │   (Qwen, etc) │
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │    Skills     │ ← Execute actions if needed
    │   (Optional)  │
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │   Response    │ ← Send back to user
    │   Delivery    │
    └───────────────┘
```

---

## Documentation Map

```
                    START HERE
                       │
              ┌────────▼────────┐
              │   README.md     │
              │  (Overview &    │
              │   Quick Start)  │
              └────────┬────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌───────────┐ ┌──────────┐
│ Installation │ │Configure  │ │Architecture│
│   Guide      │ │  Guide    │ │   Guide   │
└──────────────┘ └───────────┘ └──────────┘
        │              │              │
        │              │              │
        ▼              ▼              ▼
┌─────────────────────────────────────────┐
│           SKILLS DEVELOPMENT            │
│            (Extend CoPaw)               │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│            USE CASES                    │
│      (Real-world Examples)              │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│         FAQ & TROUBLESHOOTING           │
│          (Get Help)                     │
└─────────────────────────────────────────┘
```

---

## Decision Tree: Which Model?

```
Do you need privacy?
    │
    ├─ YES → Use Local Model
    │         │
    │         ├─ Apple Silicon? → MLX Backend
    │         │
    │         └─ Other? → llama.cpp Backend
    │
    └─ NO → Use Cloud Model
              │
              ├─ Need speed? → Qwen-Turbo
              │
              ├─ Need quality? → Qwen-Max
              │
              └─ Already using OpenAI? → GPT-4
```

---

## Comparison with Other Solutions

| Feature | CoPaw | Bot Frameworks | Chatbot Platforms |
|---------|-------|----------------|-------------------|
| **Multi-Channel** | ✅ Native | ⚠️ Add-ons | ⚠️ Limited |
| **Persistent Memory** | ✅ Built-in | ❌ Custom | ⚠️ Basic |
| **Local Models** | ✅ Full Support | ⚠️ Complex | ❌ No |
| **Skill System** | ✅ Python | ✅ Code | ⚠️ Limited |
| **Multi-Agent** | ✅ AgentScope | ⚠️ Custom | ❌ No |
| **Open Source** | ✅ Apache 2.0 | ✅ Various | ❌ Proprietary |
| **Self-Hosted** | ✅ Yes | ✅ Yes | ❌ No |

---

## Getting Help

```
┌─────────────────────────────────────────────────────────┐
│  📖 Read Documentation                                  │
│  Start with README.md, then dive into specific guides   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  ❓ Check FAQ                                           │
│  docs/faq/README.md - Common issues and solutions       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  🐛 Report Issues                                       │
│  github.com/agentscope-ai/CoPaw/issues                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  💬 Community                                           │
│  Join discussions, share skills, get help               │
└─────────────────────────────────────────────────────────┘
```

---

*Last updated: March 2026*
