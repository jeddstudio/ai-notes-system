# src/components/note_processor.py
from datetime import datetime
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import logging
import yaml

logger = logging.getLogger(__name__)
load_dotenv()

class NoteProcessor:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.db = None
        self.load_prompts()

    def load_prompts(self):
        """Load prompt templates"""
        self.prompts = {}
        prompt_dir = os.path.join(os.path.dirname(__file__), '..', 'ai', 'prompts', 'templates')
        
        for lang in ['en', 'zh']:
            template_path = os.path.join(prompt_dir, f'note_summary_{lang}.yaml')
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    template = yaml.safe_load(f)
                    self.prompts[lang] = template['content']
            except Exception as e:
                logger.error(f"Error loading prompt template {lang}: {str(e)}")
                self.prompts[lang] = None

    def set_db(self, db):
        self.db = db

    def create_note(self, title: str, content: str):
        """Create a regular note"""
        note = {
            "title": title,
            "content": content,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "type": "regular"
        }
        return self.db.notes.insert_one(note)

    async def create_ai_note(self, title: str, content: str, language: str = "en"):
        """Create a note processed by AI"""
        try:
            # Get the appropriate prompt template
            prompt_template = self.prompts.get(language)
            if not prompt_template:
                logger.warning(f"No prompt template found for language {language}, using default")
                prompt_template = "You are a helpful assistant that helps structure and summarize notes."

            # Create system message with the template and specific instructions
            system_message = f"{prompt_template}\n\nInput Note to Process:\n{content}"
            
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo-16k",  # Using 16k model for longer context
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": "Please process this note according to the provided template structure."}
                ],
                temperature=0.7,
                max_tokens=4000  # Increased token limit for more detailed response
            )
            
            processed_content = response.choices[0].message.content
            
            note = {
                "title": title,
                "content": processed_content,
                "original_content": content,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "type": "ai",
                "language": language
            }
            
            return self.db.notes.insert_one(note)
            
        except Exception as e:
            logger.error(f"Error creating AI note: {str(e)}")
            raise