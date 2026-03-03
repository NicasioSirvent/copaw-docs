# Contributing to CoPaw Documentation

Thank you for your interest in contributing to CoPaw documentation! This guide will help you get started.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Documentation Standards](#documentation-standards)
- [Pull Request Process](#pull-request-process)
- [Style Guide](#style-guide)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Our Standards

✅ **Do:**
- Be welcoming and inclusive
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

❌ **Don't:**
- Use sexualized language or imagery
- Make personal or political attacks
- Engage in trolling or insulting comments
- Harass others

---

## How to Contribute

### Ways to Contribute

1. **📝 Write Documentation**
   - Add new guides
   - Improve existing content
   - Add examples and use cases

2. **🐛 Report Issues**
   - Find bugs in documentation
   - Suggest improvements
   - Report outdated information

3. **🔧 Create Skills**
   - Develop new skills
   - Improve existing skills
   - Share with the community

4. **💡 Share Use Cases**
   - Document real-world scenarios
   - Share best practices
   - Create tutorials

5. **🌍 Translate**
   - Translate documentation
   - Improve translations
   - Add language support

### Getting Started

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone
   git clone https://github.com/your-username/copaw-docs.git
   cd copaw-docs
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow documentation standards
   - Test your changes
   - Add examples where applicable

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: your descriptive commit message"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   # Then create a Pull Request on GitHub
   ```

---

## Documentation Standards

### Structure

Each documentation file should follow this structure:

```markdown
# Title

Brief introduction (1-2 paragraphs)

---

## Table of Contents

- [Section 1](#section-1)
- [Section 2](#section-2)

---

## Section 1

Content with examples

## Section 2

More content

---

*Last updated: Month Year*
```

### Content Guidelines

#### Be Clear and Concise

✅ **Good:**
```markdown
Install CoPaw with pip:
```bash
pip install copaw
```
```

❌ **Bad:**
```markdown
So you want to install CoPaw, well there are many ways to do it but the best way is probably using pip which is a package manager...
```

#### Use Active Voice

✅ **Good:**
```markdown
Configure your API key in the settings.
```

❌ **Bad:**
```markdown
The API key should be configured in the settings.
```

#### Provide Examples

✅ **Good:**
```markdown
Set environment variables:
```bash
export DASHSCOPE_API_KEY=sk-xxxxxxxx
copaw init
```
```

❌ **Bad:**
```markdown
You need to set up your environment variables somehow.
```

#### Use Tables for Comparisons

✅ **Good:**
```markdown
| Method | Best For | Difficulty |
|--------|----------|------------|
| One-Click | Beginners | Easy |
| pip | Developers | Medium |
| Docker | Enterprise | Advanced |
```

❌ **Bad:**
```markdown
One-click is good for beginners, pip is for developers, and Docker is advanced.
```

---

## Pull Request Process

### Before Submitting

- [ ] Check for typos and grammar errors
- [ ] Verify all links work
- [ ] Test code examples
- [ ] Ensure consistent formatting
- [ ] Add yourself to contributors (if applicable)

### PR Title Format

Use conventional commits style:

```
docs: Add installation guide for Windows
docs: Fix broken links in architecture doc
docs: Update configuration examples
```

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New documentation
- [ ] Bug fix
- [ ] Improvement
- [ ] Translation

## Checklist
- [ ] I have read the contributing guide
- [ ] My changes follow the style guide
- [ ] I have tested my changes
- [ ] I have updated relevant documentation

## Related Issues
Fixes #123
```

### Review Process

1. **Automated Checks**
   - Link validation
   - Spell check
   - Format validation

2. **Maintainer Review**
   - Content accuracy
   - Style compliance
   - Clarity and completeness

3. **Community Feedback**
   - Open for community comments
   - Address feedback
   - Iterate on changes

4. **Merge**
   - Approved by maintainer
   - All checks pass
   - Merged to main branch

---

## Style Guide

### Markdown Style

#### Headers

```markdown
# Page Title (H1)

## Section (H2)

### Subsection (H3)

#### Sub-subsection (H4)
```

#### Code Blocks

Use language-specific syntax highlighting:

````markdown
```python
def hello():
    print("Hello, CoPaw!")
```

```bash
copaw init
```

```yaml
models:
  default:
    provider: dashscope
```
````

#### Emphasis

```markdown
**Bold** for important items
*Italic* for emphasis
`Inline code` for technical terms
> Blockquotes for notes
```

#### Lists

```markdown
- Unordered list item
- Another item
  - Nested item

1. Ordered list item
2. Another item
   1. Nested item
```

#### Links

```markdown
[Link Text](URL)

[Internal Link](../other-doc.md)

[External Link](https://example.com)
```

#### Images

```markdown
![Alt Text](image.png "Caption")
```

### Writing Style

#### Tone

- **Professional but friendly**
- **Inclusive and welcoming**
- **Clear and direct**
- **Avoid jargon when possible**

#### Terminology

| Term | Usage |
|------|-------|
| CoPaw | Always capitalize as "CoPaw" |
| AgentScope | Proper noun, capitalize |
| ReMe | Proper noun, capitalize |
| skill | Lowercase unless starting a sentence |
| channel | Lowercase unless starting a sentence |

#### Commands and Paths

- Use `code formatting` for commands, paths, and technical terms
- Show full commands with context
- Include expected output when helpful

✅ **Good:**
```markdown
Run `copaw init` to initialize configuration.
Configuration is saved to `~/.copaw/config.yaml`.
```

❌ **Bad:**
```markdown
Run copaw init to initialize. Config is saved in a file somewhere.
```

---

## Contributing Skills

### Skill Submission Requirements

1. **Working Code**
   - Skill executes successfully
   - No hardcoded credentials
   - Error handling implemented

2. **Documentation**
   - README with usage instructions
   - Configuration examples
   - Usage examples

3. **Tests**
   - Basic test coverage
   - Test instructions

4. **License**
   - Compatible with Apache 2.0
   - Clear licensing information

### Skill Template

```
my_skill/
├── __init__.py
├── skill.py
├── config.yaml
├── requirements.txt
├── README.md
└── tests/
    └── test_skill.py
```

---

## Reporting Issues

### Bug Report Template

```markdown
**Description:**
Clear description of the issue

**Location:**
- Page/Section: [URL or file path]
- Specific content: [quote or reference]

**Expected:**
What should it say/do?

**Actual:**
What does it say/do?

**Suggestion:**
How should it be fixed?
```

### Feature Request Template

```markdown
**Problem:**
What problem does this solve?

**Proposal:**
What should be added/changed?

**Benefits:**
Who benefits from this?

**Alternatives:**
What alternatives exist?
```

---

## Questions?

### Getting Help

- **Discussions:** GitHub Discussions
- **Issues:** For specific problems
- **Email:** Documentation maintainers

### Common Questions

**Q: Can I contribute if I'm not a native English speaker?**

A: Absolutely! We welcome contributions in all languages. Translation contributions are especially valuable.

**Q: Do I need to be a CoPaw expert?**

A: No! If you found something confusing, that's valuable feedback. Often, newcomers spot issues experts miss.

**Q: How long does review take?**

A: Typically 1-2 weeks. Complex changes may take longer.

**Q: Can I contribute anonymously?**

A: We prefer credited contributions for recognition, but anonymous contributions are accepted.

---

## Contributors

Thank you to all our contributors! 🎉

<!-- Add your name here when you contribute -->
- Original Documentation Team
- You? (Submit a PR!)

---

## License

By contributing, you agree that your contributions will be licensed under the Apache 2.0 License.

---

*Last updated: March 2026*
