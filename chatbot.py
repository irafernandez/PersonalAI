import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import random

# Load local .env file if it exists
load_dotenv()

class ChatBot:
    def __init__(self):
        # 1. Look for API key in local .env OR Streamlit Cloud Secrets
        self.api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
        
        if self.api_key:
            try:
                # Initialize the Groq client
                self.client = Groq(api_key=self.api_key)
                
                # Your "Personal Friend" instructions
                self.persona = """
                You are Astra, a chill, supportive, and funny personal friend. 
                - Use casual language (like 'hey', 'totally', 'no worries').
                - Be empathetic and grounded. 
                - Keep responses relatively concise, like a text message.
                - Don't be too formal or corporate. 
                - Do not use emojis at all.
                - Do not be repetitive
                """
                
                # Note: llama-3.3-70b-versatile is smart and has a high free limit
                self.model_name = "llama-3.3-70b-versatile"
                self.mode = "ai"
                
            except Exception as e:
                print(f"Error starting AI: {e}")
                self.mode = "basic"
        else:
            self.mode = "basic"
            
        # Fallback responses if the AI is offline
        self.responses = [
            "Yo, my brain is offline. Check that Groq API key!", 
            "I'm in basic mode right now, but I'm still here for ya.", 
            "Connection issues... but hey, how's it going?"
        ]

    def get_response(self, message):
        if self.mode == "ai":
            try:
                # Groq uses a different way to send messages compared to Gemini
                completion = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": self.persona},
                        {"role": "user", "content": message}
                    ],
                    temperature=0.7, # Adds a bit of personality
                )
                return completion.choices[0].message.content
            except Exception as e:
                # Nicer error handling for rate limits
                if "429" in str(e):
                    return "Astra is taking a quick breather (Rate limit hit). Try again in a few seconds!"
                return f"Astra is a bit overwhelmed right now: {e}"
        else:
            return random.choice(self.responses)