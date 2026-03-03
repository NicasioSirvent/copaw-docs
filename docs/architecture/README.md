# CoPaw Architecture

This document provides a comprehensive overview of CoPaw's architecture, components, and design principles.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Framework Relationships](#framework-relationships)
- [Core Components](#core-components)
- [System Design](#system-design)
- [Data Flow](#data-flow)
- [Extension Points](#extension-points)

---

## Architecture Overview

CoPaw is built on a **three-layer middleware architecture** that transforms raw LLM capabilities into proactive, personalized assistants:

---

## Framework Relationships

CoPaw is part of Alibaba's broader agent ecosystem:

```
┌─────────────────────────────────────────────────────────────┐
│              Alibaba Agent Ecosystem                         │
│                                                              │
│  ┌──────────────────┐        ┌──────────────────┐           │
│  │   qwen-agent     │        │    AgentScope    │           │
│  │                  │        │                  │           │
│  │  • Qwen-optimized│        │  • Multi-agent   │           │
│  │  • Function Call │        │  • Orchestration │           │
│  │  • Code Interpreter    │  • Production     │           │
│  │  • RAG (1M tokens)     │  • Deployment     │           │
│  │  • Qwen Chat backend │  • CoPaw backend  │           │
│  └──────────────────┘        └────────┬─────────┘           │
│                                       │                      │
│                                       ▼                      │
│                              ┌──────────────────┐           │
│                              │      CoPaw       │           │
│                              │                  │           │
│                              │  • Channels      │           │
│                              │  • Skills        │           │
│                              │  • Memory (ReMe) │           │
│                              │  • Web Console   │           │
│                              └──────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

**Key Points:**
- **CoPaw** is built on **AgentScope** (multi-agent framework)
- **AgentScope** and **qwen-agent** are **complementary** (can be used together)
- **qwen-agent** is Qwen-optimized for single-agent applications

For detailed comparison, see [AgentScope vs qwen-agent](AGENTSCOPE-VS-QWEN-AGENT.md).

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  DingTalk   │  │    Lark     │  │   Discord   │  ...     │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Connectivity Layer                         │
│              (All-Domain Access / Channels)                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Agent Logic Layer                         │
│                  (AgentScope Framework)                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Planner   │  │  Executor   │  │  Evaluator  │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Runtime Layer                              │
│              (AgentScope Runtime)                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Resource  │  │    Safety   │  │   Logging   │          │
│  │  Management │  │   Monitor   │  │   System    │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Memory Layer                              │
│                    (ReMe Module)                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Local     │  │    Cloud    │  │   Semantic  │          │
│  │  Storage    │  │   Storage   │  │   Search    │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Extension Layer                           │
│                  (Skills System)                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Web       │  │    File     │  │   Custom    │          │
│  │   Scraping  │  │   Operations│  │   Skills    │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. AgentScope

**Role:** Agent Communication & Logic Framework

AgentScope is the foundational framework that coordinates agent interactions and decision-making modules.

#### Key Features

| Feature | Description |
|---------|-------------|
| **Multi-Agent Coordination** | Orchestrates multiple agents for complex tasks |
| **Message Routing** | Intelligent routing between agents and channels |
| **Task Decomposition** | Breaks down complex tasks into subtasks |
| **Response Aggregation** | Combines results from multiple agents |

#### Components

```
AgentScope
├── Agent Manager
│   ├── Agent Registry
│   ├── Agent Lifecycle
│   └── Agent Communication
├── Message Bus
│   ├── Message Queue
│   ├── Event System
│   └── Pub/Sub System
└── Task Orchestrator
    ├── Task Planner
    ├── Task Executor
    └── Task Monitor
```

### 2. AgentScope Runtime

**Role:** Execution & Resource Management

The runtime layer ensures stable operations and manages resource allocation.

#### Key Features

| Feature | Description |
|---------|-------------|
| **Resource Management** | CPU, memory, and GPU allocation |
| **Safety Monitor** | Prevents harmful operations |
| **Logging System** | Comprehensive audit trails |
| **Error Handling** | Graceful degradation and recovery |

#### Components

```
Runtime
├── Resource Manager
│   ├── CPU Scheduler
│   ├── Memory Manager
│   └── GPU Allocator
├── Safety Monitor
│   ├── Permission Checker
│   ├── Content Filter
│   └── Rate Limiter
└── Logging System
    ├── Event Logger
    ├── Audit Trail
    └── Metrics Collector
```

### 3. ReMe (Persistent Memory)

**Role:** Long-term Memory Module

ReMe addresses LLM statelessness by providing persistent memory storage.

#### Key Features

| Feature | Description |
|---------|-------------|
| **Persistent Storage** | Local or cloud-based storage |
| **Context Preservation** | Maintains user context across sessions |
| **Semantic Search** | Intelligent memory retrieval |
| **Experience Learning** | Agents learn and adapt over time |

#### Memory Structure

```
ReMe Memory System
├── Short-term Memory
│   ├── Conversation History
│   ├── Recent Context
│   └── Working State
├── Long-term Memory
│   ├── User Preferences
│   ├── Learned Patterns
│   └── Domain Knowledge
└── Semantic Index
    ├── Vector Embeddings
    ├── Keyword Index
    └── Relationship Graph
```

#### Storage Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| **JSONL** | Line-delimited JSON | Conversation logs |
| **Markdown** | Structured documents | Knowledge base |
| **Vector** | Embedding vectors | Semantic search |

---

## System Design

### Layer Architecture

#### 1. Connectivity Layer (All-Domain Access)

Unifies multiple communication channels into a single interface.

**Responsibilities:**
- Channel abstraction
- Message normalization
- Protocol adapters
- Authentication handling

**Supported Channels:**
- DingTalk
- Lark (Feishu)
- QQ
- Discord
- iMessage

#### 2. Agent Logic Layer

Core intelligence and decision-making.

**Responsibilities:**
- Intent recognition
- Task planning
- Agent coordination
- Response generation

**Agent Types:**
- **Planner Agent:** Breaks down complex tasks
- **Executor Agent:** Performs actions
- **Evaluator Agent:** Validates results
- **Specialist Agents:** Domain-specific tasks

#### 3. Runtime Layer

Execution environment and resource management.

**Responsibilities:**
- Process management
- Resource allocation
- Safety enforcement
- Error recovery

#### 4. Memory Layer

Persistent storage and retrieval.

**Responsibilities:**
- Data persistence
- Context management
- Semantic indexing
- Memory optimization

#### 5. Extension Layer (Skills)

Custom functionality and integrations.

**Responsibilities:**
- Skill execution
- API integrations
- File operations
- External services

---

## Data Flow

### Request Processing Flow

```
1. User Message (Channel)
         │
         ▼
2. Channel Adapter (Normalization)
         │
         ▼
3. Message Router (AgentScope)
         │
         ▼
4. Intent Recognition (LLM)
         │
         ▼
5. Memory Retrieval (ReMe)
         │
         ▼
6. Task Planning (Planner Agent)
         │
         ▼
7. Skill Execution (if needed)
         │
         ▼
8. Response Generation (LLM)
         │
         ▼
9. Memory Storage (ReMe)
         │
         ▼
10. Response Delivery (Channel)
```

### Memory Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Write      │────▶│   Index      │────▶│   Store      │
│   (Incoming) │     │  (Embedding) │     │  (Persist)   │
└──────────────┘     └──────────────┘     └──────────────┘
                            │
                            ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Retrieve   │◀────│   Search     │◀────│   Query      │
│   (Context)  │     │  (Semantic)  │     │  (Input)     │
└──────────────┘     └──────────────┘     └──────────────┘
```

---

## Extension Points

### Skills System

CoPaw's skill system allows developers to extend functionality through Python-based modules.

#### Skill Structure

```python
# Example skill structure
class MySkill:
    """Custom skill implementation"""
    
    def __init__(self, config):
        self.config = config
    
    def execute(self, input_data):
        """Execute the skill"""
        # Implementation
        return result
    
    def validate(self, input_data):
        """Validate input before execution"""
        # Validation logic
        return True
```

#### Skill Registration

Skills are registered in the configuration:

```yaml
skills:
  custom:
    - name: my_skill
      module: skills.my_skill
      config:
        api_key: ${API_KEY}
```

### Custom Agents

Developers can create custom agents for specific tasks:

```python
from agentscope.agents import BaseAgent

class CustomAgent(BaseAgent):
    """Custom agent for specific domain"""
    
    def __init__(self, name, config):
        super().__init__(name)
        self.config = config
    
    def reply(self, message):
        """Generate response"""
        # Custom logic
        return response
```

### Channel Adapters

New channels can be added through adapters:

```python
from copaw.channels import BaseChannel

class CustomChannel(BaseChannel):
    """Custom channel adapter"""
    
    def receive(self):
        """Receive messages"""
        # Implementation
        pass
    
    def send(self, message):
        """Send messages"""
        # Implementation
        pass
```

### Memory Backends

Custom memory backends can be implemented:

```python
from copaw.memory import BaseMemory

class CustomMemory(BaseMemory):
    """Custom memory backend"""
    
    def store(self, key, value):
        """Store memory"""
        pass
    
    def retrieve(self, key):
        """Retrieve memory"""
        pass
    
    def search(self, query):
        """Semantic search"""
        pass
```

---

## Configuration Architecture

### Configuration Hierarchy

```
Configuration
├── System Level
│   ├── Global Settings
│   ├── Environment Variables
│   └── Default Values
├── User Level
│   ├── User Preferences
│   ├── API Keys
│   └── Custom Settings
└── Session Level
    ├── Runtime Settings
    ├── Temporary State
    └── Override Values
```

### Configuration Sources (Priority Order)

1. **Command-line arguments** (highest priority)
2. **Environment variables**
3. **User configuration file** (`~/.copaw/config.yaml`)
4. **System configuration file** (`/etc/copaw/config.yaml`)
5. **Default values** (lowest priority)

---

## Security Architecture

### Security Layers

```
┌─────────────────────────────────────────┐
│         User Authentication              │
│    (Channel-specific auth)               │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│         API Key Management               │
│    (Encrypted storage)                   │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│         Permission System                │
│    (Skill-level permissions)             │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│         Content Filtering                │
│    (Safety monitoring)                   │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│         Data Encryption                  │
│    (At rest and in transit)              │
└─────────────────────────────────────────┘
```

### Security Features

| Feature | Description |
|---------|-------------|
| **API Key Encryption** | Keys stored encrypted |
| **Permission Scoping** | Skills have limited permissions |
| **Audit Logging** | All actions logged |
| **Rate Limiting** | Prevents abuse |
| **Content Filtering** | Blocks harmful content |

---

## Performance Considerations

### Optimization Strategies

| Area | Strategy |
|------|----------|
| **Memory** | Caching, lazy loading, compression |
| **Compute** | Async execution, parallel processing |
| **Network** | Connection pooling, retry logic |
| **Storage** | Indexing, partitioning, compaction |

### Scaling

CoPaw supports horizontal scaling through:

- **Multi-instance deployment** (Docker/Kubernetes)
- **Distributed memory** (Redis/Cloud storage)
- **Load balancing** (Reverse proxy)
- **Message queuing** (RabbitMQ/Kafka)

---

## Next Steps

- [Skills Development](../skills/README.md) - Create custom skills
- [Configuration Guide](../configuration/README.md) - Configure CoPaw
- [Use Cases](../use-cases/README.md) - Real-world examples

---

*Last updated: March 2026*
