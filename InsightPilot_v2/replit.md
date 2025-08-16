# AI-Powered Business Insights Assistant

## Overview

This is a comprehensive business intelligence application built with Streamlit that transforms business data into actionable insights using AI and machine learning. The application provides an interactive dashboard for analyzing sales, customer, and product data with features including natural language querying, predictive analytics, anomaly detection, and AI-powered recommendations.

The system is designed as a modular analytics platform that can process business data and generate strategic insights through multiple specialized interfaces. It combines traditional business intelligence with modern AI capabilities to help users make data-driven decisions.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit-based web application with a multi-page component structure
- **Layout**: Wide layout with expandable sidebar navigation
- **State Management**: Session state for data persistence and loading optimization
- **Visualization**: Plotly for interactive charts and graphs
- **Component Structure**: Modular components for dashboard, NLP interface, predictions, anomaly detection, and recommendations

### Backend Architecture
- **Service Layer Pattern**: Separated business logic into dedicated service classes
  - `AIService`: Handles OpenAI API interactions for natural language processing
  - `MLService`: Manages machine learning models for predictions and anomaly detection
  - `AnalyticsService`: Processes business metrics and KPI calculations
- **Data Processing**: Centralized `DataProcessor` utility for data transformations and filtering
- **Sample Data Generation**: Synthetic business data generator for demonstration purposes

### Data Architecture
- **In-Memory Processing**: Uses pandas DataFrames for data manipulation and analysis
- **Data Structure**: Relational-style data with separate entities for sales, customers, and products
- **Time Series Support**: Built-in support for temporal analysis and forecasting
- **No Persistent Storage**: Currently operates on generated sample data without database integration

### Machine Learning Components
- **Scikit-learn Integration**: Random Forest and Linear Regression for predictions
- **Anomaly Detection**: Isolation Forest algorithm for outlier identification
- **Feature Engineering**: Automated time-based feature creation for forecasting
- **Model Training**: On-demand model training with real-time predictions

### AI Integration
- **OpenAI GPT-4o**: Latest model for natural language understanding and business insights
- **Structured Responses**: JSON-formatted AI responses for consistent data handling
- **Context-Aware Analysis**: AI receives comprehensive business data summaries for informed recommendations
- **Fallback Handling**: Graceful degradation when AI services are unavailable

## External Dependencies

### AI Services
- **OpenAI API**: GPT-4o model for natural language processing and business insights generation
- **Authentication**: Environment variable-based API key configuration (`OPENAI_API_KEY`)

### Python Libraries
- **Streamlit**: Web application framework and UI components
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing and statistical operations
- **Plotly**: Interactive data visualization (Express and Graph Objects)
- **Scikit-learn**: Machine learning algorithms and preprocessing tools

### Development Tools
- **Environment Configuration**: OS environment variables for API key management
- **Error Handling**: Comprehensive exception handling with user-friendly error messages
- **Performance Optimization**: Data caching through session state management