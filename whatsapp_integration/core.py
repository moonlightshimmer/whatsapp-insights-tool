"""
Core WhatsApp Integration functionality

This module contains the main classes and functions for WhatsApp integration.
"""

import re
import pandas as pd
from datetime import datetime
import streamlit as st
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhatsAppIntegration:
    """
    WhatsApp Integration for automatic order extraction from exported chat files
    """
    
    def __init__(self):
        self.order_pattern = r"Order:\s*(.*?)\s*\|\s*Name:\s*(.*?)\s*\|\s*Date:\s*(.*?)$"
        self.date_patterns = [
            r"(\d{1,2}/\d{1,2}/\d{2,4})",  # MM/DD/YY or MM/DD/YYYY
            r"(\d{1,2}-\d{1,2}-\d{2,4})",  # MM-DD-YY or MM-DD-YYYY
            r"(\d{4}-\d{1,2}-\d{1,2})",    # YYYY-MM-DD
        ]
        logger.info("WhatsAppIntegration initialized")
    
    def parse_exported_chat(self, chat_file):
        """
        Parse exported WhatsApp chat file and extract order messages
        
        Args:
            chat_file (str): Path to the exported chat file
            
        Returns:
            list: List of order dictionaries
        """
        orders = []
        
        try:
            with open(chat_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            logger.info(f"Processing {len(lines)} lines from chat file")
            
            for line in lines:
                # Look for order messages
                match = re.search(self.order_pattern, line, re.IGNORECASE)
                if match:
                    items_raw = match.group(1).strip()
                    name = match.group(2).strip()
                    date_str = match.group(3).strip()
                    
                    # Parse date
                    date = self.parse_date(date_str)
                    if date:
                        # Parse items
                        items = self.parse_items(items_raw)
                        for item, qty in items:
                            orders.append({
                                "date": date,
                                "customer": name,
                                "item": item,
                                "quantity": qty,
                                "raw_message": line.strip()
                            })
        
        except Exception as e:
            logger.error(f"Error parsing chat file: {str(e)}")
            st.error(f"Error parsing chat file: {str(e)}")
            return []
        
        logger.info(f"Extracted {len(orders)} orders from chat file")
        return orders
    
    def parse_date(self, date_str):
        """
        Parse various date formats from WhatsApp messages
        
        Args:
            date_str (str): Date string to parse
            
        Returns:
            datetime: Parsed date or None if parsing fails
        """
        for pattern in self.date_patterns:
            match = re.search(pattern, date_str)
            if match:
                date_part = match.group(1)
                try:
                    # Try different date formats
                    for fmt in ["%m/%d/%y", "%m/%d/%Y", "%m-%d-%y", "%m-%d-%Y", "%Y-%m-%d"]:
                        try:
                            return datetime.strptime(date_part, fmt)
                        except ValueError:
                            continue
                except:
                    continue
        return None
    
    def parse_items(self, items_raw):
        """
        Parse order items and quantities
        
        Args:
            items_raw (str): Raw items string
            
        Returns:
            list: List of (item_name, quantity) tuples
        """
        items = []
        item_parts = [part.strip() for part in items_raw.split(',')]
        
        for part in item_parts:
            # Look for quantity and item name
            # Pattern: "2 Biryani" or "1 Naan"
            match = re.match(r"(\d+)\s+(.+)", part)
            if match:
                qty = int(match.group(1))
                item_name = match.group(2).strip()
                items.append((item_name, qty))
        
        return items
    
    def extract_orders_from_text(self, text):
        """
        Extract orders from pasted text (current functionality)
        
        Args:
            text (str): Pasted text containing order messages
            
        Returns:
            list: List of order dictionaries
        """
        orders = []
        lines = text.strip().split('\n')
        
        logger.info(f"Processing {len(lines)} lines from pasted text")
        
        for line in lines:
            match = re.search(self.order_pattern, line, re.IGNORECASE)
            if match:
                items_raw = match.group(1).strip()
                name = match.group(2).strip()
                date_str = match.group(3).strip()
                
                date = self.parse_date(date_str)
                if date:
                    items = self.parse_items(items_raw)
                    for item, qty in items:
                        orders.append({
                            "date": date,
                            "customer": name,
                            "item": item,
                            "quantity": qty,
                            "raw_message": line.strip()
                        })
        
        logger.info(f"Extracted {len(orders)} orders from pasted text")
        return orders

def integrate_whatsapp_export():
    """
    Streamlit interface for WhatsApp export integration
    
    Returns:
        pandas.DataFrame: DataFrame containing extracted orders or None
    """
    st.subheader("📱 WhatsApp Export Integration")
    
    integration = WhatsAppIntegration()
    
    # Option 1: Upload exported chat file
    st.write("**Option 1: Upload Exported WhatsApp Chat**")
    uploaded_chat = st.file_uploader(
        "Upload exported WhatsApp chat file (.txt)",
        type=['txt'],
        help="Export your WhatsApp chat and upload the .txt file"
    )
    
    orders_from_file = []
    if uploaded_chat:
        # Save uploaded file temporarily
        with open("temp_chat.txt", "w", encoding="utf-8") as f:
            f.write(uploaded_chat.getvalue().decode("utf-8"))
        
        orders_from_file = integration.parse_exported_chat("temp_chat.txt")
        
        if orders_from_file:
            st.success(f"✅ Extracted {len(orders_from_file)} orders from chat file")
            st.write("**Sample extracted orders:**")
            sample_df = pd.DataFrame(orders_from_file[:5])
            st.dataframe(sample_df[['date', 'customer', 'item', 'quantity']])
        else:
            st.warning("⚠️ No order messages found in the chat file")
    
    # Option 2: Paste messages (existing functionality)
    st.write("**Option 2: Paste WhatsApp Messages**")
    whatsapp_input = st.text_area(
        "Paste WhatsApp Order Messages (one per line)",
        help="Copy and paste your WhatsApp order messages here"
    )
    
    orders_from_text = []
    if whatsapp_input:
        orders_from_text = integration.extract_orders_from_text(whatsapp_input)
        
        if orders_from_text:
            st.success(f"✅ Extracted {len(orders_from_text)} orders from pasted text")
    
    # Combine orders from both sources
    all_orders = orders_from_file + orders_from_text
    
    if all_orders:
        st.write("**📊 Combined Orders Summary**")
        orders_df = pd.DataFrame(all_orders)
        st.dataframe(orders_df[['date', 'customer', 'item', 'quantity']])
        
        return orders_df
    
    return None

def show_whatsapp_export_instructions():
    """
    Show instructions for exporting WhatsApp chats
    """
    with st.expander("📋 How to Export WhatsApp Chat"):
        st.write("""
        **To export your WhatsApp chat:**
        
        1. **Open WhatsApp** on your phone
        2. **Go to the chat** you want to export
        3. **Tap the three dots** (menu) in the top right
        4. **Select 'More'** → **'Export chat'**
        5. **Choose 'Without Media'** (faster, smaller file)
        6. **Share the file** to your computer (email, cloud storage, etc.)
        7. **Upload the .txt file** in the app above
        
        **Note:** The chat export will include all messages. The app will automatically 
        extract only the order messages that match the expected format.
        """) 