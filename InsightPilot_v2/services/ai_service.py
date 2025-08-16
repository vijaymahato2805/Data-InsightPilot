import os
import json
import pandas as pd
from openai import OpenAI

class AIService:
    """Service for handling OpenAI interactions"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def is_available(self):
        """Check if OpenAI service is available"""
        return self.client is not None
    
    def process_natural_language_query(self, query, data_summary):
        """
        Process natural language query and convert to actionable insights
        """
        if not self.is_available():
            return {"error": "OpenAI API key not configured"}
        
        try:
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a business analytics AI assistant. 
                        Analyze the user's query and data summary to provide actionable insights.
                        Respond with JSON containing: analysis, key_findings (array), recommendations (array), and suggested_actions (array).
                        Focus on specific, actionable insights based on the data provided."""
                    },
                    {
                        "role": "user", 
                        "content": f"Query: {query}\n\nData Summary: {data_summary}\n\nProvide insights in JSON format."
                    }
                ],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            return {"error": f"Failed to process query: {str(e)}"}
    
    def generate_business_insights(self, metrics_data):
        """
        Generate AI-powered business insights from metrics
        """
        if not self.is_available():
            return {"error": "OpenAI API key not configured"}
        
        try:
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a senior business analyst. Analyze the provided business metrics 
                        and generate strategic insights. Respond with JSON containing: 
                        overall_health (1-5 rating), key_insights (array), growth_opportunities (array), 
                        risk_factors (array), and strategic_recommendations (array)."""
                    },
                    {
                        "role": "user",
                        "content": f"Business Metrics: {json.dumps(metrics_data)}\n\nProvide strategic analysis in JSON format."
                    }
                ],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            return {"error": f"Failed to generate insights: {str(e)}"}
    
    def analyze_anomaly_causes(self, anomaly_data):
        """
        Analyze potential causes of detected anomalies
        """
        if not self.is_available():
            return {"error": "OpenAI API key not configured"}
        
        try:
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a data anomaly expert. Analyze the anomaly data and suggest 
                        potential causes and recommended actions. Respond with JSON containing: 
                        severity (1-5), potential_causes (array), impact_assessment (string), 
                        recommended_actions (array)."""
                    },
                    {
                        "role": "user",
                        "content": f"Anomaly Data: {json.dumps(anomaly_data)}\n\nAnalyze causes and suggest actions in JSON format."
                    }
                ],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            return {"error": f"Failed to analyze anomaly: {str(e)}"}
    
    def generate_recommendations(self, business_context):
        """
        Generate smart business recommendations based on context
        """
        if not self.is_available():
            return {"error": "OpenAI API key not configured"}
        
        try:
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a strategic business consultant. Based on the business context,
                        generate actionable recommendations with priority levels and expected outcomes.
                        Respond with JSON containing: recommendations array with fields: title, description, 
                        priority (High/Medium/Low), expected_impact, implementation_steps (array), timeline."""
                    },
                    {
                        "role": "user",
                        "content": f"Business Context: {json.dumps(business_context)}\n\nGenerate strategic recommendations in JSON format."
                    }
                ],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            return {"error": f"Failed to generate recommendations: {str(e)}"}
