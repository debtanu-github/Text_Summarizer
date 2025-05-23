import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv # For local .env loading

# --- Page Configuration (do this first) ---
st.set_page_config(
    page_title="Gemini Text Summarizer",
    page_icon="📝",
    layout="centered"
)

# --- Load Environment Variables & Configure Gemini API ---
gemini_api_key = None
gemini_configured = False

# Try to get the API key from Streamlit secrets first (for deployed app)
streamlit_secret_name = "GOOGLE_GEMINI_API_KEY" # Must match what you set in Streamlit Cloud
try:
    # Check if st.secrets has the key. This works on Streamlit Cloud.
    # Locally, if no .streamlit/secrets.toml, st.secrets will be empty or raise an error on access.
    if hasattr(st, 'secrets') and streamlit_secret_name in st.secrets:
        gemini_api_key = st.secrets[streamlit_secret_name]
        # st.sidebar.info("Using API Key from Streamlit Secrets.", icon="☁️") # For debugging
except Exception: # Broad exception because st.secrets behavior can vary locally
    pass # If st.secrets access fails or key not found, proceed to .env check

# If not found in secrets (or if running locally and secrets aren't set up), try .env
if not gemini_api_key:
    load_dotenv()
    local_env_key = os.getenv("GOOGLE_API_KEY") # Key name in your local .env file
    if local_env_key:
        gemini_api_key = local_env_key
        # st.sidebar.info("Using API Key from local .env file.", icon="📄") # For debugging

# Final check and configuration
if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        gemini_configured = True
    except Exception as e:
        st.error(f"🔴 Error configuring Google Gemini API: {e}")
        st.stop()
else:
    # If after all checks, no API key is found
    st.error(f"🔴 Google API Key not found. Please ensure '{streamlit_secret_name}' is set in Streamlit secrets for deployment, or 'GOOGLE_API_KEY' is in your .env file for local development.")
    st.stop()


# --- Gemini Summarization Function ---
def summarize_with_gemini(text_to_summarize, target_word_count_gemini):
    if not gemini_configured:
         return "Error: Gemini API not configured."

    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest') # Or 'gemini-pro'

        prompt = f"""Please summarize the following text concisely.
Aim for a summary of approximately {target_word_count_gemini} words.
Do not start the summary with phrases like "Here is a summary of the text:" or "The text is about:".
Just provide the direct summary.

Text to summarize:
---
{text_to_summarize}
---

Summary:
"""
        generation_config = genai.types.GenerationConfig(temperature=0.7)

        # Use synchronous version for Streamlit simplicity here
        response = model.generate_content(prompt, generation_config=generation_config)

        if response.parts:
            summary = response.text.strip()
            if not summary: # Handle case where model returns empty string
                return "Error: Gemini returned an empty summary. The input might be too short or unclear."
            return summary
        elif response.prompt_feedback and response.prompt_feedback.block_reason:
            block_reason_name = "Unknown"
            if hasattr(response.prompt_feedback.block_reason, 'name'):
                block_reason_name = response.prompt_feedback.block_reason.name
            elif hasattr(response.prompt_feedback.block_reason, 'value'): # Older SDK check
                block_reason_name = str(response.prompt_feedback.block_reason.value)
            return f"Error: Content blocked by Gemini due to: {block_reason_name}."
        else:
            # This case might occur if the response is empty for other reasons
            # print(f"Gemini API response unexpected or empty. Full response: {response}") # Log for debugging
            return "Error: Unexpected response from Gemini API. Check logs."
    except Exception as e:
        # print(f"Error during summarization: {type(e).__name__} - {str(e)}") # Log for debugging
        return f"Error during summarization: {str(e)}"

# --- Streamlit App UI ---
st.title("📝 Gemini Text Summarizer")
st.markdown("Enter some text below and get a concise summary using Google Gemini!")

# Input text area
input_text = st.text_area(
    "Paste your text here:",
    height=250,
    placeholder="Enter a long article, paragraph, or any text you want to summarize..."
)

# Slider for target word count
target_words = st.slider(
    "Approximate target word count for summary:",
    min_value=20,
    max_value=250, # Increased max
    value=75,
    step=5
)

if st.button("✨ Summarize Text", type="primary"):
    if not gemini_configured:
        st.error("Cannot summarize: Gemini API is not configured correctly.")
    elif input_text.strip(): # Check if input_text is not just whitespace
        with st.spinner("🤖 Gemini is thinking... Please wait."):
            summary_output = summarize_with_gemini(input_text, target_words)

        st.subheader("Summary:")
        if "Error:" in summary_output:
            st.error(summary_output)
        else:
            st.success(summary_output) # Use success for positive output
            # Optional: Display word counts
            st.markdown(f"*(Original word count: ~{len(input_text.split())} | Summary word count: ~{len(summary_output.split())})*")
    else:
        st.warning("Please enter some text to summarize.")

st.markdown("---")
st.markdown("Powered by [Google Gemini](https://ai.google.dev/) & [Streamlit](https://streamlit.io/)")
# st.caption(f"Gemini API Configured: {'Yes' if gemini_configured else 'No'}") # For debugging