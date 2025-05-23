import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("ERROR: Google API Key not found. Make sure it's in your .env file as GOOGLE_API_KEY and that the .env file is in the same directory as main.py.")
    # For a real app, you might raise a more specific startup error or exit.
else:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        print("Google Gemini API configured successfully.")
    except Exception as e:
        print(f"Error configuring Google Gemini API: {e}")
        GOOGLE_API_KEY = None # Prevent further use if config fails

# --- FastAPI App Instance ---
app = FastAPI(
    title="Simple Text Summarizer API (Gemini)",
    description="An API that uses Google Gemini to summarize text.",
    version="0.1.0"
)

# --- Pydantic Models for Request and Response ---
class TextToSummarize(BaseModel):
    text: str
    target_word_count: int = 75 # Approximate target word count for the summary

class SummaryResponse(BaseModel):
    original_text: str
    summary: str

# --- API Endpoint ---
@app.post("/summarize", response_model=SummaryResponse, tags=["Summarization"])
async def summarize_text_gemini(payload: TextToSummarize):
    """
    Summarizes the input text using the Google Gemini API.
    """
    if not GOOGLE_API_KEY:
        raise HTTPException(status_code=500, detail="Google API Key not configured or configuration failed at startup.")

    try:
        # Choose a Gemini model. 'gemini-1.5-flash-latest' is fast and capable.
        # 'gemini-pro' is also a good choice.
        model = genai.GenerativeModel('gemini-1.5-flash-latest') # Or 'gemini-pro'

        # Construct the prompt for summarization
        prompt = f"""Please summarize the following text concisely.
Aim for a summary of approximately {payload.target_word_count} words.
Do not start the summary with phrases like "Here is a summary of the text:" or "The text is about:".
Just provide the direct summary.

Text to summarize:
---
{payload.text}
---

Summary:
"""

        # Make the API call to Gemini
        # generation_config can be used for more control (temperature, top_p, etc.)
        # For summarization, default or slightly lower temperature is often good.
        generation_config = genai.types.GenerationConfig(
            # candidate_count=1, # Default is 1
            # stop_sequences=['.'], # Example: stop if a period is generated
            # max_output_tokens=200, # Max tokens for the summary
            temperature=0.7 # Lower temperature for more factual summaries
        )
        
        response = await model.generate_content_async( # Use async version
            prompt,
            generation_config=generation_config
        )

        # Extract the summary text
        if response.parts:
            summary = response.text.strip()
        elif response.prompt_feedback and response.prompt_feedback.block_reason:
            block_reason_name = "Unknown"
            # Check for 'name' attribute (newer SDK versions)
            if hasattr(response.prompt_feedback.block_reason, 'name'):
                block_reason_name = response.prompt_feedback.block_reason.name
            # Check for 'value' attribute (older SDK versions, less common now)
            elif hasattr(response.prompt_feedback.block_reason, 'value'): 
                block_reason_name = str(response.prompt_feedback.block_reason.value)
            
            print(f"Content blocked by Gemini. Reason: {block_reason_name}. Full feedback: {response.prompt_feedback}")
            raise HTTPException(
                status_code=400, 
                detail=f"Content blocked by Gemini due to: {block_reason_name}. The input text might violate safety policies."
            )
        else:
            # This case might occur if the response is empty for other reasons
            # or if the model couldn't generate a summary.
            print(f"Gemini API response unexpected or empty. Full response: {response}")
            raise HTTPException(status_code=500, detail="Error processing summary from Gemini API: Empty or unexpected response.")

        if not summary: # Check if summary is empty after stripping
            print(f"Gemini API returned an empty summary for prompt: {prompt}. Full response: {response}")
            raise HTTPException(status_code=500, detail="Gemini API returned an empty summary. Try rephrasing input or check model.")

        return SummaryResponse(original_text=payload.text, summary=summary)

    except Exception as e:
        # Log the full error for debugging
        print(f"An unexpected error occurred with Gemini API: {type(e).__name__} - {str(e)}")
        # Provide a generic error message to the client
        raise HTTPException(status_code=500, detail=f"An internal server error occurred while contacting the Gemini API.")

# --- Basic Root Endpoint (Optional) ---
@app.get("/", tags=["General"])
async def read_root():
    return {"message": "Welcome to the Simple Text Summarizer API (Gemini). Go to /docs for API documentation."}

# To run the app (from the terminal, in the Text_Summarizer directory, with venv active):
# uvicorn main:app --reload