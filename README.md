# 📝 Gemini AI Text Summarizer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://text-summarizer-1.streamlit.app/)

An interactive web application that leverages Google's Gemini Large Language Model to provide concise summaries of user-provided text. Built with Python and Streamlit for a fast, responsive user experience.

**[➡️ Live Demo: text-summarizer-1.streamlit.app](https://text-summarizer-1.streamlit.app/)**

---

## ✨ Features

*   **AI-Powered Summarization:** Utilizes Google Gemini for intelligent text summarization.
*   **Interactive UI:** Simple and intuitive interface built with Streamlit.
*   **Adjustable Summary Length:** Users can specify the approximate target word count for the summary.
*   **Real-time Output:** Get summaries quickly with a loading indicator.
*   **Responsive Design:** Works on desktop and mobile browsers.

---

## 🚀 Demo

<!-- 
  TODO: Add a screenshot or an animated GIF here!
  How to add a GIF/Screenshot:
  1. Take a screenshot of your app running, or record a short GIF.
  2. Upload this image/GIF to this GitHub repository (e.g., in an 'assets' folder or the root).
  3. Get the raw link to the image/GIF on GitHub.
  4. Replace the placeholder below with: ![App Demo](LINK_TO_YOUR_IMAGE_OR_GIF_ON_GITHUB)
-->

**(A screenshot or GIF demonstrating the app in action will be added here soon!)**

---

## 🛠️ Technologies Used

*   **Frontend / Application Framework:** [Streamlit](https://streamlit.io/)
*   **Programming Language:** [Python](https://www.python.org/)
*   **AI / LLM:** [Google Gemini API](https://ai.google.dev/) (via `google-generativeai` SDK)
*   **Prompt Engineering:** Custom prompts to guide LLM output.
*   **Deployment:** [Streamlit Community Cloud](https://streamlit.io/cloud)
*   **Version Control:** [Git](https://git-scm.com/) & [GitHub](https://github.com/)
*   **Environment Management:** `python-dotenv` (for local development)

---

## ⚙️ Setup and Run Locally (Optional)

If you'd like to run this project on your local machine:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/debtanu-github/Text_Summarizer.git
    cd Text_Summarizer
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your Google Gemini API Key:**
    *   Create a file named `.env` in the project root (`Text_Summarizer` folder).
    *   Add your API key to the `.env` file:
        ```
        GOOGLE_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY_HERE"
        ```
    *   You can get an API key from [Google AI Studio](https://aistudio.google.com/).

5.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
    The application should open in your web browser.

---

## 📄 Files in this Repository

*   `app.py`: The main Streamlit application script.
*   `requirements.txt`: Python dependencies for the project.
*   `.gitignore`: Specifies intentionally untracked files that Git should ignore.
*   `main.py`: (Kept for reference) Foundational FastAPI backend structure for potential future API development.
*   `README.md`: This file!

---

## 💡 Future Ideas (Potential Improvements)

*   Option for different summary styles (e.g., bullet points).
*   Support for summarizing text from URLs or uploaded files.
*   More advanced error handling and user feedback.
*   Caching results for frequently summarized texts.

---

## 🙏 Acknowledgements

*   Powered by [Google Gemini](https://ai.google.dev/)
*   User Interface by [Streamlit](https://streamlit.io/)

---