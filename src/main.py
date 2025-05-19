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

        genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=self.max_tokens,
                temperature=self.temperature
            )
        )

        self.system_prompt = """
        You are a helpful medical information assistant that provides accurate, evidence-based information
        about medical symptoms, medications, and general health questions for educational and research purposes only. 
        Do not provide diagnosis or medical advice.
        """

    def get_response(self, query, conversation_history=None, document_context=None, image_path=None):
        try:
            messages = [self.system_prompt]

            if document_context:
                messages.append(f"Document context:\n\n{document_context}")

            if conversation_history:
                for user_msg, bot_msg in conversation_history:
                    messages.append(f"User: {user_msg}")
                    messages.append(f"Assistant: {bot_msg}")

            # Combine the messages into a prompt
            prompt = "\n".join(messages) + f"\nUser: {query}"

            if image_path:
                with open(image_path, "rb") as f:
                    image_bytes = f.read()

                response = self.model.generate_content([
                    prompt,
                    {
                        "mime_type": "image/jpeg",
                        "data": image_bytes
                    }
                ])
            else:
                response = self.model.generate_content(prompt)

            answer = response.text.strip()
            return f"{answer}\n\n{self.disclaimer}"

        except Exception as e:
            return f"❌ Error while calling Gemini API: {str(e)}"

if __name__ == "__main__":
    print("Starting MedicalChatbot test...")

    bot = MedicalChatbot()
    response = bot.get_response("What are common symptoms of diabetes?")
    print(response)