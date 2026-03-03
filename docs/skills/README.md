# CoPaw Skills Development Guide

This guide covers everything you need to know about developing, extending, and sharing skills for CoPaw.

---

## Table of Contents

- [What are Skills?](#what-are-skills)
- [Skill Architecture](#skill-architecture)
- [Creating Your First Skill](#creating-your-first-skill)
- [Skill Types](#skill-types)
- [Advanced Skills](#advanced-skills)
- [Testing Skills](#testing-skills)
- [Sharing Skills](#sharing-skills)
- [Best Practices](#best-practices)

---

## What are Skills?

**Skills** are Python-based modules that extend CoPaw's capabilities. They allow you to:

- 🔌 Integrate with external APIs and services
- 📁 Perform file and desktop operations
- 🌐 Scrape web content
- 🤖 Create custom AI workflows
- 📊 Process and analyze data

### Key Characteristics

| Characteristic | Description |
|----------------|-------------|
| **Modular** | Each skill is a self-contained module |
| **Python-based** | Written in Python for flexibility |
| **Standardized** | Follows a common interface specification |
| **Composable** | Skills can be combined for complex workflows |
| **Secure** | Permission-based execution model |

---

## Skill Architecture

### Skill Structure

```
my_skill/
├── __init__.py          # Package initialization
├── skill.py             # Main skill implementation
├── config.yaml          # Skill configuration
├── requirements.txt     # Dependencies
└── README.md            # Skill documentation
```

### Skill Interface

```python
from copaw.skills import BaseSkill

class MySkill(BaseSkill):
    """Custom skill implementation"""
    
    # Skill metadata
    name = "my_skill"
    version = "1.0.0"
    description = "Description of what the skill does"
    
    def __init__(self, config=None):
        """Initialize the skill"""
        super().__init__(config)
        # Setup code here
    
    async def execute(self, input_data: dict) -> dict:
        """
        Execute the skill
        
        Args:
            input_data: Input parameters
            
        Returns:
            dict: Execution result
        """
        # Implementation
        return {"result": "success"}
    
    def validate(self, input_data: dict) -> bool:
        """
        Validate input before execution
        
        Args:
            input_data: Input parameters
            
        Returns:
            bool: Whether input is valid
        """
        # Validation logic
        return True
```

---

## Creating Your First Skill

### Step 1: Set Up Development Environment

```bash
# Create skills directory
mkdir -p ~/.copaw/skills

# Navigate to skills directory
cd ~/.copaw/skills

# Create skill directory
mkdir my_first_skill
cd my_first_skill
```

### Step 2: Create Skill Files

**`__init__.py`:**
```python
from .skill import MyFirstSkill

__all__ = ["MyFirstSkill"]
```

**`skill.py`:**
```python
from copaw.skills import BaseSkill

class MyFirstSkill(BaseSkill):
    """My first CoPaw skill - A simple greeting skill"""
    
    name = "my_first_skill"
    version = "1.0.0"
    description = "Returns a personalized greeting"
    
    async def execute(self, input_data: dict) -> dict:
        name = input_data.get("name", "World")
        greeting = f"Hello, {name}! Welcome to CoPaw!"
        
        return {
            "success": True,
            "message": greeting,
            "data": {
                "greeting": greeting,
                "name": name
            }
        }
```

**`config.yaml`:**
```yaml
name: my_first_skill
version: 1.0.0
description: Returns a personalized greeting
author: Your Name

# Configuration schema
config_schema:
  properties:
    default_name:
      type: string
      default: "World"
      description: Default name to use if not provided

# Required permissions
permissions:
  - read:input
```

### Step 3: Register the Skill

Add to your CoPaw configuration (`~/.copaw/config.yaml`):

```yaml
skills:
  custom:
    - name: my_first_skill
      path: ~/.copaw/skills/my_first_skill
      config:
        default_name: "Friend"
```

### Step 4: Test the Skill

```bash
# Reload skills
copaw skills reload

# Test the skill
copaw skills test my_first_skill --input '{"name": "Alice"}'
```

Expected output:
```json
{
  "success": true,
  "message": "Hello, Alice! Welcome to CoPaw!",
  "data": {
    "greeting": "Hello, Alice! Welcome to CoPaw!",
    "name": "Alice"
  }
}
```

---

## Skill Types

### 1. Web Scraping Skills

Extract information from websites:

```python
import aiohttp
from bs4 import BeautifulSoup
from copaw.skills import BaseSkill

class WebScraperSkill(BaseSkill):
    """Scrape and summarize web content"""
    
    name = "web_scraper"
    description = "Extract content from URLs"
    
    async def execute(self, input_data: dict) -> dict:
        url = input_data.get("url")
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract title
                title = soup.find('title')
                title_text = title.string if title else "No title"
                
                # Extract main content
                content = self._extract_content(soup)
                
                return {
                    "success": True,
                    "data": {
                        "url": url,
                        "title": title_text,
                        "content": content
                    }
                }
    
    def _extract_content(self, soup):
        """Extract main content from HTML"""
        # Implementation
        pass
```

### 2. File Operation Skills

Manipulate files and directories:

```python
import os
import shutil
from pathlib import Path
from copaw.skills import BaseSkill

class FileOperatorSkill(BaseSkill):
    """Perform file operations"""
    
    name = "file_operator"
    description = "Create, read, update, delete files"
    
    async def execute(self, input_data: dict) -> dict:
        operation = input_data.get("operation")
        path = input_data.get("path")
        
        if operation == "read":
            return await self._read_file(path)
        elif operation == "write":
            content = input_data.get("content")
            return await self._write_file(path, content)
        elif operation == "delete":
            return await self._delete_file(path)
        elif operation == "list":
            return await self._list_directory(path)
        else:
            return {"success": False, "error": "Unknown operation"}
    
    async def _read_file(self, path: str) -> dict:
        try:
            with open(path, 'r') as f:
                content = f.read()
            return {"success": True, "content": content}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _write_file(self, path: str, content: str) -> dict:
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
            return {"success": True, "message": "File written"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _delete_file(self, path: str) -> dict:
        try:
            os.remove(path)
            return {"success": True, "message": "File deleted"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _list_directory(self, path: str) -> dict:
        try:
            items = os.listdir(path)
            return {"success": True, "items": items}
        except Exception as e:
            return {"success": False, "error": str(e)}
```

### 3. API Integration Skills

Connect to external services:

```python
import aiohttp
from copaw.skills import BaseSkill

class WeatherSkill(BaseSkill):
    """Get weather information from API"""
    
    name = "weather"
    description = "Fetch current weather for a location"
    
    async def execute(self, input_data: dict) -> dict:
        location = input_data.get("location")
        api_key = self.config.get("api_key")
        
        url = f"https://api.weather.com/weather/{location}"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": {
                            "location": location,
                            "temperature": data.get("temp"),
                            "condition": data.get("condition"),
                            "humidity": data.get("humidity")
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Weather API error: {response.status}"
                    }
```

### 4. Data Processing Skills

Analyze and transform data:

```python
import json
import pandas as pd
from copaw.skills import BaseSkill

class DataAnalyzerSkill(BaseSkill):
    """Analyze data and generate insights"""
    
    name = "data_analyzer"
    description = "Perform data analysis on datasets"
    
    async def execute(self, input_data: dict) -> dict:
        data = input_data.get("data")
        operation = input_data.get("operation")
        
        if isinstance(data, str):
            data = json.loads(data)
        
        df = pd.DataFrame(data)
        
        if operation == "summary":
            return {
                "success": True,
                "data": {
                    "rows": len(df),
                    "columns": len(df.columns),
                    "column_names": list(df.columns),
                    "statistics": df.describe().to_dict()
                }
            }
        elif operation == "filter":
            column = input_data.get("column")
            value = input_data.get("value")
            filtered = df[df[column] == value]
            return {
                "success": True,
                "data": filtered.to_dict('records')
            }
        else:
            return {"success": False, "error": "Unknown operation"}
```

### 5. Agentic Workflow Skills

Create autonomous workflows:

```python
from copaw.skills import BaseSkill
from copaw.agents import AgentExecutor

class AgenticWorkflowSkill(BaseSkill):
    """Execute multi-step agentic workflow"""
    
    name = "agentic_workflow"
    description = "Run autonomous agent workflows"
    
    async def execute(self, input_data: dict) -> dict:
        task = input_data.get("task")
        
        # Initialize agent executor
        executor = AgentExecutor()
        
        # Define workflow steps
        workflow = [
            {"agent": "planner", "action": "decompose", "input": task},
            {"agent": "researcher", "action": "gather_info"},
            {"agent": "analyst", "action": "analyze"},
            {"agent": "writer", "action": "synthesize"}
        ]
        
        # Execute workflow
        results = []
        for step in workflow:
            result = await executor.execute(step)
            results.append(result)
        
        return {
            "success": True,
            "data": {
                "task": task,
                "results": results,
                "final_output": results[-1]
            }
        }
```

---

## Advanced Skills

### Skill with State Management

```python
from copaw.skills import BaseSkill

class StatefulSkill(BaseSkill):
    """Skill that maintains state across invocations"""
    
    name = "stateful_skill"
    description = "Maintains conversation state"
    
    def __init__(self, config=None):
        super().__init__(config)
        self.state = {}
    
    async def execute(self, input_data: dict) -> dict:
        session_id = input_data.get("session_id", "default")
        
        # Load or initialize state
        if session_id not in self.state:
            self.state[session_id] = {"count": 0, "history": []}
        
        # Update state
        self.state[session_id]["count"] += 1
        self.state[session_id]["history"].append(input_data)
        
        return {
            "success": True,
            "data": {
                "session_id": session_id,
                "count": self.state[session_id]["count"],
                "message": f"This is invocation #{self.state[session_id]['count']}"
            }
        }
```

### Skill with Caching

```python
import hashlib
import json
from functools import wraps
from copaw.skills import BaseSkill

class CachedSkill(BaseSkill):
    """Skill with result caching"""
    
    name = "cached_skill"
    description = "Caches results for performance"
    
    def __init__(self, config=None):
        super().__init__(config)
        self.cache = {}
        self.cache_ttl = config.get("cache_ttl", 3600)
    
    def _get_cache_key(self, input_data: dict) -> str:
        data_str = json.dumps(input_data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    async def execute(self, input_data: dict) -> dict:
        cache_key = self._get_cache_key(input_data)
        
        # Check cache
        if cache_key in self.cache:
            cached_result = self.cache[cache_key]
            if self._is_valid(cached_result):
                return {
                    "success": True,
                    "data": cached_result["result"],
                    "from_cache": True
                }
        
        # Execute and cache
        result = await self._compute(input_data)
        self.cache[cache_key] = {
            "result": result,
            "timestamp": self._now()
        }
        
        return {
            "success": True,
            "data": result,
            "from_cache": False
        }
    
    async def _compute(self, input_data: dict):
        # Actual computation
        pass
    
    def _is_valid(self, cached_result: dict) -> bool:
        return (self._now() - cached_result["timestamp"]) < self.cache_ttl
    
    def _now(self) -> int:
        import time
        return int(time.time())
```

### Skill with Error Handling

```python
from copaw.skills import BaseSkill
from copaw.exceptions import SkillError

class RobustSkill(BaseSkill):
    """Skill with comprehensive error handling"""
    
    name = "robust_skill"
    description = "Handles errors gracefully"
    
    async def execute(self, input_data: dict) -> dict:
        try:
            # Validate input
            self._validate_input(input_data)
            
            # Execute with retry
            result = await self._execute_with_retry(input_data)
            
            return {
                "success": True,
                "data": result
            }
            
        except ValueError as e:
            return {
                "success": False,
                "error": "Invalid input",
                "details": str(e)
            }
        except TimeoutError as e:
            return {
                "success": False,
                "error": "Operation timed out",
                "retryable": True
            }
        except Exception as e:
            return {
                "success": False,
                "error": "Unexpected error",
                "details": str(e),
                "type": type(e).__name__
            }
    
    def _validate_input(self, input_data: dict):
        if "required_field" not in input_data:
            raise ValueError("Missing required_field")
    
    async def _execute_with_retry(self, input_data: dict, max_retries=3):
        for attempt in range(max_retries):
            try:
                return await self._do_execute(input_data)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                await self._wait_backoff(attempt)
    
    async def _do_execute(self, input_data: dict):
        # Actual implementation
        pass
    
    async def _wait_backoff(self, attempt: int):
        import asyncio
        wait_time = 2 ** attempt  # Exponential backoff
        await asyncio.sleep(wait_time)
```

---

## Testing Skills

### Unit Testing

Create `tests/test_my_skill.py`:

```python
import pytest
import asyncio
from my_skill.skill import MyFirstSkill

class TestMyFirstSkill:
    
    @pytest.fixture
    def skill(self):
        return MyFirstSkill(config={"default_name": "Test"})
    
    def test_basic_greeting(self, skill):
        input_data = {"name": "Alice"}
        result = asyncio.run(skill.execute(input_data))
        
        assert result["success"] is True
        assert "Alice" in result["message"]
        assert result["data"]["name"] == "Alice"
    
    def test_default_name(self, skill):
        input_data = {}
        result = asyncio.run(skill.execute(input_data))
        
        assert result["success"] is True
        assert "Test" in result["message"]
    
    def test_validation(self, skill):
        input_data = {"name": 123}  # Invalid type
        result = asyncio.run(skill.execute(input_data))
        
        assert result["success"] is False
```

### Integration Testing

```bash
# Test skill in CoPaw context
copaw skills test my_first_skill --input '{"name": "Bob"}'

# Test with verbose output
copaw skills test my_first_skill --input '{"name": "Bob"}' --verbose

# Test performance
copaw skills benchmark my_first_skill --iterations 100
```

---

## Sharing Skills

### Publishing to Skills Hub

1. **Prepare Your Skill**
   - Ensure all files are in place
   - Write comprehensive README
   - Add tests
   - Version your skill

2. **Create Package**

```bash
# Package skill
copaw skills package my_first_skill

# This creates: my_first_skill-1.0.0.zip
```

3. **Submit to Skills Hub**

```bash
# Submit to community hub
copaw skills publish my_first_skill-1.0.0.zip --hub skills.sh

# Or to ClawHub
copaw skills publish my_first_skill-1.0.0.zip --hub clawhub.ai
```

### Skill Metadata

Include in your `config.yaml`:

```yaml
# Publishing metadata
publishing:
  license: MIT
  repository: https://github.com/yourusername/my-skill
  documentation: https://your-docs-url.com
  tags:
    - utility
    - productivity
    - automation
```

---

## Best Practices

### Code Quality

✅ **Do:**
- Follow PEP 8 style guidelines
- Add type hints
- Write docstrings
- Handle errors gracefully
- Log important operations

❌ **Don't:**
- Hardcode credentials
- Block the event loop
- Ignore exceptions
- Skip input validation

### Security

```python
# ✅ Good: Validate and sanitize input
def validate_input(self, data: dict):
    if not isinstance(data.get("path"), str):
        raise ValueError("Path must be a string")
    if ".." in data["path"]:
        raise ValueError("Invalid path traversal")

# ❌ Bad: Trust user input
def bad_validate(self, data: dict):
    path = data["path"]  # No validation!
    open(path, 'r')  # Dangerous!
```

### Performance

```python
# ✅ Good: Async I/O
async def good_fetch(self, urls: list):
    async with aiohttp.ClientSession() as session:
        tasks = [self._fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# ❌ Bad: Blocking I/O
async def bad_fetch(self, urls: list):
    results = []
    for url in urls:
        response = requests.get(url)  # Blocking!
        results.append(response)
    return results
```

### Documentation

Include in your skill's README:

```markdown
# My Skill

## Description
Brief description of what the skill does.

## Installation
```bash
copaw skills install my_skill
```

## Configuration
```yaml
skills:
  my_skill:
    api_key: ${API_KEY}
```

## Usage
```python
result = await skill.execute({"param": "value"})
```

## Examples
- Example 1
- Example 2

## API Reference
Document all methods and parameters.
```

---

## Next Steps

- [Use Cases](../use-cases/README.md) - See skills in action
- [Architecture](../architecture/README.md) - Understand skill integration
- [Community Skills](https://skills.sh) - Browse existing skills

---

*Last updated: March 2026*
