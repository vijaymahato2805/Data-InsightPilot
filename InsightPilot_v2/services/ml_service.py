import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

class MLService:
    """Service for machine learning models and predictions"""
    
    def __init__(self):
        self.sales_model = None
        self.anomaly_detector = None
        self.scaler = StandardScaler()
        
    def prepare_sales_features(self, sales_df):
        """Prepare features for sales prediction"""
        # Create time-based features
        sales_df['year'] = sales_df['date'].dt.year
        sales_df['month'] = sales_df['date'].dt.month
        sales_df['day_of_week'] = sales_df['date'].dt.dayofweek
        sales_df['day_of_year'] = sales_df['date'].dt.dayofyear
        sales_df['quarter'] = sales_df['date'].dt.quarter
        
        # Aggregate daily sales
        daily_sales = sales_df.groupby('date').agg({
            'total_amount': 'sum',
            'quantity': 'sum',
            'sale_id': 'count'
        }).reset_index()
        
        daily_sales.columns = ['date', 'daily_revenue', 'daily_quantity', 'daily_transactions']
        
        # Add time features
        daily_sales['year'] = daily_sales['date'].dt.year
        daily_sales['month'] = daily_sales['date'].dt.month
        daily_sales['day_of_week'] = daily_sales['date'].dt.dayofweek
        daily_sales['day_of_year'] = daily_sales['date'].dt.dayofyear
        daily_sales['quarter'] = daily_sales['date'].dt.quarter
        
        # Add rolling averages
        daily_sales = daily_sales.sort_values('date')
        daily_sales['revenue_ma_7'] = daily_sales['daily_revenue'].rolling(window=7, min_periods=1).mean()
        daily_sales['revenue_ma_30'] = daily_sales['daily_revenue'].rolling(window=30, min_periods=1).mean()
        
        return daily_sales
    
    def train_sales_prediction_model(self, sales_df):
        """Train sales prediction model"""
        try:
            # Prepare features
            features_df = self.prepare_sales_features(sales_df)
            
            # Select features for model
            feature_columns = [
                'month', 'day_of_week', 'day_of_year', 'quarter',
                'daily_quantity', 'daily_transactions', 'revenue_ma_7', 'revenue_ma_30'
            ]
            
            # Remove rows with NaN values
            features_df = features_df.dropna()
            
            if len(features_df) < 10:
                return {"error": "Insufficient data for training"}
            
            X = features_df[feature_columns]
            y = features_df['daily_revenue']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train model
            self.sales_model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.sales_model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.sales_model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            return {
                "success": True,
                "mae": mae,
                "r2_score": r2,
                "feature_importance": dict(zip(feature_columns, self.sales_model.feature_importances_))
            }
            
        except Exception as e:
            return {"error": f"Model training failed: {str(e)}"}
    
    def predict_sales(self, sales_df, forecast_days=30):
        """Predict future sales"""
        if self.sales_model is None:
            train_result = self.train_sales_prediction_model(sales_df)
            if "error" in train_result:
                return train_result
        
        try:
            # Get the latest data point
            features_df = self.prepare_sales_features(sales_df)
            features_df = features_df.sort_values('date')
            
            last_date = features_df['date'].max()
            last_row = features_df[features_df['date'] == last_date].iloc[0]
            
            predictions = []
            current_date = last_date
            
            for i in range(forecast_days):
                current_date += pd.Timedelta(days=1)
                
                # Create features for prediction
                pred_features = {
                    'month': current_date.month,
                    'day_of_week': current_date.dayofweek,
                    'day_of_year': current_date.dayofyear,
                    'quarter': current_date.quarter,
                    'daily_quantity': last_row['daily_quantity'],  # Use last known values
                    'daily_transactions': last_row['daily_transactions'],
                    'revenue_ma_7': last_row['revenue_ma_7'],
                    'revenue_ma_30': last_row['revenue_ma_30']
                }
                
                # Make prediction
                pred_df = pd.DataFrame([pred_features])
                predicted_revenue = self.sales_model.predict(pred_df)[0]
                
                predictions.append({
                    'date': current_date,
                    'predicted_revenue': max(0, predicted_revenue)  # Ensure non-negative
                })
            
            return {"success": True, "predictions": predictions}
            
        except Exception as e:
            return {"error": f"Prediction failed: {str(e)}"}
    
    def detect_anomalies(self, sales_df):
        """Detect anomalies in sales data"""
        try:
            # Prepare daily aggregated data
            daily_sales = sales_df.groupby('date').agg({
                'total_amount': 'sum',
                'quantity': 'sum',
                'sale_id': 'count'
            }).reset_index()
            
            if len(daily_sales) < 10:
                return {"error": "Insufficient data for anomaly detection"}
            
            # Features for anomaly detection
            features = daily_sales[['total_amount', 'quantity', 'sale_id']].values
            
            # Scale features
            features_scaled = self.scaler.fit_transform(features)
            
            # Train anomaly detector
            self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
            anomaly_labels = self.anomaly_detector.fit_predict(features_scaled)
            
            # Get anomaly scores
            anomaly_scores = self.anomaly_detector.score_samples(features_scaled)
            
            # Combine results
            daily_sales['anomaly'] = anomaly_labels == -1
            daily_sales['anomaly_score'] = anomaly_scores
            
            # Get anomalies
            anomalies = daily_sales[daily_sales['anomaly']].copy()
            
            return {
                "success": True,
                "anomalies": anomalies.to_dict('records'),
                "anomaly_count": len(anomalies),
                "total_days": len(daily_sales)
            }
            
        except Exception as e:
            return {"error": f"Anomaly detection failed: {str(e)}"}
    
    def customer_segmentation(self, customers_df, sales_df):
        """Perform customer segmentation analysis"""
        try:
            # Calculate customer metrics
            customer_metrics = sales_df.groupby('customer_id').agg({
                'total_amount': ['sum', 'mean', 'count'],
                'date': ['min', 'max']
            }).reset_index()
            
            customer_metrics.columns = [
                'customer_id', 'total_spent', 'avg_order_value', 
                'order_count', 'first_purchase', 'last_purchase'
            ]
            
            # Calculate recency, frequency, monetary
            current_date = sales_df['date'].max()
            customer_metrics['recency'] = (current_date - customer_metrics['last_purchase']).dt.days
            customer_metrics['frequency'] = customer_metrics['order_count']
            customer_metrics['monetary'] = customer_metrics['total_spent']
            
            # Simple segmentation based on quartiles
            customer_metrics['recency_score'] = pd.qcut(customer_metrics['recency'], 4, labels=[4,3,2,1])
            customer_metrics['frequency_score'] = pd.qcut(customer_metrics['frequency'].rank(method='first'), 4, labels=[1,2,3,4])
            customer_metrics['monetary_score'] = pd.qcut(customer_metrics['monetary'], 4, labels=[1,2,3,4])
            
            # Create RFM score
            customer_metrics['rfm_score'] = (
                customer_metrics['recency_score'].astype(int) + 
                customer_metrics['frequency_score'].astype(int) + 
                customer_metrics['monetary_score'].astype(int)
            )
            
            # Define segments
            def categorize_customer(rfm_score):
                if rfm_score >= 10:
                    return "Champions"
                elif rfm_score >= 8:
                    return "Loyal Customers"
                elif rfm_score >= 6:
                    return "Potential Loyalists"
                elif rfm_score >= 4:
                    return "At Risk"
                else:
                    return "Lost Customers"
            
            customer_metrics['segment'] = customer_metrics['rfm_score'].apply(categorize_customer)
            
            # Merge with customer data
            result = customer_metrics.merge(customers_df, on='customer_id', how='left')
            
            return {
                "success": True,
                "segmentation": result.to_dict('records'),
                "segment_summary": result['segment'].value_counts().to_dict()
            }
            
        except Exception as e:
            return {"error": f"Customer segmentation failed: {str(e)}"}
