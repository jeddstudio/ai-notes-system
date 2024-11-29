from pathlib import Path
import yaml
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PromptManager:
    def __init__(self):
        self.templates_dir = Path(__file__).parent / "templates"
        self.templates: Dict[str, Any] = {}
        self._load_templates()
    
    def _load_templates(self) -> None:
        """Load all YAML templates from the templates directory"""
        for filename in self.templates_dir.glob("*.yaml"):
            template_name = filename.stem  # Remove .yaml extension
            with open(filename, "r", encoding="utf-8") as f:
                self.templates[template_name] = yaml.safe_load(f)
            logger.info(f"Loaded prompt template: {template_name}")
    
    def get_prompt(self, template_name: str, **kwargs) -> str:
        """Get a prompt by template name and format it with provided kwargs"""
        if template_name not in self.templates:
            raise ValueError(f"Template {template_name} not found")
        
        template = self.templates[template_name]
        try:
            return template["prompt"].format(**kwargs)
        except KeyError as e:
            logger.error(f"Missing required parameter for prompt '{template_name}': {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error formatting prompt '{template_name}': {str(e)}")
            raise