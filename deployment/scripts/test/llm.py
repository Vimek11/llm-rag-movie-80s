""" import os
from dotenv import load_dotenv
from openai import OpenAI
import httpx


load_dotenv("config.env")

API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY, http_client=httpx.Client(verify=False))

def ask_llm(prompt: str):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente experto que responde basándose solo en la información proporcionada."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error al consultar el LLM: {str(e)}" """

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv("config.env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Crea el modelo (usa el pro por defecto)
model = genai.GenerativeModel('gemini-2.0-flash')

def ask_llm(prompt: str):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error al consultar Gemini: {str(e)}"
