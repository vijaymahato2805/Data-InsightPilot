
import streamlit as st
import pandas as pd
def render_anomaly_detection(data, processor):
    st.header('🚨 Anomaly Detection')
    df = processor.filter_data_by_date()
    if df.empty:
        st.info('No sales data')
        return
    # simple anomaly: orders with total_amount > mean + 3*std
    thresh = df['total_amount'].mean() + 3*df['total_amount'].std()
    anomalies = df[df['total_amount'] > thresh]
    st.write(f'Found {len(anomalies)} anomalies (amount > {thresh:.2f})')
    st.dataframe(anomalies.head(50))
