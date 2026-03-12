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
        "type": "function",
        "name": "web_search",
        "description": "Performs web search on a given query",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        }
    },
    {
        "type": "function",
        "name": "save_report",
        "description": "Save the result in a specified file",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["filename", "content"]
        }
    },
    {
        "type": "function",
        "name": "get_date",
        "description": "Very straightforward. Gets the current date and time",
        "parameters":{
            "type": "object",
            "properties": {}
        }
    }
]

def run_agent(user_request: str, output_file_name:str):

    messages = [{"role": "user", "content": user_request}]

    response = client.responses.create(
            model="gpt-4.1", 
            input=messages, 
            instructions="You are a research assistant. Use tools to gather information and save organized reports.", 
            tools=tools
        )

    # if response.status == "completed":
    #     print("Agent finished")
    #     print(response.output_text)
    #     break
    
    tool_results = []
    for tool in response.tools:
        print(f"Calling tool {tool}")

        if tool.name == "web_search":
            result = web_search(user_request)
        
        elif tool.name == "save_report":
            result = save_report(output_file_name, response.output_text)
        
        elif tool.name == "get_date":
            result = get_date()
        else:
            result = "Unknown"

        print(f".  -> {result[:100]}....")
        tool_results.append({
            "type": "tool_result",
            "content": result
        })
    
    messages.append({"role": "assistant", "content": response.output_text})
    messages.append({"role": "user", "content": tool_results})


# msg = [{"role": "user", "content": "What's the day today"}]
# response = client.responses.create(model= "gpt-4.1",input = msg, tools=None)
# print("\n", response)

run_agent("Research the topic 'Model Context Protocol' and save a structured summary report as output.txt", "output.txt")