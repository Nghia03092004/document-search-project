import streamlit as st
import requests

st.title("📰 Vietnamese News Search")

query = st.text_input("Input key words")

top_k = st.slider("Number results", 1, 10, 3)

if st.button("Search"):
    r = requests.post(
        "http://127.0.0.1:8000/query",
        json={"query": query, "top_k": top_k}
    )

    st.write("STATUS:", r.status_code)

    if r.status_code != 200:
        st.text("RAW RESPONSE:")
        st.text(r.text)
    else:
        data = r.json()
        for res in data["results"]:
            st.write(f"**Score:** {res['score']}")
            st.write(res["text"])
            st.divider()
