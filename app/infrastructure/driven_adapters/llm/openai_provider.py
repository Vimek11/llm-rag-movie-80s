import os
import logging
from openai import OpenAI
import httpx
from dotenv import load_dotenv
from app.domain.model.llm.llm_provider import LLMProvider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv("config.env")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    http_client=httpx.Client(verify=False)
)

class OpenAIProvider(LLMProvider):
    def ask(self, prompt: str) -> str:
        logger.info("Sending prompt to OpenAI.")
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            result = response.choices[0].message.content.strip()
            logger.info("Received response from OpenAI.")
            return result
        except Exception as e:
            logger.exception("Error while requesting OpenAI completion.")
            return ""

    def extract_topic(self, question: str) -> str:
        prompt = f"""
            Extract the name of the movie mentioned in this question.
            Question: {question}
            Return ONLY the movie title, in English, with no extra text.
            If there's no movie title mentioned, return false.
        """
        return self.ask(prompt)
