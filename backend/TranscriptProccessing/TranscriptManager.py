import os
import json
import google.generativeai as genai
from objs.TherapySession import TherapySession 
from utils.db import Database
from dotenv import load_dotenv


load_dotenv()
db = Database()

gemini_api_key = os.getenv("API_KEY")

# Define the path to the transcript
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#TODO: not used for now- check why it breaks the AI proccessing when injected dynamicly
prompt_path = os.path.join("Prompts", "gemini_clinical_note_prompt.txt")
with open(prompt_path, "r", encoding="utf-8") as f:
    prompt_text = f.read()

#fetch session summery from DB
#TODO: id to be fed dynamicly
therapySession = TherapySession(**db.find_by_id("session_text", "2"))
transcript = therapySession.transcript
# Replace with your actual Gemini API key
genai.configure(api_key=gemini_api_key)
# TODO: check if this is the best model (Gemini 1.5 Pro)
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

# Construct the prompt
prompt = """
You are a language model expert in converting clinical note documents into a structured JSON format.
Your task is to transform an input clinical note (which includes sections such as “Note”, “Subjective”, “Objective”, “Assessment”, “Plan”, “Interventions and Response”, “Mental Status Examination (MSE)”, “Risk Assessment”, “Topics”, and “Notable Mentions”) into a JSON object that strictly follows the structure outlined below.
Instructions:
1. Overall Structure:
• The output must be a valid JSON object containing three keys: "id", "title", and "content".
• The main container is the overall “Note” section. Use "id": "notes" and "title": "Note".

2. Section Identification and Processing:
• Identify Main Sections: Accurately identify sections such as Subjective, Objective, Assessment, Plan, Interventions and Response, Mental Status Examination (MSE), Risk Assessment, Topics, and Notable Mentions.
• Generate IDs: For each section, generate an "id" by converting the section title to lowercase and replacing spaces (and non-alphanumeric characters) with hyphens. For example, "Mental Status Examination (MSE)" becomes "mse", and "Interventions and Response" becomes "interventions-and-response".

3. Content Splitting:
• Sentence Splitting: Split the text under each section into individual sentences. Assume sentences are delimited by periods. However, take care not to split within section titles or bullet points.
• Bullet Points Handling: Any text starting with a bullet point (e.g., •) should be treated as an individual sentence and preserved exactly as it appears, including the bullet symbol.

4. Nested Subsections:
• Some sections (specifically "Interventions and Response" and "Topics", as well as subsections under "Notable Mentions") contain further nested subsections.
• Detection: Identify nested subsections by markers such as "Topic:" or similar prefixes.
• Structure: Represent each nested subsection as a JSON object within the parent section’s "content" array, using the same three keys ("id", "title", and "content").
• ID Generation for Subsections: Generate IDs for these subsections similarly by converting their titles to lowercase and replacing spaces with hyphens.

5. Output Format:
• The final JSON output must adhere exactly to the provided structure. Do not include any additional keys or modify the structure.
• The output must be valid JSON.

6. Reusability:
• Your instructions should work for any similar clinical note document following this or a similar section layout.

Input Clinical Note:
{transcript}
Return only the structured JSON output.
"""

# Call Gemini
response = model.generate_content(prompt)

# Output the result
try:
    # Clean up the markdown-style code block
    clean_json = response.text.strip('`\njson')
    summary_json = json.loads(clean_json)
    print(json.dumps(summary_json, indent=2))
    summary_json["session_id"] = therapySession.session_id
    insert_result = db.insert_document("transcript_summary", summary_json)
except json.JSONDecodeError:
    print("Could not parse JSON output. Raw response:")
    print(response.text)








