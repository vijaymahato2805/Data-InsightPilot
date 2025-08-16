
import streamlit as st
def render_recommendations(data, processor):
    st.header('💡 Smart Recommendations')
    growth = processor.calculate_growth_metrics().get('monthly_growth_pct')
    if growth is None:
        st.write('Not enough data to recommend.')
        return
    if growth < 0:
        st.success('Revenue down — recommend marketing push and promotions.')
    elif growth < 5:
        st.info('Modest growth — optimise pricing and retention.')
    else:
        st.success('Good growth — scale up high-performing channels.')
