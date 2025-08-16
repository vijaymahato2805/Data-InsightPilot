
import streamlit as st
import plotly.express as px
import pandas as pd
import io

def render_dashboard(data, processor):
    st.header('📊 Dashboard (Improved)')
    sales = data.get('sales')
    if sales is None or len(sales)==0:
        st.warning('No sales data. Upload data or use sample.')
        return
    df = sales.copy()
    df['date'] = pd.to_datetime(df['date'])
    # Filters
    with st.sidebar.expander('Filters', expanded=False):
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        start = st.date_input('Start date', min_date)
        end = st.date_input('End date', max_date)
        product = None
        if 'product_id' in df.columns:
            product = st.multiselect('Product', options=sorted(df['product_id'].unique().tolist()))
        region = None
        if 'region' in df.columns:
            region = st.multiselect('Region', options=sorted(df['region'].unique().tolist()))
    # apply filters
    mask = (df['date'].dt.date >= start) & (df['date'].dt.date <= end)
    if product:
        mask &= df['product_id'].isin(product)
    if region:
        mask &= df['region'].isin(region)
    filtered = df[mask]
    # KPIs
    total_rev = filtered['total_amount'].sum()
    total_orders = len(filtered)
    aov = filtered['total_amount'].mean() if total_orders>0 else 0
    col1, col2, col3 = st.columns(3)
    col1.metric('Total Revenue', f'₹{total_rev:,.2f}')
    col2.metric('Total Orders', f'{total_orders}')
    col3.metric('Avg Order Value', f'₹{aov:,.2f}')
    # Charts
    daily = filtered.groupby(filtered['date'].dt.date)['total_amount'].sum().reset_index().rename(columns={'date':'day'})
    fig = px.line(daily, x='day', y='total_amount', title='Daily Sales')
    st.plotly_chart(fig, use_container_width=True)
    if 'product_id' in filtered.columns:
        prod = filtered.groupby('product_id')['total_amount'].sum().reset_index().sort_values('total_amount', ascending=False).head(10)
        fig2 = px.bar(prod, x='product_id', y='total_amount', title='Top Products')
        st.plotly_chart(fig2, use_container_width=True)
    # Export filtered data
    buf = io.BytesIO()
    filtered.to_csv(buf, index=False)
    buf.seek(0)
    st.download_button('Download filtered CSV', data=buf, file_name='filtered_sales.csv', mime='text/csv')
    st.dataframe(filtered.head(200))
