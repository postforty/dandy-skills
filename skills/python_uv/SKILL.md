---
name: Python uv Development Rules
description: Guidelines for managing dependencies and executing code in Python projects using uv.
---

# Python uv Development Rules

This skill defines mandatory rules for dependency management and code execution in Python projects using `uv`.

## 1. Dependency Installation
- ALWAYS use `uv` instead of standard pip when installing libraries or packages in a Python project.
- Examples: 
  - `uv add <package_name>`
  - `uv pip install <package_name>`
- Prioritize `uv` over legacy tools like `pip install` to ensure speed and consistency.

## 2. Code Execution
- ALWAYS use the `uv run` command to execute source code or scripts.
- Examples: 
  - `uv run python main.py`
  - `uv run script.py`
- This ensures that the code runs seamlessly within an isolated environment with consistent dependencies.

## 3. Environment Initialization and Virtual Environments
- Actively utilize `uv init` and `uv venv` when starting a new project or configuring a virtual environment.
- If a virtual environment folder (`.venv`) already exists, DO NOT create a new one. When creating a virtual environment, you MUST use `uv venv`.
