import google.generativeai as genai
import os
from dotenv import load_dotenv
import random

load_dotenv()

class ChatBot:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            
            # This is your persona/friend instructions
            persona = """
            You are Astra, a chill, supportive, and funny personal friend. 
            - Use casual language (like 'hey', 'totally', 'no worries').
            - Be empathetic and grounded. 
            - Keep responses relatively concise, like a text message.
            - Don't be too formal or corporate. 
            - Don't use emojis
            """
            
            try:
                # Initialize the model with the persona
                self.model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash", # Use whichever version worked for you earlier
                    system_instruction=persona
                )
                self.chat = self.model.start_chat(history=[])
                self.mode = "ai"
            except Exception as e:
                print(f"Error starting AI: {e}")
                self.mode = "basic"
        else:
            self.mode = "basic"
            
        # Fallback responses if the AI is offline
        self.responses = [
            "Yo, my brain is offline. Check that API key!", 
            "I'm in basic mode right now, but I'm still here for ya.", 
            "Connection issues... but hey, how's it going?"
        ]

    def get_response(self, message):
        if self.mode == "ai":
            try:
                response = self.chat.send_message(message)
                return response.text
            except Exception as e:
                return f"AI Error: {e}"
        else:
            return random.choice(self.responses)