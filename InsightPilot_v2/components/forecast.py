
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import timedelta

def simple_linear_forecast(series, periods=30):
    # series: pd.Series with datetime index and numeric values
    s = series.dropna()
    if len(s) < 2:
        return None
    # convert dates to ordinal for regression
    x = np.array([d.toordinal() for d in s.index])
    y = s.values
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    last = s.index.max().toordinal()
    future_dates = [pd.to_datetime(t) for t in [ (last + i) for i in range(1, periods+1) ]]
    preds = [m*d.toordinal() + c for d in future_dates]
    return pd.Series(preds, index=future_dates)

def render_forecast(data, processor):
    st.header('🔮 Forecast: Simple Linear Forecast Demo')
    sales = data.get('sales')
    if sales is None or len(sales)==0:
        st.warning('No sales data available. Upload data or use sample data.')
        return
    df = sales.copy()
    df['date'] = pd.to_datetime(df['date'])
    daily = df.groupby('date')['total_amount'].sum().sort_index()
    periods = st.sidebar.number_input('Forecast periods (days)', min_value=7, max_value=365, value=30)
    forecast = simple_linear_forecast(daily, periods=periods)
    if forecast is None:
        st.info('Not enough data to forecast.')
        return
    chart_df = pd.concat([daily, forecast.rename('forecast')], axis=0)
    fig = px.line(x=chart_df.index, y=chart_df.values, labels={'x':'date','y':'amount'}, title='Sales + Forecast (simple linear)')
    st.plotly_chart(fig, use_container_width=True)
    st.write('Forecast (next rows):')
    st.dataframe(forecast.head(20).rename('predicted_amount').reset_index().rename(columns={'index':'date'}))
