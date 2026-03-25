import os 
import json
import httpx
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "fetch_readme",
            "description": "Fetches the README from a GitHub repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string", "description": "GitHub repo URL"}
                },
                "required": ["repo_url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_languages",
            "description": "Fetches the languages used in a GitHub repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string", "description": "GitHub repo URL"}
                },
                "required": ["repo_url"]
            }
        }
    }
]

def fetch_readme(repo_url: str) -> str:
    parts = repo_url.strip("/").split("/")
    user, repo = parts[-2], parts[-1]
    
    for branch in ["main", "master"]:
        url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/README.md"
        response = httpx.get(url)
        if response.status_code == 200:
            return response.text[:3000]  # ← truncate here
    
    return "README not found"

def fetch_languages(repo_url: str) -> dict:
    parts = repo_url.strip("/").split("/")
    user, repo = parts[-2], parts[-1]
    url = f"https://api.github.com/repos/{user}/{repo}/languages"
    return httpx.get(url).json()

tool_map = {
    "fetch_readme": fetch_readme,
    "fetch_languages": fetch_languages,
}

def github_agent(repo_url: str):
    messages = [{"role": "user", "content": f"Summarize this repo: {repo_url}"}]

    while True:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message
        finish_reason = response.choices[0].finish_reason

        if finish_reason == "tool_calls":
            tool_call = message.tool_calls[0]
            args = json.loads(tool_call.function.arguments)
            result = tool_map[tool_call.function.name](args["repo_url"])

            messages.append(message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })
        else:
            return message.content

# run it!
print(github_agent("https://github.com/donnemartin/system-design-primer"))