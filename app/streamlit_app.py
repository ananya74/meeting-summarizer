
import os
from dotenv import load_dotenv


# Load .env 
load_dotenv()

import streamlit as st
from llm_client import generate_summary
from email_utils import send_summary_email
from database import init_db, save_summary, list_summaries, get_summary,delete_summary,delete_all_summaries
from email_validator import validate_email, EmailNotValidError
# Init DB
init_db()

st.set_page_config(page_title="AI Meeting Summarizer", layout="wide")
st.title(" AI Meeting Notes Summarizer & Sharer")

# --- Session state ---
if "transcript" not in st.session_state:
    st.session_state["transcript"] = ""
if "summary" not in st.session_state:
    st.session_state["summary"] = ""

# --- Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Create a new summary")

    # Transcript input
    uploaded_file = st.file_uploader("Upload transcript (.txt)", type=["txt"])
    if uploaded_file:
        st.session_state["transcript"] = uploaded_file.read().decode("utf-8", errors="ignore")

    st.session_state["transcript"] = st.text_area(
        "Or paste transcript here",
        value=st.session_state["transcript"],
        height=250,
        key="transcript_area"
    )

    # Prompt + Title
    instruction = st.text_input(
        "Instruction / Prompt",
        value="Summarize the transcript into a concise structured summary with action items, decisions, and owners."
    )
    title = st.text_input("Summary title (for saving)")

    # Generate
    if st.button("Generate Summary"):
        if not st.session_state["transcript"].strip():
            st.warning("Please upload or paste a transcript before generating.")
        else:
            with st.spinner("Calling the LLM..."):
                prompt = f"INSTRUCTION: {instruction}\n\nTRANSCRIPT:\n{st.session_state['transcript']}"
                try:
                    st.session_state["summary"] = generate_summary(prompt)
                except Exception as e:
                    st.error(f"LLM call failed: {e}")
                    st.session_state["summary"] = f"(Error: {e})"

    # Editable summary (always visible after generation)
    if st.session_state["summary"]:
        st.subheader("Generated summary (editable)")
        st.session_state["summary"] = st.text_area(
            "Edit the generated summary",
            value=st.session_state["summary"],
            height=300,
            key="summary_area"
        )

        # --- Save to DB ---
        if st.button("Save summary to DB"):
            if st.session_state["summary"].strip():
                try:
                    save_summary(
                        title or "Meeting",             # title input
                        instruction,                    # prompt/instruction used
                        st.session_state["transcript"], # original transcript
                        st.session_state["summary"],    # generated summary (editable in textarea)
                        st.session_state["summary"]     # store edited version (same field here)
                    )
                    st.success("Summary saved to database!")
                except Exception as e:
                    st.error(f" Error saving to DB: {e}")
            else:
                st.warning(" No summary to save.")



        # --- Email ---
        recipients = st.text_input("Recipients (comma-separated)")
        subject = st.text_input("Email subject", f"Meeting Summary: {title or 'Untitled'}")
        if st.button("Send email"):
            if not recipients.strip():
                st.warning("Enter at least one recipient.")
            else:
                addrs = [a.strip() for a in recipients.split(",") if a.strip()]
                bad = []
                for a in addrs:
                    try:
                        validate_email(a)
                    except EmailNotValidError:
                        bad.append(a)
                if bad:
                    st.error(f"Invalid emails: {bad}")
                else:
                    body = f"<h2>{subject}</h2><pre>{st.session_state['summary']}</pre>"
                    try:
                        send_summary_email(addrs, subject, body)
                        st.success("Email sent!")
                    except Exception as e:
                        st.error(f"Email failed: {e}")

with col2:
    st.header("Saved Summaries")
    rows = list_summaries(limit=50)
    if st.button("Delete All Summaries"):
        from database import delete_all_summaries
        delete_all_summaries()
        st.success("All summaries deleted!")
        st.rerun()

    if not rows:
        st.info("No saved summaries yet.")
    else:
        for r in rows:
            with st.expander(f"{r.id} — {r.title} ({r.created_at:%Y-%m-%d %H:%M})"):
                st.markdown(f"**Prompt:** {r.prompt}")
                st.markdown(f"**Summary:**\n\n{r.generated_summary}")

                # Delete button
                if st.button(f"Delete summary {r.id}", key=f"del_{r.id}"):
                    from database import delete_summary
                    delete_summary(r.id)
                    st.success(f"Summary {r.id} deleted!")
                    st.rerun()
                
