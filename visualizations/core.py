"""
Core Visualizations functionality

This module contains the main classes and functions for data visualization.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhatsAppVisualizations:
    """
    Visualization class for WhatsApp Insights Tool
    """
    
    def __init__(self):
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'warning': '#d62728',
            'info': '#9467bd'
        }
        logger.info("WhatsAppVisualizations initialized")
    
    def plot_top_items(self, order_df):
        """
        Plot top selling items by quantity
        
        Args:
            order_df (pandas.DataFrame): Orders dataframe
            
        Returns:
            plotly.graph_objects.Figure: Bar chart figure
        """
        if order_df.empty:
            logger.warning("No data available for top items plot")
            return None
            
        top_items = order_df.groupby('item')['quantity'].sum().sort_values(ascending=False).head(10)
        
        fig = px.bar(
            x=top_items.values,
            y=top_items.index,
            orientation='h',
            title="🏆 Top Selling Items by Quantity",
            labels={'x': 'Total Quantity Sold', 'y': 'Item'},
            color=top_items.values,
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="Quantity Sold",
            yaxis_title="Items"
        )
        
        logger.info(f"Created top items plot with {len(top_items)} items")
        return fig
    
    def plot_sales_trend(self, order_df):
        """
        Plot sales trend over time
        
        Args:
            order_df (pandas.DataFrame): Orders dataframe
            
        Returns:
            plotly.graph_objects.Figure: Line chart figure
        """
        if order_df.empty:
            logger.warning("No data available for sales trend plot")
            return None
            
        daily_sales = order_df.groupby('date')['quantity'].sum().reset_index()
        
        fig = px.line(
            daily_sales,
            x='date',
            y='quantity',
            title="📈 Daily Sales Trend",
            labels={'date': 'Date', 'quantity': 'Total Quantity Sold'},
            markers=True
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Date",
            yaxis_title="Quantity Sold"
        )
        
        logger.info(f"Created sales trend plot with {len(daily_sales)} data points")
        return fig
    
    def plot_customer_activity(self, order_df):
        """
        Plot customer order frequency
        
        Args:
            order_df (pandas.DataFrame): Orders dataframe
            
        Returns:
            plotly.graph_objects.Figure: Scatter plot figure
        """
        if order_df.empty:
            logger.warning("No data available for customer activity plot")
            return None
            
        customer_orders = order_df.groupby('customer').agg({
            'date': 'count',
            'quantity': 'sum'
        }).reset_index()
        customer_orders.columns = ['customer', 'order_count', 'total_quantity']
        
        fig = px.scatter(
            customer_orders,
            x='order_count',
            y='total_quantity',
            size='total_quantity',
            color='order_count',
            hover_data=['customer'],
            title="👥 Customer Activity Analysis",
            labels={
                'order_count': 'Number of Orders',
                'total_quantity': 'Total Quantity Ordered',
                'customer': 'Customer Name'
            }
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Number of Orders",
            yaxis_title="Total Quantity Ordered"
        )
        
        logger.info(f"Created customer activity plot with {len(customer_orders)} customers")
        return fig
    
    def plot_item_heatmap(self, order_df):
        """
        Plot item sales heatmap by day of week
        
        Args:
            order_df (pandas.DataFrame): Orders dataframe
            
        Returns:
            plotly.graph_objects.Figure: Heatmap figure
        """
        if order_df.empty:
            logger.warning("No data available for item heatmap")
            return None
            
        # Add day of week
        order_df['day_of_week'] = order_df['date'].dt.day_name()
        order_df['week'] = order_df['date'].dt.isocalendar().week
        
        # Create pivot table
        heatmap_data = order_df.groupby(['day_of_week', 'week'])['quantity'].sum().unstack(fill_value=0)
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data.reindex(day_order)
        
        fig = px.imshow(
            heatmap_data,
            title="🔥 Item Sales Heatmap (by Day of Week)",
            labels={'x': 'Week', 'y': 'Day of Week'},
            color_continuous_scale='YlOrRd'
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Week",
            yaxis_title="Day of Week"
        )
        
        logger.info("Created item heatmap plot")
        return fig
    
    def plot_revenue_analysis(self, order_df, zelle_df):
        """
        Plot revenue analysis combining orders and payments
        
        Args:
            order_df (pandas.DataFrame): Orders dataframe
            zelle_df (pandas.DataFrame): Zelle transactions dataframe
            
        Returns:
            plotly.graph_objects.Figure: Subplot figure
        """
        if order_df.empty or zelle_df.empty:
            logger.warning("Insufficient data for revenue analysis plot")
            return None
            
        # Group orders by date
        daily_orders = order_df.groupby('date')['quantity'].sum().reset_index()
        daily_orders.columns = ['date', 'total_quantity']
        
        # Group payments by date
        daily_payments = zelle_df.groupby('date')['amount'].sum().reset_index()
        daily_payments.columns = ['date', 'total_amount']
        
        # Merge data
        revenue_data = pd.merge(daily_orders, daily_payments, on='date', how='outer').fillna(0)
        
        # Create subplot
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('📊 Daily Orders', '💰 Daily Revenue'),
            vertical_spacing=0.1
        )
        
        # Orders subplot
        fig.add_trace(
            go.Bar(x=revenue_data['date'], y=revenue_data['total_quantity'], name='Orders'),
            row=1, col=1
        )
        
        # Revenue subplot
        fig.add_trace(
            go.Scatter(x=revenue_data['date'], y=revenue_data['total_amount'], name='Revenue', mode='lines+markers'),
            row=2, col=1
        )
        
        fig.update_layout(
            height=600,
            title_text="📈 Revenue Analysis",
            showlegend=False
        )
        
        logger.info("Created revenue analysis plot")
        return fig
    
    def plot_customer_retention(self, order_df):
        """
        Plot customer retention analysis
        
        Args:
            order_df (pandas.DataFrame): Orders dataframe
            
        Returns:
            plotly.graph_objects.Figure: Pie chart figure
        """
        if order_df.empty:
            logger.warning("No data available for customer retention plot")
            return None
            
        # Calculate customer metrics
        now = order_df['date'].max()
        customer_orders = order_df.groupby('customer')['date'].agg(['min', 'max', 'count']).reset_index()
        customer_orders['days_since_last_order'] = (now - customer_orders['max']).dt.days
        customer_orders['customer_lifetime'] = (customer_orders['max'] - customer_orders['min']).dt.days
        
        # Categorize customers
        def categorize_customer(row):
            if row['days_since_last_order'] <= 7:
                return 'Active (7 days)'
            elif row['days_since_last_order'] <= 14:
                return 'Active (14 days)'
            elif row['days_since_last_order'] <= 30:
                return 'At Risk'
            else:
                return 'Churned'
        
        customer_orders['status'] = customer_orders.apply(categorize_customer, axis=1)
        
        # Create pie chart
        status_counts = customer_orders['status'].value_counts()
        
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="👥 Customer Retention Status",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_layout(height=400)
        
        logger.info(f"Created customer retention plot with {len(status_counts)} categories")
        return fig
    
    def plot_item_trends(self, order_df):
        """
        Plot trending items over time
        
        Args:
            order_df (pandas.DataFrame): Orders dataframe
            
        Returns:
            plotly.graph_objects.Figure: Line chart figure
        """
        if order_df.empty:
            logger.warning("No data available for item trends plot")
            return None
            
        # Group by item and week
        order_df['week'] = order_df['date'].dt.to_period('W')
        item_trends = order_df.groupby(['item', 'week'])['quantity'].sum().unstack(fill_value=0)
        
        # Get top 5 items
        top_items = order_df.groupby('item')['quantity'].sum().sort_values(ascending=False).head(5).index
        
        # Filter for top items
        item_trends_filtered = item_trends.loc[top_items]
        
        # Create line plot
        fig = go.Figure()
        
        for item in top_items:
            if item in item_trends_filtered.index:
                fig.add_trace(
                    go.Scatter(
                        x=item_trends_filtered.columns.astype(str),
                        y=item_trends_filtered.loc[item],
                        mode='lines+markers',
                        name=item
                    )
                )
        
        fig.update_layout(
            title="📈 Top Items Trend Over Time",
            xaxis_title="Week",
            yaxis_title="Quantity Sold",
            height=400
        )
        
        logger.info(f"Created item trends plot with {len(top_items)} items")
        return fig
    
    def create_dashboard_summary(self, order_df, zelle_df, insights):
        """
        Create a summary dashboard with key metrics
        
        Args:
            order_df (pandas.DataFrame): Orders dataframe
            zelle_df (pandas.DataFrame): Zelle transactions dataframe
            insights (dict): Insights dictionary
        """
        if order_df.empty:
            logger.warning("No data available for dashboard summary")
            return None
            
        # Calculate key metrics
        total_orders = len(order_df)
        total_customers = order_df['customer'].nunique()
        total_items = order_df['item'].nunique()
        total_quantity = order_df['quantity'].sum()
        
        # Revenue metrics
        total_revenue = zelle_df['amount'].sum() if not zelle_df.empty else 0
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Create metrics display
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📦 Total Orders", total_orders)
        
        with col2:
            st.metric("👥 Unique Customers", total_customers)
        
        with col3:
            st.metric("💰 Total Revenue", f"${total_revenue:.2f}")
        
        with col4:
            st.metric("📊 Avg Order Value", f"${avg_order_value:.2f}")
        
        # Additional metrics
        col5, col6, col7, col8 = st.columns(4)
        
        with col5:
            st.metric("🍽️ Items Sold", total_quantity)
        
        with col6:
            st.metric("🏷️ Unique Items", total_items)
        
        with col7:
            avg_orders_per_customer = total_orders / total_customers if total_customers > 0 else 0
            st.metric("📈 Avg Orders/Customer", f"{avg_orders_per_customer:.1f}")
        
        with col8:
            retention_rate = len(insights.get('retained_customers', [])) / total_customers * 100 if total_customers > 0 else 0
            st.metric("🔄 Retention Rate", f"{retention_rate:.1f}%")
        
        logger.info("Created dashboard summary with key metrics")

def create_visualizations(order_df, zelle_df, insights):
    """
    Main function to create all visualizations
    
    Args:
        order_df (pandas.DataFrame): Orders dataframe
        zelle_df (pandas.DataFrame): Zelle transactions dataframe
        insights (dict): Insights dictionary
    """
    logger.info("Starting visualization creation")
    
    viz = WhatsAppVisualizations()
    
    # Create summary dashboard
    viz.create_dashboard_summary(order_df, zelle_df, insights)
    
    # Create visualizations
    st.subheader("📊 Data Visualizations")
    
    # Top items chart
    if not order_df.empty:
        fig1 = viz.plot_top_items(order_df)
        if fig1:
            st.plotly_chart(fig1, use_container_width=True)
    
    # Sales trend
    if not order_df.empty:
        fig2 = viz.plot_sales_trend(order_df)
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)
    
    # Customer activity
    if not order_df.empty:
        fig3 = viz.plot_customer_activity(order_df)
        if fig3:
            st.plotly_chart(fig3, use_container_width=True)
    
    # Revenue analysis
    if not order_df.empty and not zelle_df.empty:
        fig4 = viz.plot_revenue_analysis(order_df, zelle_df)
        if fig4:
            st.plotly_chart(fig4, use_container_width=True)
    
    # Customer retention
    if not order_df.empty:
        fig5 = viz.plot_customer_retention(order_df)
        if fig5:
            st.plotly_chart(fig5, use_container_width=True)
    
    # Item trends
    if not order_df.empty:
        fig6 = viz.plot_item_trends(order_df)
        if fig6:
            st.plotly_chart(fig6, use_container_width=True)
    
    # Item heatmap
    if not order_df.empty:
        fig7 = viz.plot_item_heatmap(order_df)
        if fig7:
            st.plotly_chart(fig7, use_container_width=True)
    
    logger.info("Completed visualization creation") 