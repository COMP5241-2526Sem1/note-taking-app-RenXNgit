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

system_prompt= '''
 Extract the user's notes into the following structured fields:
 1. Title: A concise title of the notes less than 5 words
 2. Notes: The notes based on user input written in full sentences.
 3. Tags (A list): At most 3 Keywords or tags that categorize the content of the notes.
 Output in JSON format without ```json. Output title and notes in the language: {lang}.
 Example:
 Input: "Badminton tmr5pm @polyu".
 Output:
 {{
 "Title": "Badminton at PolyU", 
"Notes": "Remember to play badminton at 5pm tomorrow at PolyU.",
 "Tags": ["badminton", "sports"]
 }}
 '''
# a function extract structed notes using the LLM model
def extract_structured_notes(user_input, lang="English"):
    messages = [
        {
            "role": "system",
            "content": system_prompt.format(lang=lang),
        },
        {
            "role": "user",
            "content": user_input,
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
    #test the extract notes feature
    simple_input = "Meeting with Bob at 3pm on Friday to discuss the project updates."
    structured_notes = extract_structured_notes(simple_input, lang="English")
    print(f"Input: {simple_input}")
    print(f"Structured Notes: {structured_notes}")
