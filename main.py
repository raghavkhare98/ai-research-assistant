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
    if ["_", ".", "-", "~"] not in query:
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