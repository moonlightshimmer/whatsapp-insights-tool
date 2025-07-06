import streamlit as st
import pandas as pd
import re
from datetime import datetime, timedelta
from whatsapp_integration import integrate_whatsapp_export, show_whatsapp_export_instructions
from visualizations import create_visualizations

WHATSAPP_INTEGRATION_AVAILABLE = True
VISUALIZATIONS_AVAILABLE = True

def parse_whatsapp_messages(messages):
    order_data = []
    for msg in messages:
        match = re.search(r"Order:\s*(.*)\s*\|\s*Name:\s*(.*?)\s*\|\s*Date:\s*(.*?)$", msg)
        if match:
            items_raw = match.group(1).split(',')
            name = match.group(2)
            date = datetime.strptime(match.group(3), "%Y-%m-%d")
            for item in items_raw:
                qty_item = item.strip().split(' ', 1)
                qty = int(qty_item[0])
                item_name = qty_item[1].strip()
                order_data.append({"date": date, "customer": name, "item": item_name, "quantity": qty})
    return pd.DataFrame(order_data)

def read_zelle_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df.columns = [col.lower().strip().replace(' ', '_') for col in df.columns]
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df[['date', 'description', 'amount']]

def generate_insights(order_df):
    insights = {}
    order_df['week'] = order_df['date'].dt.to_period('W')
    item_trends = order_df.groupby(['item', 'week'])['quantity'].sum().unstack(fill_value=0)
    increasing_items = []
    for item in item_trends.index:
        trend = item_trends.loc[item].tail(3).values
        if len(trend) == 3 and trend[2] > trend[1] > trend[0]:
            increasing_items.append((item, trend.tolist()))
    insights['increasing_items'] = increasing_items
    top_items = order_df.groupby('item')['quantity'].sum().sort_values(ascending=False).head(5)
    insights['top_items'] = top_items.to_dict()
    stock_threshold = 10
    current_stock = {item: 8 for item in top_items.index}
    low_stock_items = {item: qty for item, qty in current_stock.items() if qty < stock_threshold}
    insights['low_stock'] = low_stock_items
    now = order_df['date'].max()
    customer_orders = order_df.groupby('customer')['date'].agg(['min', 'max', 'count'])
    customer_orders['days_since_last_order'] = (now - customer_orders['max']).dt.days
    retained = customer_orders[customer_orders['days_since_last_order'] <= 14]
    churned = customer_orders[customer_orders['days_since_last_order'] > 14]
    churn_types = {}
    for customer, row in churned.iterrows():
        lifetime = (row['max'] - row['min']).days
        if row['count'] == 1:
            churn_types[customer] = 'Trial'
        elif lifetime < 7:
            churn_types[customer] = 'Quick Churn'
        else:
            churn_types[customer] = 'Slow Churn'
    insights['retained_customers'] = retained.index.tolist()
    insights['churned_customers'] = churn_types
    reorder_counts = order_df.groupby(['customer', 'item']).size().reset_index(name='order_count')
    reordered_items = reorder_counts[reorder_counts['order_count'] > 1]
    insights['reordered_items'] = reordered_items.to_dict(orient='records')
    return insights

st.title("Tiffin Service Insights Dashboard")

# WhatsApp Integration (with fallback)
if WHATSAPP_INTEGRATION_AVAILABLE:
    # Show WhatsApp export instructions
    show_whatsapp_export_instructions()
    
    # WhatsApp Integration
    whatsapp_df = integrate_whatsapp_export()
else:
    # Fallback to original method
    st.subheader("📱 WhatsApp Order Messages")
    whatsapp_input = st.text_area("Paste WhatsApp Order Messages (one per line)")
    whatsapp_df = None
    if whatsapp_input:
        whatsapp_lines = whatsapp_input.strip().split('\n')
        whatsapp_df = parse_whatsapp_messages(whatsapp_lines)

uploaded_zelle = st.file_uploader("Upload Zelle Transactions CSV", type="csv")

if uploaded_zelle and whatsapp_df is not None:
    zelle_df = read_zelle_csv(uploaded_zelle)

    st.subheader("Parsed Orders")
    st.dataframe(whatsapp_df)

    insights = generate_insights(whatsapp_df)

    # Create visualizations
    if VISUALIZATIONS_AVAILABLE:
        create_visualizations(whatsapp_df, zelle_df, insights)
    else:
        st.warning("⚠️ Visualizations are not available in this environment")
    
    # Text insights
    st.subheader("📋 Detailed Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📈 Increasing Items:**")
        for item, trend in insights['increasing_items']:
            st.write(f"- {item}: {trend}")
        
        st.write("**🏆 Top Items:**")
        for item, qty in insights['top_items'].items():
            st.write(f"- {item}: {qty} units")
        
        st.write("**⚠️ Low Stock Items:**")
        for item, qty in insights['low_stock'].items():
            st.write(f"- {item}: {qty} units remaining")
    
    with col2:
        st.write("**👥 Retained Customers:**")
        for customer in insights['retained_customers']:
            st.write(f"- {customer}")
        
        st.write("**❌ Churned Customers:**")
        for customer, churn_type in insights['churned_customers'].items():
            st.write(f"- {customer} ({churn_type})")
        
        st.write("**🔄 Reordered Items:**")
        for record in insights['reordered_items']:
            st.write(f"- {record['customer']}: {record['item']} ({record['order_count']} times)")
else:
    st.info("Please upload both WhatsApp order messages and Zelle transaction file to see insights.")
