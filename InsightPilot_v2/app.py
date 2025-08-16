
import streamlit as st
from data.sample_business_data import load_sample_data
from utils.data_processor import DataProcessor
from components.dashboard import render_dashboard
from components.upload import render_upload
from components.forecast import render_forecast
from components.ai_chat import render_ai_chat
from components.predictions import render_predictions
from components.anomaly_detection import render_anomaly_detection
from components.recommendations import render_recommendations

def main():
    st.set_page_config(page_title='InsightPilot v2', layout='wide')
    st.title('InsightPilot — v2 (Upload · Forecast · AI Chat)')
    
    # Load sample data into session state if not present
    if 'data' not in st.session_state:
        st.session_state.data = load_sample_data()
        st.session_state.processor = DataProcessor(st.session_state.data)
    
    pages = {
        "📊 Dashboard": render_dashboard,
        "📥 Upload": render_upload,
        "🔮 Forecast": render_forecast,
        "🤖 AI Chat": render_ai_chat,
        "📈 Predictive Analytics": render_predictions,
        "🚨 Anomaly Detection": render_anomaly_detection,
        "💡 Smart Recommendations": render_recommendations
    }
    
    page = st.sidebar.selectbox("Select page", list(pages.keys()))
    pages[page](st.session_state.data, st.session_state.processor)

if __name__ == '__main__':
    main()
