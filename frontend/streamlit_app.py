import streamlit as st
import requests
import uuid

API = "http://localhost:8000"
st.set_page_config(page_title="Nova Memory Agent", page_icon="🧠", layout="wide")

# ── Custom CSS for the Landing Page ──────────────────────────
st.markdown("""
<style>
    .hero-title { font-size: 3.5rem; font-weight: 800; color: #1e3a8a; line-height: 1.1; margin-bottom: 1rem; }
    .hero-highlight { color: #8b5cf6; }
    .hero-sub { font-size: 1.1rem; color: #475569; margin-bottom: 2rem; }
    .feature-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05); height: 100%; }
    .feature-title { font-size: 1.25rem; font-weight: 700; color: #0f172a; margin-bottom: 10px; }
    .feature-text { color: #64748b; font-size: 0.95rem; }
</style>
""", unsafe_allow_html=True)

# ── 1. Session State ──────────────────────────────────────────
if "role" not in st.session_state:
    st.session_state.role = None

if "chats" not in st.session_state:
    st.session_state.chats = {}
    
if "expert_inbox" not in st.session_state:
    st.session_state.expert_inbox = []

# ── 2. Landing Page (Inspired by image) ───────────────────────
if st.session_state.role is None:
    st.write("##")
    st.markdown('<div class="hero-title">Remember the <span class="hero-highlight">why</span><br>behind every decision.</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Nova connects documents, decisions, and people using a Knowledge Graph. Employees ask, experts review, and the system learns.</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="feature-card"><div class="feature-title">Capture</div><div class="feature-text">Record decisions, owners, and reasons from raw documents using LLMs.</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="feature-card"><div class="feature-title">Route</div><div class="feature-text">When the AI doesn\'t know, it queries Neo4j to find the exact human expert.</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="feature-card"><div class="feature-title">Save</div><div class="feature-text">Experts save answers to permanent memory, making the system smarter instantly.</div></div>', unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("Select a role to enter the demo")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👤 **Guest**\n\nDiscover public documents only", use_container_width=True, type="primary"):
            st.session_state.role = "Guest"
            st.rerun()
    with col2:
        if st.button("🧑‍💻 **Employee**\n\nAsk questions, discover context, route to experts", use_container_width=True, type="primary"):
            st.session_state.role = "Employee"
            st.rerun()
    with col3:
        if st.button("👑 **Project Head**\n\nReview proposals, answer questions, save to memory", use_container_width=True, type="primary"):
            st.session_state.role = "Head"
            st.rerun()
    st.stop()

# ── 3. Sidebar ────────────────────────────────────────────────
with st.sidebar:
    st.title(f"🧠 {st.session_state.role}")
    if st.button("🚪 Logout / Switch Role"):
        st.session_state.role = None
        st.session_state.chats = {}
        st.session_state.current_chat = None
        st.rerun()
    
    st.markdown("---")
    
    if st.session_state.role in ["Employee", "Guest"]:
        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            new_id = str(uuid.uuid4())
            st.session_state.chats[new_id] = {"title": "New Chat", "messages": []}
            st.session_state.current_chat = new_id
            st.rerun()

        st.markdown("### Recent Chats")
        for chat_id, chat_data in reversed(list(st.session_state.chats.items())):
            is_active = chat_id == st.session_state.get("current_chat")
            if st.button(f"💬 {chat_data['title']}", key=chat_id, use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state.current_chat = chat_id
                st.rerun()

# ── 4. Head Account (Inbox) ───────────────────────────────────
if st.session_state.role == "Head":
    st.title("👑 Project Head Inbox")
    st.write("Answer questions routed by Employees. Your answers become permanent memory.")
    
    if len(st.session_state.expert_inbox) == 0:
        st.info("No pending questions. (Log in as Employee, ask a question, and click 'Send to Expert' to test this).")
    
    # Iterate over a copy of the list to safely remove items
    for idx, item in enumerate(list(st.session_state.expert_inbox)):
        with st.expander(f"❓ {item['question']} (Asked to {item['expert_name']})", expanded=True):
            answer = st.text_area("Your Answer", key=f"ans_{idx}")
            if st.button("💾 Save to Permanent Memory", key=f"save_{idx}", type="primary"):
                requests.post(f"{API}/save", json={
                    "question": item['question'],
                    "answer": answer,
                    "person": item['expert_name']
                })
                st.success("✅ Saved! This answer will now appear in the Employee's chat.")
                st.session_state.expert_inbox.pop(idx)
                st.rerun()

# ── 5. Chat Interface (Employee & Guest) ──────────────────────
elif st.session_state.role in ["Employee", "Guest"]:
    
    # Ensure a chat exists
    if not st.session_state.chats:
        new_id = str(uuid.uuid4())
        st.session_state.chats[new_id] = {"title": "New Chat", "messages": []}
        st.session_state.current_chat = new_id

    if "current_chat" not in st.session_state or st.session_state.current_chat not in st.session_state.chats:
        st.session_state.current_chat = list(st.session_state.chats.keys())[0]

    chat_id = st.session_state.current_chat
    current_chat = st.session_state.chats[chat_id]
    
    st.title(f"💬 {current_chat['title']}")

    # 1. Render History
    for msg_idx, msg in enumerate(current_chat["messages"]):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
            if msg["role"] == "assistant" and "data" in msg:
                data = msg["data"]
                if data.get("escalate"):
                    st.warning(f"🤔 I don't know. (confidence: {data.get('confidence', 0)})")
                    if data.get("expert"):
                        expert = data["expert"]
                        st.info(f"👤 **Suggested Expert: {expert['name']}**\n\n*{expert['reason']}*")
                        
                        if st.session_state.role == "Employee":
                            if st.button(f"📨 Send to {expert['name']}", key=f"hist_send_{msg_idx}"):
                                st.session_state.expert_inbox.append({
                                    "question": current_chat["messages"][msg_idx-1]["content"], 
                                    "expert_name": expert['name']
                                })
                                st.success("Question sent to Head's Inbox! (Switch role to Head to answer).")
                else:
                    st.caption(f"Confidence: {data.get('confidence', 0)}")
                
                if data.get("citations"):
                    with st.expander("📚 Sources"):
                        for c in data["citations"]:
                            st.markdown(f"**{c['source']}** — {c['text']}")

    # 2. Chat Input
    if prompt := st.chat_input("Ask a question..."):
        # Auto-title update
        if len(current_chat["messages"]) == 0:
            current_chat["title"] = prompt[:30] + "..." if len(prompt) > 30 else prompt

        # Append user message immediately
        current_chat["messages"].append({"role": "user", "content": prompt})
        
        # 3. Display live user message and AI response
        with st.chat_message("assistant"):
            with st.spinner("Searching..."):
                response = requests.post(f"{API}/ask", json={
                    "question": prompt,
                    "role": st.session_state.role
                })
                data = response.json()
                
                st.markdown(data["answer"])
                if data.get("escalate"):
                    st.warning(f"🤔 I don't know. (confidence: {data.get('confidence', 0)})")
                    if data.get("expert"):
                        expert = data["expert"]
                        st.info(f"👤 **Suggested Expert: {expert['name']}**\n\n*{expert['reason']}*")
                        
                        if st.session_state.role == "Employee":
                            if st.button(f"📨 Send to {expert['name']}", key=f"live_send_{len(current_chat['messages'])}"):
                                st.session_state.expert_inbox.append({
                                    "question": prompt,
                                    "expert_name": expert['name']
                                })
                                st.success("Question sent to Head's Inbox! (Logout and switch to Head to answer).")
                else:
                    st.caption(f"Confidence: {data.get('confidence', 0)}")
                    
                if data.get("citations"):
                    with st.expander("📚 Sources"):
                        for c in data["citations"]:
                            st.markdown(f"**{c['source']}** — {c['text']}")

                # Save assistant message to state
                current_chat["messages"].append({
                    "role": "assistant", 
                    "content": data["answer"],
                    "data": data
                })
        
        # Force a rerun so the sidebar title updates immediately
        st.rerun()