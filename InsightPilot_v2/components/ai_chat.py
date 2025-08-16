
import streamlit as st
import pandas as pd
import numpy as np
import os

def local_answer(question, data, processor):
    q = question.lower()
    sales = data.get('sales')
    if sales is None or len(sales)==0:
        return "No sales data available."
    df = sales.copy()
    df['date'] = pd.to_datetime(df['date'])
    if 'highest' in q and 'month' in q:
        monthly = df.groupby(df['date'].dt.to_period('M'))['total_amount'].sum()
        top = monthly.idxmax(), monthly.max()
        return f"Highest month was {top[0].strftime('%Y-%m')} with revenue {top[1]:.2f}"
    if 'top' in q and 'product' in q:
        if 'product_id' in df.columns:
            p = df.groupby('product_id')['total_amount'].sum().sort_values(ascending=False).head(5)
            return 'Top products (by revenue):\n' + p.to_string()
        return 'No product_id column found in data.'
    if 'total revenue' in q or 'total sales' in q:
        total = df['total_amount'].sum()
        return f'Total revenue: {total:.2f}'
    if 'average order' in q or 'aov' in q:
        return f'Average order value: {df["total_amount"].mean():.2f}'
    return 'Sorry — I could not parse the question. Try phrases like "highest month", "top product", "total revenue".'

def render_ai_chat(data, processor):
    st.header('🤖 AI Chat (Local + Optional OpenAI)')
    st.write('Ask questions about the dataset. If you provide an OpenAI API key below, the app will try to call OpenAI to answer more complex queries.')
    use_openai = False
    openai_key = st.text_input('OpenAI API Key (optional)', type='password')
    if openai_key:
        try:
            import openai
            openai.api_key = openai_key.strip()
            use_openai = True
        except Exception as e:
            st.warning('OpenAI package not installed or failed to import; will use local parser.')
    q = st.text_input('Ask a question (examples: "highest month", "top product", "total revenue")')
    if st.button('Ask') and q:
        if use_openai:
            try:
                # create a short context from data summary
                summary = processor.get_data_summary()
                prompt = f"""You are a helpful assistant answering questions about a sales dataset. Summary: {summary}. Question: {q}"""
                import openai
                resp = openai.Completion.create(model='text-davinci-003', prompt=prompt, max_tokens=200)
                st.write(resp.choices[0].text.strip())
            except Exception as e:
                st.error(f'OpenAI call failed: {e}')
                st.write(local_answer(q, data, processor))
        else:
            st.write(local_answer(q, data, processor))
