"""
email_utils.py

Utility to send emails via SMTP using standard library smtplib.
"""

import os
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
import streamlit as st

SMTP_HOST = os.getenv("SMTP_HOST") or st.secrets.get("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", st.secrets.get("SMTP_PORT", 587)))
SMTP_USERNAME = os.getenv("SMTP_USERNAME") or st.secrets.get("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD") or st.secrets.get("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM") or st.secrets.get("SMTP_FROM")

def send_summary_email(to_addresses, subject, body_html, body_text=None):
    """
    Send the edited summary to one or more recipients.

    - to_addresses: list[str] or comma-separated str
    - body_html: HTML string (we include also text fallback)
    - body_text: optional plain text version
    """
    if isinstance(to_addresses, str):
        to_addresses = [addr.strip() for addr in to_addresses.split(",") if addr.strip()]

    if not SMTP_HOST or not SMTP_USERNAME or not SMTP_PASSWORD or not SMTP_FROM:
        raise RuntimeError("SMTP config incomplete. Please set SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD, SMTP_FROM.")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_FROM
    msg["To"] = ", ".join(to_addresses)

    # unique cid for possible inline images (not used here, but safe)
    msg_id = make_msgid()
    msg["Message-ID"] = msg_id

    if not body_text:
        # very basic fallback: strip HTML tags (naive)
        import re
        body_text = re.sub(r'<[^>]+>', '', body_html)

    msg.set_content(body_text)
    msg.add_alternative(body_html, subtype="html")

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
