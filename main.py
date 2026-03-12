import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.environ.get('OPENAI_KEY')

client = openai.OpenAI(api_key=OPENAI_KEY)