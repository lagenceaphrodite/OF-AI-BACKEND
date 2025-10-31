from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()

class Message(BaseModel):
    conversation: str

@app.post("/analyze")
def analyze(msg: Message):
    prompt = f"""
    Tu es un analyste en psychologie appliquée à la vente.
    Conversation :
    {msg.conversation}

    Donne :
    1. Le profil (1 phrase)
    2. Trois phrases suggérées pour améliorer la conversion PPV.
    JSON :
    {{
      "profile": "...",
      "suggestions": ["...", "...", "..."]
    }}
    """
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    text = completion.choices[0].message.content
    import json
    try:
        return json.loads(text)
    except:
        return {"profile": "Analyse en erreur", "suggestions": []}