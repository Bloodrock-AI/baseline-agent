import os
import json

from llm_tool import tool
from dotenv import load_dotenv
from groq import Groq

# these must be defined externally
# from .ext import global_state, tools

from typing import List, Dict

MODEL="llama-3.1-70b-versatile"
SYSTEM_PROMPT=""

global_state = {
    "distance_calulated": False,
}

@tool()
def calculate_distance(a: int, b: int) -> int:
    """
    Calculate the euclidian distance between two integers.

    :param a: first integer
    :param b: second integer
    :return: distance
    """
    global_state["distance_calulated"] = True
    return abs(int(a) - int(b))

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def baseline_agent(prompt: str) -> List[Dict[str, str]]:
    
    seq = []
    finished = False

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": prompt,
        }
    ]

    while not finished:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            tools=[calculate_distance.definition],
            tool_choice="auto",
            temperature=0,
            top_p=1,
        )
        
        tool_calls = response.choices[0].message.tool_calls

        if not tool_calls: return seq

        for tool_call in tool_calls:
            args = json.loads(tool_call.function.arguments)
            # calculate response
            resp = calculate_distance(**args)

            messages.append({
                "tool_call_id": tool_call.id,
                "role": "assistant",
                "name": tool_call.function.name,
                "content": str(resp),
            })

            seq.append({
                "name": tool_call.function.name,
                "args": args,
            })

        temp = messages
        temp.append({
            "role": "user",
            "content": f"""
                Based on the provided global state, is the goal of the user prompt reached?

                prompt: {prompt}
                global state: {global_state}

                your answer should be either "yes" or "no" in the following json format
                {{ "answer": "yes" }}
            """
        })

        response = client.chat.completions.create(
            model=MODEL,
            messages=temp,
            temperature=0.8,
            top_p=1,
        )

        try:
            resp = json.loads(response.choices[0].message.content)
        except:
            print(response.choices[0].message.content)
            break

        print(resp['answer'])
        if resp['answer'] == 'yes':
            finished = True

    return seq

if __name__ == '__main__':
   print(baseline_agent("What is the distance between 1 and 2?")) 
