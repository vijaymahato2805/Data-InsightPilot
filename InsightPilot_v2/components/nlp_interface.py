
import streamlit as st
def render_nlp_interface(data, processor):
    st.header('💬 Natural Language Query')
    st.write('Type a question about the dataset. (Simple demo)')
    q = st.text_input('Ask anything')
    if q:
        summary = processor.get_data_summary()
        st.write('I am not an LLM here, but here is a data summary:')
        st.json(summary)
