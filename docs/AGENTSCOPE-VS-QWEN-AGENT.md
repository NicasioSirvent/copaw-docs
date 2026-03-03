# AgentScope vs qwen-agent: Framework Comparison

Understanding the relationship between Alibaba's agent frameworks and CoPaw.

---

## Table of Contents

- [Overview](#overview)
- [Quick Comparison](#quick-comparison)
- [Detailed Comparison](#detailed-comparison)
- [Architecture Comparison](#architecture-comparison)
- [When to Use Which](#when-to-use-which)
- [How They Work Together](#how-they-work-together)
- [Relationship to CoPaw](#relationship-to-copaw)

---

## Overview

Both **AgentScope** and **qwen-agent** are open-source agent frameworks from Alibaba, but they serve **different purposes** and have **complementary capabilities**.

### Official Position

From the Qwen-Agent team (GitHub Issue #201):

> **"qwen-agent 和 agentscope 是互补关系，目前两者的功能重叠度并不高"**
> 
> *"qwen-agent and AgentScope are **complementary**. Their functional overlap is not high."*

> **"可以通过在 agentscope 里 import qwen-agent 来结合使用"**
> 
> *"You can use them together by importing qwen-agent in AgentScope"*

---

## Quick Comparison

| Aspect | **qwen-agent** | **AgentScope** | **CoPaw** |
|--------|----------------|----------------|-----------|
| **Primary Focus** | Single-agent applications | Multi-agent orchestration | Personal AI assistant |
| **Team** | Qwen model algorithm team | Alibaba Tongyi Lab | Alibaba Tongyi Lab |
| **GitHub Stars** | ~13.5k | ~16.9k | Growing |
| **License** | Apache 2.0 | Apache 2.0 | Apache 2.0 |
| **Model Support** | Qwen-optimized | Multi-provider | Multi-provider |
| **Key Features** | Function Calling, MCP, Code Interpreter, RAG | MsgHub, Multi-agent workflows, RL | Channels, Skills, Memory |
| **Best For** | Qwen-specific apps | Multi-agent systems | Personal assistant |

---

## Detailed Comparison

### qwen-agent

**Purpose:** Framework for developing LLM applications based on Qwen≥3.0 capabilities

**Key Features:**
- ✅ **Function Calling**: Parallel, multi-step, multi-turn tool calls
- ✅ **MCP (Model Context Protocol)**: External tool integration
- ✅ **Code Interpreter**: Docker-based sandboxed execution
- ✅ **RAG**: 1M-token context question-answering
- ✅ **Chrome Extension**: BrowserQwen browser assistant
- ✅ **Gradio GUI**: Built-in web UI
- ✅ **Multi-Modal**: Qwen3-VL support (image search, zoom)

**Architecture:**
```
qwen-agent
├── Agents
│   ├── Assistant
│   ├── FnCallAgent
│   └── ReActChat
├── LLMs (Qwen-optimized)
│   ├── BaseChatModel
│   └── Function Calling
├── Tools
│   ├── BaseTool
│   ├── MCP Tools
│   └── Code Interpreter
└── Infrastructure
    ├── DashScope API
    ├── Docker Sandbox
    └── MCP Servers
```

**Use Cases:**
- Qwen Chat backend
- Browser assistant (Chrome extension)
- Code interpreter applications
- Long-document QA (1M tokens)
- Custom Qwen-powered assistants

---

### AgentScope

**Purpose:** Developer-centric framework for multi-agent AI development

**Key Features:**
- ✅ **Multi-Agent Workflows**: MsgHub for agent communication
- ✅ **Tool Integration**: MCP, Anthropic skills, Python/shell
- ✅ **Memory Systems**: ReMe long-term memory, compression
- ✅ **Voice Support**: Real-time voice agents with TTS
- ✅ **Agentic RL**: Reinforcement learning with Trinity-RFT
- ✅ **Production Deployment**: Local, cloud, Kubernetes
- ✅ **OpenTelemetry**: Built-in observability

**Architecture:**
```
AgentScope
├── Agents
│   ├── ReActAgent
│   ├── UserAgent
│   ├── VoiceAgent
│   └── Custom Agents
├── MsgHub (Multi-agent router)
├── Tools
│   ├── MCP Tools
│   ├── Python/Shell
│   └── Custom Tools
├── Memory
│   ├── InMemoryMemory
│   ├── ReMe (long-term)
│   └── SQLite
├── Models
│   ├── DashScope
│   ├── OpenAI
│   └── Other providers
└── Pipeline
    ├── Sequential
    ├── Concurrent
    └── MsgHub
```

**Use Cases:**
- Multi-agent collaboration
- Agent simulation & research
- CoPaw personal assistant
- Production agentic applications
- Agentic RL training

---

## Architecture Comparison

### Design Philosophy

#### qwen-agent: **Model-Centric**
```
┌─────────────────────────────────────┐
│         Qwen-Agent                   │
│  ┌─────────────────────────────────┐│
│  │  Assistant / FnCallAgent / ReAct ││
│  └──────────────┬──────────────────┘│
│                 │                    │
│  ┌──────────────▼──────────────────┐│
│  │  Qwen LLM (optimized)           ││
│  │  + Function Calling             ││
│  │  + MCP Tools                    ││
│  │  + Code Interpreter             ││
│  │  + RAG (1M context)             ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

**Focus:** Maximize Qwen model capabilities

#### AgentScope: **Orchestration-Centric**
```
┌─────────────────────────────────────┐
│         AgentScope                   │
│  ┌─────────┐  ┌─────────┐  ┌──────┐│
│  │ Agent 1 │  │ Agent 2 │  │ ... ││
│  └────┬────┘  └────┬────┘  └──┬───┘│
│       └────────────┼───────────┘   │
│                    │                │
│       ┌────────────▼────────────┐  │
│       │    MsgHub (Router)      │  │
│       └────────────┬────────────┘  │
│                    │                │
│  ┌─────────────────▼─────────────┐ │
│  │  Models | Tools | Memory      │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

**Focus:** Coordinate multiple agents effectively

---

## When to Use Which

### Use qwen-agent when:

| ✅ | Scenario |
|----|----------|
| ✅ | Building **Qwen-specific** applications |
| ✅ | Need **function calling** optimized for Qwen models |
| ✅ | Want **code interpreter** with Docker sandbox |
| ✅ | Need **1M-token context** RAG |
| ✅ | Building **Qwen Chat**-like applications |
| ✅ | Want **Chrome extension** (BrowserQwen) |
| ✅ | Need **Gradio GUI** out of the box |
| ✅ | Single-agent task automation |

**Example Projects:**
- Document QA system with 1M-token context
- Code interpreter web service
- Qwen-powered customer support bot
- Browser assistant extension

---

### Use AgentScope when:

| ✅ | Scenario |
|----|----------|
| ✅ | Building **multi-agent** applications |
| ✅ | Need **agent-to-agent** communication |
| ✅ | Want **production deployment** (K8s, cloud) |
| ✅ | Need **agentic RL** (reinforcement learning) |
| ✅ | Building **CoPaw**-like personal assistants |
| ✅ | Want **multi-model** support (not just Qwen) |
| ✅ | Need **OpenTelemetry** observability |
| ✅ | Multi-agent simulation or research |

**Example Projects:**
- CoPaw personal AI assistant
- Multi-agent debate system
- Collaborative problem-solving agents
- Production agentic workflows

---

### Use Both when:

| ✅ | Scenario |
|----|----------|
| ✅ | Multi-agent system with Qwen-optimized single agents |
| ✅ | Want best of both worlds |
| ✅ | Need Qwen capabilities + multi-agent orchestration |

**Example Integration:**
```python
# Use qwen-agent's specialized agents within AgentScope
from qwen_agent.agents import Assistant
from agentscope.agent import ReActAgent, MsgHub

# Create qwen-agent powered specialist
qwen_coder = Assistant(
    llm={'model': 'qwen-coder-latest'},
    function_list=['code_interpreter']
)

# Create AgentScope coordinator
coordinator = ReActAgent(name="coordinator", ...)

# Use in multi-agent workflow
async def workflow():
    # Coordinator delegates to qwen specialist
    result = await qwen_coder(code_task)
    return await coordinator(result)
```

---

## How They Work Together

### Integration Pattern

```
┌─────────────────────────────────────────────────────────┐
│              Combined Architecture                       │
│                                                          │
│  ┌──────────────────┐        ┌──────────────────┐       │
│  │   qwen-agent     │        │    AgentScope    │       │
│  │                  │        │                  │       │
│  │  Specialist      │        │  Orchestrator    │       │
│  │  Agents          │        │  (MsgHub)        │       │
│  │  • Code          │        │                  │       │
│  │  • RAG           │        │  • Routing       │       │
│  │  • Function Call │        │  • Coordination  │       │
│  └────────┬─────────┘        └─────────┬────────┘       │
│           │                            │                 │
│           └────────────┬───────────────┘                 │
│                        │                                  │
│              Combined Workflow                            │
└─────────────────────────────────────────────────────────┘
```

### Example Code

```python
from agentscope.agent import ReActAgent, MsgHub
from agentscope.memory import InMemoryMemory
from qwen_agent.agents import Assistant

# Create qwen-agent specialist (code interpreter)
qwen_coder = Assistant(
    name="Coder",
    llm={'model': 'qwen-coder-latest', 'model_type': 'qwen_dashscope'},
    function_list=['code_interpreter', 'mcp']
)

# Create AgentScope agents
coordinator = ReActAgent(
    name="Coordinator",
    sys_prompt="You coordinate tasks between specialists.",
    model="dashscope-qwen-max",
    memory=InMemoryMemory()
)

researcher = ReActAgent(
    name="Researcher",
    sys_prompt="You research and gather information.",
    model="dashscope-qwen-max",
    memory=InMemoryMemory()
)

# Create message hub for multi-agent conversation
async with MsgHub(
    participants=[coordinator, researcher],
    name="Project Team"
) as hub:
    # Coordinator can delegate to qwen specialist
    await hub.send({
        "from": "coordinator",
        "content": "Write code to analyze this data",
        "target": "Coder"  # qwen-agent specialist
    })
```

---

## Relationship to CoPaw

### CoPaw's Architecture

**CoPaw** is built on **AgentScope**, not qwen-agent:

```
┌─────────────────────────────────────────────────────────┐
│                      CoPaw                               │
│  (Personal AI Assistant Application)                     │
└─────────────────────────────────────────────────────────┘
         ▲
         │ Uses
         │
┌─────────────────────────────────────────────────────────┐
│                    AgentScope                            │
│  (Multi-Agent Framework)                                 │
│  • Agent orchestration                                   │
│  • Message routing (MsgHub)                              │
│  • Memory management (ReMe)                              │
│  • Tool execution                                        │
└─────────────────────────────────────────────────────────┘
         ▲
         │ Could integrate
         │
┌─────────────────────────────────────────────────────────┐
│                   qwen-agent                             │
│  (Qwen-optimized single-agent framework)                 │
│  • Code interpreter                                      │
│  • Function calling                                      │
│  • RAG (1M context)                                      │
└─────────────────────────────────────────────────────────┘
```

### Why CoPaw Uses AgentScope

| Reason | Explanation |
|--------|-------------|
| **Multi-Agent Support** | CoPaw needs multiple specialized agents working together |
| **Channel Integration** | AgentScope's architecture supports multiple input channels |
| **Memory Management** | ReMe provides persistent memory across sessions |
| **Production Deployment** | AgentScope supports K8s, cloud, OpenTelemetry |
| **Flexibility** | Works with multiple model providers, not just Qwen |

### Potential Integration

CoPaw **could** integrate qwen-agent for specialized tasks:

```yaml
# Hypothetical CoPaw config with qwen-agent integration
skills:
  code_interpreter:
    backend: qwen-agent
    model: qwen-coder-latest
    features:
      - docker_sandbox
      - mcp
  
  research:
    backend: agentscope
    model: qwen-max
    features:
      - web_search
      - summarization
```

---

## Summary

### Key Takeaways

1. **Complementary, Not Competing**: qwen-agent and AgentScope solve different problems
2. **Different Focus**: 
   - qwen-agent = Qwen-optimized single-agent
   - AgentScope = Multi-agent orchestration
3. **Can Work Together**: Import qwen-agent capabilities in AgentScope
4. **CoPaw Uses AgentScope**: Built on AgentScope's multi-agent foundation
5. **Choose Based on Needs**:
   - Single-agent Qwen app → qwen-agent
   - Multi-agent system → AgentScope
   - Both → Use together!

### Quick Decision Tree

```
Need to build an AI agent application?
         │
         ├── Using Qwen models exclusively?
         │       │
         │       ├── Yes, single agent → qwen-agent ✅
         │       │
         │       └── No, multiple agents → AgentScope ✅
         │
         └── Need multi-agent orchestration?
                 │
                 └── Yes → AgentScope ✅
                     (optionally integrate qwen-agent for specialists)
```

---

## Resources

### qwen-agent
- **GitHub**: [QwenLM/qwen-agent](https://github.com/QwenLM/qwen-agent)
- **Docs**: [qwen.readthedocs.io](https://qwen.readthedocs.io/)
- **PyPI**: `pip install qwen-agent`

### AgentScope
- **GitHub**: [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope)
- **Docs**: [doc.agentscope.io](https://doc.agentscope.io/)
- **PyPI**: `pip install agentscope`

### CoPaw
- **GitHub**: [agentscope-ai/CoPaw](https://github.com/agentscope-ai/CoPaw)
- **Docs**: [copaw.agentscope.io](https://copaw.agentscope.io)

---

*Last updated: March 2026*
