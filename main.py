import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def baseline_agent():
    pass

if __name__ == '__main__':
    pass
