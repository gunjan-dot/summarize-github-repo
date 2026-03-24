# summarize-github-repo

# GitHub Repo Summarizer Agent

An AI agent that takes any GitHub repository URL and returns a 
summary of what the project does and what tech stack it uses.

## How it works

1. Given a repo URL, the agent decides which tools to call
2. It fetches the README and/or language breakdown via GitHub's API
3. An LLM synthesizes the information into a clear summary

## Tech Stack

- Python
- Groq API (LLaMA 3.3 70B)
- OpenAI-compatible client
- httpx

## Setup

1. Clone the repo
2. Install dependencies: `pip install openai httpx`
3. Set your Groq API key: `export GROQ_API_KEY=your-key`
4. Run: `python agent.py`

## Example

Input:
    https://github.com/tiangolo/fastapi

Output:
    FastAPI is a modern, high-performance Python web framework 
    for building APIs. It uses Python type hints for validation 
    and auto-generates OpenAPI documentation...

## What I learned

- How AI agents work (ReAct loop)
- Tool calling with LLMs
- Building agents from scratch without frameworks
