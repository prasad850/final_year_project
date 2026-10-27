import streamlit as st
import requests
import uuid

API = "http://localhost:8000"

st.set_page_config(page_title="Nova Memory Agent", page_icon="🧠", layout="wide")

# ── 1. Initialize Chat History in Session State ─────────────────
if "chats" not in st.session_state:
    # Create a default first chat
    default_id = str(uuid.uuid4())
    st.session_state.chats = {default_id: {"title": "New Chat", "messages": []}}
    st.session_state.current_chat = default_id

if "current_chat" not in st.session_state:
    st.session_state.current_chat = list(st.session_state.chats.keys())[0]

# ── 2. Sidebar: New Chat & History List ─────────────────────────
with st.sidebar:
    st.title("🧠 Nova Memory")
    
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        new_id = str(uuid.uuid4())
        st.session_state.chats[new_id] = {"title": "New Chat", "messages": []}
        st.session_state.current_chat = new_id
        st.rerun()

    st.markdown("---")
    st.markdown("### Recent Chats")

    # Show list of chats (reverse order so newest is at top)
    for chat_id, chat_data in reversed(list(st.session_state.chats.items())):
        # Highlight the active chat
        is_active = chat_id == st.session_state.current_chat
        
        # Use a primary button for active, secondary for inactive
        if st.button(
            f"💬 {chat_data['title']}", 
            key=chat_id, 
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.current_chat = chat_id
            st.rerun()

# ── 3. Main Chat Area ──────────────────────────────────────────
current_id = st.session_state.current_chat
current_chat = st.session_state.chats[current_id]

st.title("Ask the team memory")
st.caption("The system will answer using documents, or route you to an expert if it doesn't know.")

# Display previous messages in this chat
for msg in current_chat["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # If it's an assistant message, show citations or escalate cards
        if msg["role"] == "assistant" and "data" in msg:
            data = msg["data"]
            if data.get("escalate"):
                st.warning(f"🤔 I don't know. (confidence: {data.get('confidence', 0)})")
                if data.get("expert"):
                    st.info(f"Suggested expert: **{data['expert']['name']}**")
            else:
                st.caption(f"Confidence: {data.get('confidence', 0)}")
            
            if data.get("citations"):
                with st.expander("📚 Sources"):
                    for c in data["citations"]:
                        st.markdown(f"**{c['source']}** — {c['text']}")

# ── 4. Chat Input ──────────────────────────────────────────────
if prompt := st.chat_input("Ask a question (e.g., who decided to use AWS?)"):
    
    # If this is the first message, update the chat title in the sidebar
    if len(current_chat["messages"]) == 0:
        # Use the first 30 chars of the question as the title
        current_chat["title"] = prompt[:30] + "..." if len(prompt) > 30 else prompt

    # 1. Add user message to UI and state
    current_chat["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Call the FastAPI backend
    with st.chat_message("assistant"):
        with st.spinner("Searching memory and graph..."):
            try:
                response = requests.post(f"{API}/ask", json={"question": prompt})
                data = response.json()
                
                # Display the answer
                st.markdown(data["answer"])
                
                # Display confidence and sources (same logic as above)
                if data.get("escalate"):
                    st.warning(f"🤔 I don't know. (confidence: {data.get('confidence', 0)})")
                    if data.get("expert"):
                        st.info(f"Suggested expert: **{data['expert']['name']}** (knows {data['expert'].get('reason', '')})")
                else:
                    st.caption(f"Confidence: {data.get('confidence', 0)}")
                
                if data.get("citations"):
                    with st.expander("📚 Sources"):
                        for c in data["citations"]:
                            st.markdown(f"**{c['source']}** — {c['text']}")

                # 3. Save assistant message to state
                current_chat["messages"].append({
                    "role": "assistant", 
                    "content": data["answer"],
                    "data": data # Store raw data for rendering sources on scrollback
                })
                
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
                current_chat["messages"].pop() # Remove user message if backend failed

    # Note: No st.rerun() needed here! Streamlit handles chat_input reruns automatically.