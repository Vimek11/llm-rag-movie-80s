import os
import yaml
import logging
from app.domain.model.prompt.prompt_provider import PromptProvider

logger = logging.getLogger(__name__)

class YamlPromptProvider(PromptProvider):
    def __init__(self, path: str = None):
        if path is None:
            base_dir = os.path.dirname(__file__)
            path = os.path.join(base_dir, "prompts.yml")

        self.path = path
        logger.info(f"Using prompts file: {self.path}")

    def get_prompt(self, key: str, **kwargs) -> str:
        try:
            if not os.path.exists(self.path):
                logger.warning(f"Prompt file not found: {self.path}")
                return ""

            with open(self.path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            template = data.get(key)
            if template is None:
                logger.warning(f"Prompt key '{key}' not found in YAML.")
                return ""

            return template.format(**kwargs)

        except Exception as e:
            logger.exception(f"Error loading prompt '{key}' from {self.path}")
            return ""
