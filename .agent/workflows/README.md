# Workflows

This directory contains reusable workflows for common tasks.

## Available Workflows

### `/universal-setup` - Transform Project to Universal Tool

Transforms any project into a universal, user-friendly, GitHub-ready tool that anyone can use with their own credentials.

**When to use:**
- Making a project open-source
- Removing hardcoded credentials
- Creating comprehensive documentation
- Building setup automation
- Preparing for GitHub publication

**What it creates:**
- 📘 SETUP.md - Complete setup guide
- 🔧 TROUBLESHOOTING.md - Common issues and solutions
- ❓ FAQ.md - Frequently asked questions
- 🔒 SECURITY.md - Security best practices
- 🤝 CONTRIBUTING.md - Contribution guidelines
- 🐍 setup_wizard.py - Interactive setup wizard
- ✅ validate_setup.py - Configuration validation
- 🔑 authenticate.py - OAuth/API authentication helper
- 📝 Enhanced README.md with badges and structure
- ⚙️ config.example.py with detailed comments

**How to use:**
1. Type `/universal-setup` to view the workflow
2. Follow the 16 steps in order
3. Customize based on your project type
4. Test thoroughly before publishing

**Time estimate:** 2-4 hours for initial setup

---

## How Workflows Work

Workflows are markdown files with YAML frontmatter that provide step-by-step instructions for common tasks.

### Format

```markdown
---
description: Short description of what this workflow does
---

# Workflow Title

Step-by-step instructions...
```

### Turbo Mode

- `// turbo` above a step: Auto-run that specific command
- `// turbo-all` anywhere: Auto-run ALL commands in the workflow

### Creating New Workflows

1. Create a new file: `.agent/workflows/workflow-name.md`
2. Add YAML frontmatter with description
3. Write clear, step-by-step instructions
4. Include code examples and commands
5. Add tips and common pitfalls
6. Test the workflow end-to-end

### Best Practices

✅ **Do:**
- Make steps clear and actionable
- Include code examples
- Add verification steps
- Document prerequisites
- Provide troubleshooting tips
- Use consistent formatting

❌ **Don't:**
- Assume prior knowledge
- Skip error handling
- Forget to test
- Use vague instructions
- Leave out verification steps

---

## Contributing Workflows

Have a useful workflow? Add it here!

1. Create the workflow file
2. Update this README
3. Test it thoroughly
4. Submit a pull request
