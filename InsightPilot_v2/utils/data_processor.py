
import pandas as pd

class DataProcessor:
    def __init__(self, data):
        self.data = data or {}
    def get_data_summary(self):
        sales = self.data.get('sales')
        if sales is None or len(sales)==0:
            return {}
        sales = sales.copy()
        sales['date'] = pd.to_datetime(sales['date'])
        summary = {
            'total_revenue': float(sales['total_amount'].sum()),
            'total_orders': int(len(sales)),
            'average_order_value': float(sales['total_amount'].mean()),
            'start_date': str(sales['date'].min().date()),
            'end_date': str(sales['date'].max().date())
        }
        return summary
    def filter_data_by_date(self, start_date=None, end_date=None):
        sales = self.data.get('sales')
        if sales is None:
            return pd.DataFrame()
        df = sales.copy()
        df['date'] = pd.to_datetime(df['date'])
        if start_date:
            df = df[df['date'] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df['date'] <= pd.to_datetime(end_date)]
        return df
    def calculate_growth_metrics(self):
        sales = self.data.get('sales')
        if sales is None or len(sales)==0:
            return {}
        df = sales.copy()
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        monthly = df.groupby('month')['total_amount'].sum().sort_index()
        if len(monthly) < 2:
            return {'monthly_growth_pct': None}
        last = monthly.iloc[-1]
        prev = monthly.iloc[-2]
        growth = (last - prev) / prev * 100 if prev != 0 else None
        return {'monthly_growth_pct': float(growth) if growth is not None else None}
