import streamlit as st
import requests

API = "http://localhost:8000"

st.set_page_config(page_title="Nova Memory Agent", page_icon="🧠")
st.title("🧠 Nova Memory Agent")

q = st.text_input("Ask a question", placeholder="e.g., Have we done ERP migration before?")

if st.button("Ask", type="primary") and q:
    with st.spinner("Thinking..."):
        r = requests.post(f"{API}/ask", json={"question": q}).json()

    if r["escalate"]:
        st.warning(f"🤔 I don't know. (confidence: {r['confidence']})")
        if r.get("expert"):
            st.info(f"Suggested expert: **{r['expert']['name']}** (knows {r['expert'].get('skill', '')})")
    else:
        st.markdown(r["answer"])
        st.caption(f"Confidence: {r['confidence']}")
        if r["citations"]:
            st.markdown("### 📚 Sources")
            for c in r["citations"]:
                with st.expander(c["source"]):
                    st.write(c["text"])