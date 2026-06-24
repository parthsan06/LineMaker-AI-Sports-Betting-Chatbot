# LineMaker AI: Sports Betting Chatbot

A customer-support chat system for a sports betting platform, with strict context-grounding and compliance-first prompt design. The architecture is a single-process application: a reactive Streamlit interface invoking a stateless, validated chat-logic module directly — no network boundary between UI and inference layer.

## System Architecture

The system implements a grounded-prompt pattern, injecting platform-specific context ahead of every LLM call rather than relying on the model's general knowledge or a fine-tuned weight set.

1. **Streamlit Frontend:** Renders the conversation, captures input via `st.chat_input`, and maintains two parallel session-state histories — one for UI display, one pre-formatted to the role schema (`user`/`model`) the Gemini API expects.

2. **Chat Logic Module:** The processing core. Builds a grounded prompt by inlining the full structured knowledge base ahead of the user's query, reconstructs a Gemini chat session from the stored history on every turn (stateless by design — no persistent session object is held server-side), and issues the call with a fixed system instruction and low-temperature config.

## Technical Core Highlights

- **Context Grounding (RAG-lite):** Replaces fine-tuning or vector-indexing overhead for a small, static knowledge surface by inlining structured platform facts (terminology, banking, promotions, responsible gaming) directly into the prompt before each query reaches the model. Appropriate at this scale; the natural next step at larger knowledge-base size is retrieval (embeddings + vector search) instead of full inlining.

- **Compliance-First System Instruction:** The system prompt enforces three non-negotiable rules ahead of general support behavior — surfacing the responsible-gaming helpline immediately on any distress signal, withholding legal/financial advice, and redirecting off-topic queries. Ordering is deliberate: compliance checks take precedence over conversational helpfulness.

- **Stateless Session Reconstruction:** Rather than holding a persistent chat object across turns, each request rebuilds a fresh Gemini chat session from the full stored history (`role: user/model` pairs). Conversational memory is preserved without a database or server-side session store — state lives entirely in the Streamlit session for the duration of the browser tab.

- **Deterministic Output Tuning:** Temperature fixed at 0.3 to keep answers on betting rules, deposits, and policy factual and repeatable rather than creative.

## Architecture Note — Revised from Initial Version

The version originally scaffolded here split this into two processes: a FastAPI backend exposing a `/api/chat` endpoint, validated via Pydantic request/response models, called by Streamlit over HTTP at `127.0.0.1:8000`. That separation is the correct pattern once this needs to serve more than one client or needs request-level validation, auth, and logging independent of the UI. For a single-host deployment target (Streamlit Community Cloud), the network boundary was removed and the same grounding logic, system prompt, and Gemini call now run as a direct in-process function call. No behavior changed — only the transport between UI and logic layer, from HTTP to a function call. See `architecture.png` for the original two-process diagram; the FastAPI structure is the documented path back if/when this needs to scale beyond one Streamlit frontend (see Future Enhancements in the project documentation).

## Tech Stack

- **Language:** Python 3.11+
- **Frontend / Application Shell:** Streamlit (reactive redraw loop)
- **Model Pipeline:** Google GenAI SDK (`gemini-2.5-flash`)
- **Config:** `.env`-based key management via `python-dotenv` locally; Streamlit Cloud secrets in deployment

## Getting Started

1. **Install dependencies:**
```
pip install -r requirements.txt
```

2. **Configure environment:**

Create a `.env` file in the root directory:
```
GEMINI_API_KEY="your_api_key_here"
```

3. **Run:**
```
streamlit run app.py
```

**Live demo:** [gotta add a Streamlit Cloud link here]
