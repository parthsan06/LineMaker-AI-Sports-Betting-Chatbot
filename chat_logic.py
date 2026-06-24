"""
Core chat logic for LineMaker AI.

This used to live inside main.py as a FastAPI endpoint (/api/chat) that
Streamlit called over HTTP at 127.0.0.1:8000. That only works when both
processes run on the same machine at the same time, which breaks on
single-process hosts like Streamlit Community Cloud or Render.

Same logic, same prompting strategy, same knowledge grounding -- just
called as a plain Python function from app.py instead of over the network.
"""

import os
from typing import List, Dict

from google import genai
from google.genai import types
from dotenv import load_dotenv

from knowledge import SYSTEM_PROMPT, KNOWLEDGE_BASE

load_dotenv()

_api_key = os.getenv("GEMINI_API_KEY")
if not _api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable is missing.")

_client = genai.Client(api_key=_api_key)


def build_grounded_prompt(user_message: str) -> str:
    """
    Injects our static knowledge base directly into the prompt context
    to ground the model's response before it answers.
    """
    context = (
        f"--- PLATFORM KNOWLEDGE BASE ---\n"
        f"Terminology: {KNOWLEDGE_BASE['terminology']}\n"
        f"Banking: {KNOWLEDGE_BASE['account_and_banking']}\n"
        f"Promotions: {KNOWLEDGE_BASE['promotions']}\n"
        f"Responsible Gaming: {KNOWLEDGE_BASE['responsible_gaming']}\n"
        f"--------------------------------\n\n"
        f"User Query: {user_message}"
    )
    return context


def get_chat_response(user_message: str, history: List[Dict[str, str]]) -> str:
    """
    history: list of {"role": "user"|"model", "text": str} dicts,
    same shape app.py already keeps in st.session_state.backend_history.
    """
    gemini_history = [
        types.Content(role=msg["role"], parts=[types.Part.from_text(text=msg["text"])])
        for msg in history
    ]

    chat = _client.chats.create(
        model="gemini-2.5-flash",  # Lightweight, fast model perfect for customer support
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.3,  # Low temperature keeps answers factual and deterministic
        ),
        history=gemini_history,
    )

    grounded_input = build_grounded_prompt(user_message)
    response = chat.send_message(grounded_input)
    return response.text
