import json
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def build_prompt(chunk):

    return f"""
You are a refinery trainer.

Generate 5 MCQs.

Return JSON ONLY.

Format:

[
 {{
   "question":"",
   "options":["","","",""],
   "answer":"",
   "explanation":""
 }}
]

TEXT:

{chunk}
"""


def generate_questions(chunk):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":"user",
                "content":build_prompt(chunk)
            }
        ],
        temperature=0.3
    )

    return json.loads(
        response.choices[0].message.content
    )