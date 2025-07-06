"""
WhatsApp Integration Module for WhatsApp Insights Tool

This module provides functionality to integrate with WhatsApp data,
including parsing exported chat files and extracting order information.
"""

from .core import WhatsAppIntegration, integrate_whatsapp_export, show_whatsapp_export_instructions

__version__ = "1.0.0"
__author__ = "WhatsApp Insights Tool"
__all__ = [
    "WhatsAppIntegration",
    "integrate_whatsapp_export", 
    "show_whatsapp_export_instructions"
] 