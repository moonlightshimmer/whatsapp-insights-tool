#!/usr/bin/env python3
"""
Test script for WhatsApp Insights Tool Visualizations
"""

import pandas as pd
from datetime import datetime, timedelta
import sys
import os

def create_sample_data():
    """Create sample data for testing visualizations"""
    
    # Sample order data
    orders_data = [
        {"date": "2024-06-27", "customer": "John Doe", "item": "Biryani", "quantity": 2},
        {"date": "2024-06-27", "customer": "John Doe", "item": "Naan", "quantity": 1},
        {"date": "2024-06-27", "customer": "Alice Smith", "item": "Curry", "quantity": 1},
        {"date": "2024-06-27", "customer": "Alice Smith", "item": "Rice", "quantity": 2},
        {"date": "2024-06-27", "customer": "Alice Smith", "item": "Salad", "quantity": 1},
        {"date": "2024-06-28", "customer": "Bob Johnson", "item": "Biryani", "quantity": 3},
        {"date": "2024-06-28", "customer": "Bob Johnson", "item": "Naan", "quantity": 2},
        {"date": "2024-07-01", "customer": "John Doe", "item": "Curry", "quantity": 1},
        {"date": "2024-07-01", "customer": "John Doe", "item": "Rice", "quantity": 1},
        {"date": "2024-07-15", "customer": "Alice Smith", "item": "Biryani", "quantity": 2},
        {"date": "2024-07-15", "customer": "Alice Smith", "item": "Naan", "quantity": 1},
        {"date": "2024-07-15", "customer": "Alice Smith", "item": "Salad", "quantity": 1},
    ]
    
    # Sample Zelle data
    zelle_data = [
        {"date": "2024-06-27", "description": "John Doe - Biryani Order", "amount": 25.00},
        {"date": "2024-06-27", "description": "Alice Smith - Curry Order", "amount": 15.00},
        {"date": "2024-06-28", "description": "Bob Johnson - Biryani Order", "amount": 30.00},
        {"date": "2024-07-01", "description": "John Doe - Curry Order", "amount": 10.00},
        {"date": "2024-07-15", "description": "Alice Smith - Biryani Order", "amount": 25.00},
    ]
    
    # Create DataFrames
    orders_df = pd.DataFrame(orders_data)
    orders_df['date'] = pd.to_datetime(orders_df['date'])
    
    zelle_df = pd.DataFrame(zelle_data)
    zelle_df['date'] = pd.to_datetime(zelle_df['date'])
    
    return orders_df, zelle_df

def test_visualization_imports():
    """Test if visualization libraries can be imported"""
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        import numpy as np
        print("✅ All visualization libraries imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Error importing visualization libraries: {e}")
        print("💡 Run: pip install plotly numpy")
        return False

def test_visualization_module():
    """Test the visualization module"""
    try:
        from visualizations import WhatsAppVisualizations
        print("✅ Visualization module imported successfully")
        
        # Create sample data
        orders_df, zelle_df = create_sample_data()
        
        # Test visualization class
        viz = WhatsAppVisualizations()
        
        # Test top items plot
        fig1 = viz.plot_top_items(orders_df)
        if fig1:
            print("✅ Top items visualization created")
        
        # Test sales trend plot
        fig2 = viz.plot_sales_trend(orders_df)
        if fig2:
            print("✅ Sales trend visualization created")
        
        # Test customer activity plot
        fig3 = viz.plot_customer_activity(orders_df)
        if fig3:
            print("✅ Customer activity visualization created")
        
        print("🎉 All visualization tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing visualization module: {e}")
        return False

def main():
    print("🧪 Testing WhatsApp Insights Tool Visualizations")
    print("=" * 50)
    
    # Test imports
    if not test_visualization_imports():
        return
    
    # Test visualization module
    if not test_visualization_module():
        return
    
    print("\n🚀 Ready to run visualizations!")
    print("Run: streamlit run data_ingestion.py")
    print("Upload sample data to see the charts in action!")

if __name__ == "__main__":
    main() 