# AI Meeting Notes Summarizer & Sharer

A Streamlit app that generates structured meeting summaries using an LLM (Groq), allows editing, saving locally, and sharing via email.

## Features
- Upload or paste meeting transcripts
- Provide a custom instruction/prompt
- Generate an editable structured summary using an LLM API
- Save summaries to a local SQLite DB
- Share edited summaries via SMTP email

## Setup

1. Clone repo
  ```bash
    git clone <repo-url>
    cd meeting-summarizer
  ```

2. Create a Python venv and install
  ```bash
    python -m venv venv
    source venv/bin/activate    # or venv\Scripts\activate on Windows
    pip install -r requirements.txt
  ```

3. Copy env file and fill values
  ```bash
    # LLM / Groq
    GROQ_API_KEY="api-key"
    
    # SMTP for sending email
    SMTP_HOST="smtp.gmail.com"
    SMTP_PORT="587"
    SMTP_USERNAME="your_mail@gmail.com"
    SMTP_PASSWORD="app-password"
    SMTP_FROM="your_mail@gmail.com"
    
    # Optional app settings
    DEFAULT_MAX_TOKENS="800"
  ```
4. Run app
  ```bash
    cd app
    streamlit run streamlit_app.py
  ```
