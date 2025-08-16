import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class AnalyticsService:
    """Service for business analytics and KPI calculations"""
    
    def __init__(self, data):
        self.data = data
        
    def calculate_kpis(self):
        """Calculate key performance indicators"""
        try:
            sales_df = self.data['sales']
            customers_df = self.data['customers']
            products_df = self.data['products']
            
            # Time periods
            current_date = sales_df['date'].max()
            last_30_days = current_date - timedelta(days=30)
            last_90_days = current_date - timedelta(days=90)
            last_year = current_date - timedelta(days=365)
            
            # Revenue metrics
            total_revenue = sales_df['total_amount'].sum()
            revenue_30d = sales_df[sales_df['date'] >= last_30_days]['total_amount'].sum()
            revenue_90d = sales_df[sales_df['date'] >= last_90_days]['total_amount'].sum()
            
            # Customer metrics
            total_customers = len(customers_df)
            active_customers_30d = len(sales_df[sales_df['date'] >= last_30_days]['customer_id'].unique())
            
            # Order metrics
            total_orders = len(sales_df)
            avg_order_value = sales_df['total_amount'].mean()
            
            # Product metrics
            top_products = (sales_df.groupby('product_id')['total_amount']
                          .sum().sort_values(ascending=False).head(5))
            
            # Growth rates
            revenue_prev_30d = sales_df[
                (sales_df['date'] >= last_30_days - timedelta(days=30)) & 
                (sales_df['date'] < last_30_days)
            ]['total_amount'].sum()
            
            revenue_growth_rate = ((revenue_30d - revenue_prev_30d) / revenue_prev_30d * 100) if revenue_prev_30d > 0 else 0
            
            return {
                'total_revenue': round(total_revenue, 2),
                'revenue_30d': round(revenue_30d, 2),
                'revenue_90d': round(revenue_90d, 2),
                'revenue_growth_rate': round(revenue_growth_rate, 2),
                'total_customers': total_customers,
                'active_customers_30d': active_customers_30d,
                'total_orders': total_orders,
                'avg_order_value': round(avg_order_value, 2),
                'top_products': top_products.to_dict()
            }
            
        except Exception as e:
            return {"error": f"KPI calculation failed: {str(e)}"}
    
    def regional_analysis(self):
        """Analyze performance by region"""
        try:
            sales_df = self.data['sales']
            customers_df = self.data['customers']
            
            # Merge sales with customer region data
            sales_with_region = sales_df.merge(
                customers_df[['customer_id', 'region']], 
                on='customer_id', 
                how='left'
            )
            
            regional_metrics = sales_with_region.groupby('region').agg({
                'total_amount': ['sum', 'mean', 'count'],
                'customer_id': 'nunique'
            }).round(2)
            
            regional_metrics.columns = [
                'total_revenue', 'avg_order_value', 'total_orders', 'unique_customers'
            ]
            
            # Calculate revenue per customer
            regional_metrics['revenue_per_customer'] = (
                regional_metrics['total_revenue'] / regional_metrics['unique_customers']
            ).round(2)
            
            return regional_metrics.to_dict('index')
            
        except Exception as e:
            return {"error": f"Regional analysis failed: {str(e)}"}
    
    def product_analysis(self):
        """Analyze product performance"""
        try:
            sales_df = self.data['sales']
            products_df = self.data['products']
            
            # Product performance metrics
            product_metrics = sales_df.groupby('product_id').agg({
                'total_amount': ['sum', 'mean'],
                'quantity': 'sum',
                'sale_id': 'count'
            }).round(2)
            
            product_metrics.columns = ['total_revenue', 'avg_sale_amount', 'total_quantity', 'total_sales']
            
            # Merge with product details
            product_analysis = product_metrics.merge(
                products_df[['product_id', 'product_name', 'category', 'unit_price', 'cost']], 
                on='product_id', 
                how='left'
            )
            
            # Calculate profit margins
            product_analysis['total_profit'] = (
                product_analysis['total_revenue'] - 
                (product_analysis['total_quantity'] * product_analysis['cost'])
            ).round(2)
            
            product_analysis['profit_margin'] = (
                product_analysis['total_profit'] / product_analysis['total_revenue'] * 100
            ).round(2)
            
            # Sort by total revenue
            product_analysis = product_analysis.sort_values('total_revenue', ascending=False)
            
            return product_analysis.to_dict('records')
            
        except Exception as e:
            return {"error": f"Product analysis failed: {str(e)}"}
    
    def time_series_analysis(self):
        """Analyze trends over time"""
        try:
            sales_df = self.data['sales']
            
            # Daily trends
            daily_trends = sales_df.groupby('date').agg({
                'total_amount': 'sum',
                'quantity': 'sum',
                'sale_id': 'count'
            }).reset_index()
            
            daily_trends.columns = ['date', 'daily_revenue', 'daily_quantity', 'daily_orders']
            
            # Weekly trends
            sales_df['week'] = sales_df['date'].dt.to_period('W')
            weekly_trends = sales_df.groupby('week').agg({
                'total_amount': 'sum',
                'quantity': 'sum',
                'sale_id': 'count'
            }).reset_index()
            
            weekly_trends['week'] = weekly_trends['week'].astype(str)
            weekly_trends.columns = ['week', 'weekly_revenue', 'weekly_quantity', 'weekly_orders']
            
            # Monthly trends
            sales_df['month'] = sales_df['date'].dt.to_period('M')
            monthly_trends = sales_df.groupby('month').agg({
                'total_amount': 'sum',
                'quantity': 'sum',
                'sale_id': 'count'
            }).reset_index()
            
            monthly_trends['month'] = monthly_trends['month'].astype(str)
            monthly_trends.columns = ['month', 'monthly_revenue', 'monthly_quantity', 'monthly_orders']
            
            return {
                'daily': daily_trends.to_dict('records'),
                'weekly': weekly_trends.to_dict('records'),
                'monthly': monthly_trends.to_dict('records')
            }
            
        except Exception as e:
            return {"error": f"Time series analysis failed: {str(e)}"}
    
    def customer_analysis(self):
        """Analyze customer behavior and segments"""
        try:
            sales_df = self.data['sales']
            customers_df = self.data['customers']
            
            # Customer lifetime value analysis
            customer_metrics = sales_df.groupby('customer_id').agg({
                'total_amount': ['sum', 'mean', 'count'],
                'date': ['min', 'max']
            }).reset_index()
            
            customer_metrics.columns = [
                'customer_id', 'total_spent', 'avg_order_value', 
                'order_count', 'first_purchase', 'last_purchase'
            ]
            
            # Merge with customer data
            customer_analysis = customer_metrics.merge(customers_df, on='customer_id', how='left')
            
            # Calculate customer lifetime (days)
            customer_analysis['customer_lifetime_days'] = (
                customer_analysis['last_purchase'] - customer_analysis['first_purchase']
            ).dt.days
            
            # Segment analysis
            segment_analysis = customer_analysis.groupby('customer_segment').agg({
                'total_spent': ['sum', 'mean'],
                'order_count': 'mean',
                'customer_lifetime_days': 'mean'
            }).round(2)
            
            # Regional customer analysis
            regional_customer_analysis = customer_analysis.groupby('region').agg({
                'total_spent': ['sum', 'mean'],
                'order_count': 'mean',
                'customer_id': 'count'
            }).round(2)
            
            return {
                'customer_metrics': customer_analysis.to_dict('records'),
                'segment_analysis': segment_analysis.to_dict('index'),
                'regional_customer_analysis': regional_customer_analysis.to_dict('index')
            }
            
        except Exception as e:
            return {"error": f"Customer analysis failed: {str(e)}"}
