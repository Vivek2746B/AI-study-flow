import os
import json
import google.generativeai as genai
import wikipedia
from pypdf import PdfReader
from dotenv import load_dotenv

# 1. Configuration
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Helper: Clean JSON
def clean_json_text(text):
    """Removes markdown formatting if Gemini adds it."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.endswith("```"):
        text = text[:-3]
    return text

# 3. Tool: Fetch from Wikipedia
def fetch_wikipedia_content(topic):
    try:
        print(f"🔍 Searching Wikipedia for '{topic}'...")
        page = wikipedia.page(topic, auto_suggest=False)
        return page.content[:15000] 
    except wikipedia.exceptions.PageError:
        print("❌ Topic not found on Wikipedia.")
        return None
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"⚠️ Topic is ambiguous. Try: {e.options[:3]}")
        return None
    except Exception as e:
        print(f"⚠️ Wikipedia error: {e}")
        return None

# 4. Tool: Fetch from Gemini (For Questions)
def fetch_gemini_content(question):
    print(f"🤖 Asking Gemini 2.5 to explain: '{question}'...")
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"""
        Write a detailed, comprehensive explanation about the following question or topic. 
        The goal is to provide enough source material to create flashcards and a quiz later.
        
        Topic/Question: {question}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return None

# 5. Tool: Read PDF
def read_pdf_content(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text[:15000] 
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return None
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return None

# 6. Tool: The Brain (Generates the Study Package)
def generate_study_material(content_text, difficulty="intermediate"):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # UPDATED PROMPT: Now asks for "explanation" in the JSON
        prompt = f"""
        Act as an expert tutor. I need a study package based on the TEXT provided below.
        Target Audience Level: {difficulty.upper()}.

        INSTRUCTIONS:
        1. Summary: If beginner, make it simple/detailed. If advanced, concise/technical.
        2. Flashcards: Create 5 key term flashcards.
        3. Quiz: Create 5 multiple choice questions.
        4. Explanation: For every quiz question, provide a short explanation of why the answer is correct.

        TEXT CONTENT:
        {content_text}

        OUTPUT FORMAT:
        You must output STRICT JSON format only.
        Schema:
        {{
            "topic_title": "string",
            "summary": "string (markdown allowed)",
            "flashcards": [
                {{"front": "Question/Term", "back": "Answer/Definition"}}
            ],
            "quiz": [
                {{
                    "question": "string",
                    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
                    "correct_answer": "A) ...",
                    "explanation": "string"
                }}
            ]
        }}
        """

        response = model.generate_content(prompt)
        cleaned_json = clean_json_text(response.text)
        return json.loads(cleaned_json)

    except Exception as e:
        print(f"❌ AI Error: {e}")
        return None

# 7. Tool: Save Results
def save_results(data):
    filename = "last_topic_output.json"
    try:
        with open(filename, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"💾 Data saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")