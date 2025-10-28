from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUMBUGGING_API_TOKEN = os.getenv("HUMBUGGING_API_TOKEN")
