#!/usr/bin/env python3
"""
Test script for WhatsApp Insights Tool
This script helps you test the application with sample data
"""

import subprocess
import sys
import os

def main():
    print("🧪 WhatsApp Insights Tool - Test Setup")
    print("=" * 50)
    
    # Check if sample files exist
    whatsapp_file = "sample_whatsapp_messages.txt"
    zelle_file = "sample_zelle_comprehensive.csv"
    
    if not os.path.exists(whatsapp_file):
        print(f"❌ {whatsapp_file} not found!")
        return
    
    if not os.path.exists(zelle_file):
        print(f"❌ {zelle_file} not found!")
        return
    
    print("✅ Sample files found!")
    print(f"📱 WhatsApp messages: {whatsapp_file}")
    print(f"💰 Zelle transactions: {zelle_file}")
    
    print("\n📋 How to test the application:")
    print("1. Run: streamlit run data_ingestion.py")
    print("2. Open the web browser to the URL shown")
    print("3. Upload the Zelle CSV file: sample_zelle_comprehensive.csv")
    print("4. Copy and paste the contents of sample_whatsapp_messages.txt")
    print("5. View the generated insights!")
    
    print("\n📊 Expected insights from this sample data:")
    print("- Trending items: Biryani (increasing demand)")
    print("- Top items: Biryani, Curry, Rice, Naan, Salad")
    print("- Customer retention: John Doe and Alice Smith (frequent customers)")
    print("- Reorder patterns: Multiple reorders from loyal customers")
    
    print("\n🚀 Ready to test? Run: streamlit run data_ingestion.py")

if __name__ == "__main__":
    main() 