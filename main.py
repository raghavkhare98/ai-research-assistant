import openai
import json
import os
import datetime
import urllib.request
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.environ.get('OPENAI_KEY')

client = openai.OpenAI(api_key=OPENAI_KEY)

def web_search(query: str) -> str:
    if not any(char in query for char in ["_", ".", "-", "~"]):
        encoded_url = urllib.parse.quote(query)
        url = f"https://api.duckduckgo.com/?q={encoded_url}&format=json&no_html=1"
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read())
            abstract = data.get("AbstractText", "")
            related = [t["Text"] for t in data.get("RelatedTopics", [])[:3] if "Text" in t]
            return abstract or "\n".join(related) or "No results found"
    except:
        return "Search Unavailable"

def save_report(filename: str, content: str) -> str:
    with open(filename, "w") as f:
        f.write(content)
    return f"Search results saved to file - {filename}"

def get_date() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

tools = [
    {
        "name": "web_search",
        "description": "Performs web search on a given query",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "save_report",
        "description": "Save the result in a specified file",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["filename", "content"]
        }
    },
    {
        "name": "get_date",
        "description": "Very straightforward. Gets the current date and time",
        "input_schema":{
            "type": "object",
            "properties": {}
        }
    }
]