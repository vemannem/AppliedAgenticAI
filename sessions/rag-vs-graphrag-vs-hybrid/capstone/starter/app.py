"""Minimal Streamlit demo app for the capstone.

Run:
    streamlit run app.py
"""

import streamlit as st
from hybrid_router import answer_question

st.set_page_config(page_title="Hybrid RAG Capstone", layout="wide")
st.title("Enterprise Knowledge Intelligence Platform")
st.caption("Traditional RAG + GraphRAG + Hybrid retrieval")

query = st.text_area("Ask a question", value="Compare RAG and GraphRAG.", height=100)

if st.button("Answer", type="primary"):
    with st.spinner("Retrieving context and generating answer..."):
        result = answer_question(query)

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Route")
    st.code(result["route"])

    with st.expander("Vector hits"):
        for hit in result["vector_hits"]:
            st.markdown(f"**{hit['metadata'].get('title')} — page {hit['metadata'].get('page')}**")
            st.write(hit["text"][:1000])

    with st.expander("Graph facts"):
        for fact in result["graph_hits"]:
            st.write(fact)
