import base64
import google.generativeai as genai
from src.config import settings

class MedicalChatbot:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.MODEL_NAME
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE
        self.disclaimer = settings.MEDICAL_DISCLAIMER

        self.system_prompt = """
        You are a helpful medical information assistant that provides accurate, evidence-based information
        about medical symptoms, medications, and general health questions for educational and research purposes only. 
        Do not provide diagnosis or medical advice.
        """

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name=self.model_name)

    def get_response(self, query, conversation_history=None, document_context=None, image_path=None):
        try:
            parts = [self.system_prompt]

            if document_context:
                parts.append(f"\nDocument context:\n{document_context}")

            if conversation_history:
                for user_msg, bot_msg in conversation_history[-4:]:
                    parts.append(f"User: {user_msg}")
                    parts.append(f"Assistant: {bot_msg}")

            parts.append(f"User: {query}")

            # MULTIMODAL CASE: image + text
            if image_path:
                with open(image_path, "rb") as f:
                    image_bytes = f.read()

                response = self.model.generate_content([
                    "\n".join(parts),
                    {"mime_type": "image/jpeg", "data": image_bytes}
                ])
            else:
                # TEXT-ONLY CASE
                response = self.model.generate_content("\n".join(parts))

            return f"{response.text.strip()}\n\n{self.disclaimer}"

        except Exception as e:
            return f"❌ Error from Gemini API: {str(e)}"
