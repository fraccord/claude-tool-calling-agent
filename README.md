# Claude API Agent

Simple Python AI agent powered by **Anthropic Claude** (Messages API) with **tool use / tool calling**.

This is a basic demonstration of building an autonomous agent that can:
- Reason step-by-step
- Call external tools (e.g., calculator)
- Chain prompts and tool results in a loop
- Handle multi-turn interactions

Ideal for learning agentic workflows, ReAct-style loops, and integrating LLMs with functions.

## Features
- Uses official `anthropic` Python SDK
- Supports tool calling (Claude decides when to use tools)
- Basic agent loop: think → act (tool) → observe → repeat
- Example tool: safe calculator (using restricted `eval`)

## Installation

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/claude-api-agent.git
cd claude-api-agent

# Install dependencies
pip install anthropic python-dotenv
