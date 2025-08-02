import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from app.domain.model.llm.llm_provider import LLMProvider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv("config.env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-2.0-flash')

class GeminiProvider(LLMProvider):
    def ask(self, prompt: str) -> str:
        logger.info("Sending prompt to Gemini.")
        try:
            response = model.generate_content(prompt)
            result = response.text.strip()
            logger.info("Received response from Gemini.")
            return result
        except Exception as e:
            logger.exception("Error while requesting Gemini completion.")
            return ""

    def extract_topic(self, question: str) -> str:
        prompt = f"""
                    Extract the general topic of this movie-related question for semantic search.
                    Question: {question}
                    Return just a short English phrase. No explanation.
                """
        return self.ask(prompt)
    
    def extract_title(self, question: str) -> str:
        prompt = f"""
            Extract the name of the movie mentioned in this question.
            Question: {question}
            Return ONLY the movie title, in English, with no extra text.
            If there's no movie title mentioned, return false.
        """
        return self.ask(prompt)

