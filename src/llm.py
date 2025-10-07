 # import libraries
import os
from dotenv import load_dotenv
from openai import OpenAI
 #[Add your code here]
load_dotenv()  # Loads environment variables from .env
token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-mini"
# A function to call an LLM model and return the response
def call_llm_model(model, messages, temperature=1.0, top_p=1.0):    
    client = OpenAI(base_url=endpoint,api_key=token)
    response = client.chat.completions.create(
        messages=messages,
        temperature=temperature, top_p=top_p, model=model)
    return response.choices[0].message.content
 # A function to translate text using the LLM model
def translate_text(text, target_language="French"):
    messages = [
        {
            "role": "system",
            "content": f"You are a helpful assistant that translates English to {target_language}.",
        },
        {
            "role": "user",
            "content": f"Translate the following text to {target_language}: {text}",
        }
    ]
    return call_llm_model(model, messages)

# A function to run the main logic
# main fun
if __name__ == "__main__":
    text_to_translate = "Hello, how are you?"
    translated_text = translate_text(text_to_translate, target_language="Chinese")
    print(f"Original: {text_to_translate}")
    print(f"Translated: {translated_text}")

