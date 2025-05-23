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
# This section handles API key for both local (.env) and Streamlit Cloud (secrets)

gemini_api_key = None
gemini_configured = False

# For Streamlit Cloud deployment, secrets are accessed via st.secrets
# For local development, we'll use .env
# Check if running in Streamlit Cloud (this env var is set by Streamlit Cloud)
# A common way to check, though not officially documented for all cases,
# is to see if st.secrets is populated without raising an error,
# or check for specific environment variables Streamlit Cloud might set.
# A more robust check for Streamlit Cloud:
is_streamlit_cloud = os.getenv('SERVER_SOFTWARE', '').startswith('Streamlit') or \
                     os.getenv('STREAMLIT_SERVER_PORT') is not None or \
                     ('STREAMLIT_SHARING_MODE' in os.environ and os.environ['STREAMLIT_SHARING_MODE'] == 'true')


if is_streamlit_cloud:
    # This block executes when deployed on Streamlit Community Cloud
    streamlit_secret_key_name = "GOOGLE_GEMINI_API_KEY" # The name you'll use in Streamlit Cloud secrets
    if streamlit_secret_key_name in st.secrets:
        gemini_api_key = st.secrets[streamlit_secret_key_name]
        # st.sidebar.success("Using API Key from Streamlit Secrets!", icon="✅")
    else:
        st.error(f"🔴 Google API Key ('{streamlit_secret_key_name}') not found in Streamlit secrets. Please set it for the deployed app.")
        st.stop()
else:
    # This block executes for local development
    load_dotenv()
    local_api_key_from_env = os.getenv("GOOGLE_API_KEY")
    if local_api_key_from_env:
        gemini_api_key = local_api_key_from_env
        # st.sidebar.info("Using API Key from local .env file.", icon="📄")
    else:
        # This error will show if .env is missing or GOOGLE_API_KEY is not in it
        st.error("🔴 GOOGLE_API_KEY not found in your local .env file. Please create or check your .env file.")
        st.stop()

# Configure Gemini if API key was successfully obtained
if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        gemini_configured = True
    except Exception as e:
        st.error(f"🔴 Error configuring Google Gemini API: {e}")
        st.stop() # Stop app if configuration fails
elif not is_streamlit_cloud : # Only show this specific error if local and key wasn't loaded
    st.error("🔴 API Key was not loaded. Ensure .env is correct.")
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