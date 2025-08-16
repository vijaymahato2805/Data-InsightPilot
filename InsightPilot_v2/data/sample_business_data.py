
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def load_sample_data(num_days=90):
    np.random.seed(42)
    today = datetime.now().date()
    dates = [today - timedelta(days=i) for i in range(num_days)][::-1]
    sales = []
    products = [{'product_id': f'P{i:03}', 'name': f'Product {i}'} for i in range(1,6)]
    customers = [{'customer_id': f'C{i:03}', 'name': f'Customer {i}'} for i in range(1,11)]
    regions = ['North','South','East','West']
    for d in dates:
        for _ in range(np.random.randint(3,8)):
            prod = np.random.choice(products)
            cust = np.random.choice(customers)
            amount = round(np.random.uniform(50, 1500),2)
            qty = np.random.randint(1,10)
            sales.append({
                'date': pd.to_datetime(d),
                'product_id': prod['product_id'],
                'customer_id': cust['customer_id'],
                'region': np.random.choice(regions),
                'quantity': qty,
                'total_amount': round(amount*qty,2)
            })
    sales_df = pd.DataFrame(sales)
    customers_df = pd.DataFrame(customers)
    products_df = pd.DataFrame(products)
    regions_df = pd.DataFrame([{'region': r} for r in regions])
    expenses_df = pd.DataFrame([{'date': pd.to_datetime(today - timedelta(days=i)),
                                 'amount': round(np.random.uniform(200,2000),2)} for i in range(0,30)])
    return {
        'sales': sales_df,
        'customers': customers_df,
        'products': products_df,
        'regions': regions_df,
        'expenses': expenses_df
    }
