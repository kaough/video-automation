import google.generativeai as genai
from config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)

print("Listing available models...")
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
