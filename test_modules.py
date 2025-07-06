#!/usr/bin/env python3
"""
Test script for WhatsApp Insights Tool Modules

This script tests the new module structure for both WhatsApp integration
and visualizations modules.
"""

import sys
import os

def test_module_imports():
    """Test if the new modules can be imported correctly"""
    print("🧪 Testing Module Imports")
    print("=" * 40)
    
    # Test WhatsApp Integration Module
    print("\n📱 Testing WhatsApp Integration Module:")
    try:
        from whatsapp_integration import integrate_whatsapp_export, show_whatsapp_export_instructions
        print("✅ WhatsApp integration module imported successfully")
        
        # Test the class
        from whatsapp_integration.core import WhatsAppIntegration
        integration = WhatsAppIntegration()
        print("✅ WhatsAppIntegration class instantiated successfully")
        
    except ImportError as e:
        print(f"❌ WhatsApp integration module import failed: {e}")
        return False
    
    # Test Visualizations Module
    print("\n📊 Testing Visualizations Module:")
    try:
        from visualizations import create_visualizations
        print("✅ Visualizations module imported successfully")
        
        # Test the class
        from visualizations.core import WhatsAppVisualizations
        viz = WhatsAppVisualizations()
        print("✅ WhatsAppVisualizations class instantiated successfully")
        
    except ImportError as e:
        print(f"❌ Visualizations module import failed: {e}")
        return False
    
    return True

def test_module_structure():
    """Test the module file structure"""
    print("\n📁 Testing Module Structure:")
    print("=" * 40)
    
    required_files = [
        "whatsapp_integration/__init__.py",
        "whatsapp_integration/core.py",
        "visualizations/__init__.py",
        "visualizations/core.py"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    return True

def test_module_functionality():
    """Test basic functionality of the modules"""
    print("\n🔧 Testing Module Functionality:")
    print("=" * 40)
    
    try:
        # Test WhatsApp integration
        from whatsapp_integration.core import WhatsAppIntegration
        integration = WhatsAppIntegration()
        
        # Test with sample data
        sample_text = "Order: 2 Biryani, 1 Naan | Name: John Doe | Date: 2024-06-27"
        orders = integration.extract_orders_from_text(sample_text)
        
        if orders:
            print(f"✅ WhatsApp integration extracted {len(orders)} orders")
        else:
            print("❌ WhatsApp integration failed to extract orders")
            return False
        
        # Test visualizations
        from visualizations.core import WhatsAppVisualizations
        viz = WhatsAppVisualizations()
        print("✅ Visualizations class created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Module functionality test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 WhatsApp Insights Tool - Module Testing")
    print("=" * 50)
    
    # Test module structure
    if not test_module_structure():
        print("\n❌ Module structure test failed")
        return
    
    # Test module imports
    if not test_module_imports():
        print("\n❌ Module import test failed")
        return
    
    # Test module functionality
    if not test_module_functionality():
        print("\n❌ Module functionality test failed")
        return
    
    print("\n🎉 All module tests passed!")
    print("\n📋 Module Structure Summary:")
    print("├── whatsapp_integration/")
    print("│   ├── __init__.py")
    print("│   └── core.py")
    print("├── visualizations/")
    print("│   ├── __init__.py")
    print("│   └── core.py")
    print("└── data_ingestion.py (main app)")
    
    print("\n🚀 Ready to deploy to Streamlit Cloud!")

if __name__ == "__main__":
    main() 