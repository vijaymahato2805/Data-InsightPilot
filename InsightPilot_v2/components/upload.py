
import streamlit as st
import pandas as pd

def infer_sales_df(df):
    # Try to map columns to expected ones
    lower = {c.lower(): c for c in df.columns}
    mapping = {}
    for expected in ['date','total_amount','amount','quantity','product','product_id','customer','region']:
        if expected in lower:
            mapping[expected] = lower[expected]
    # If there's 'amount' use it as total_amount
    if 'total_amount' not in df.columns and 'amount' in mapping:
        df['total_amount'] = df[mapping.get('amount')]
    return df

def render_upload(data, processor):
    st.header('📥 Upload Data (CSV / Excel)')
    st.write('Upload a CSV or Excel file containing sales-like data (date, total_amount, product_id, region, quantity).')
    uploaded = st.file_uploader('Choose CSV or Excel', type=['csv','xlsx','xls'])
    if uploaded is not None:
        try:
            if uploaded.name.lower().endswith('.csv'):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            df = infer_sales_df(df)
            st.success(f'Loaded {len(df)} rows from {uploaded.name}')
            st.dataframe(df.head(10))
            if st.button('Use this data as sales dataset'):
                # replace sales in global data
                data['sales'] = df
                processor.data = data
                st.experimental_rerun()
        except Exception as e:
            st.error(f'Failed to load file: {e}')
    else:
        st.info('No file uploaded. You can use sample data from the Dashboard.')
