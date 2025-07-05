# WhatsApp Insights Tool

A Streamlit web application that analyzes WhatsApp order messages and Zelle payment transactions to generate business insights for small businesses, particularly food services like tiffin businesses.

## 🎯 What It Does

This tool helps small businesses transform their WhatsApp conversations and payment data into actionable business intelligence by:

- **Parsing WhatsApp Messages**: Extracts order details from structured WhatsApp messages
- **Processing Zelle Transactions**: Analyzes payment data from CSV exports
- **Generating Business Insights**: Provides trends, customer analysis, and inventory recommendations

## 🚀 Features

### 📊 Business Intelligence
- **Trending Analysis**: Identifies items with increasing demand
- **Top Performers**: Shows best-selling items by quantity
- **Inventory Alerts**: Flags low stock items
- **Customer Retention**: Analyzes customer loyalty and churn patterns
- **Reorder Patterns**: Tracks customer reorder behavior

### 💻 User Interface
- Clean Streamlit dashboard
- File upload for Zelle CSV data
- Text area for WhatsApp messages
- Interactive data tables and insights display

## 📋 Prerequisites

- Python 3.7+
- pip (Python package installer)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/moonlightshimmer/whatsapp-insights-tool.git
   cd whatsapp-insights-tool
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run data_ingestion.py
   ```

## 📖 Usage

### 1. Prepare Your Data

#### WhatsApp Messages Format
Your WhatsApp messages should follow this format:
```
Order: 2 Biryani, 1 Naan | Name: John Doe | Date: 2024-01-15
Order: 3 Curry, 2 Rice | Name: Jane Smith | Date: 2024-01-16
```

#### Zelle CSV Export
Export your Zelle transactions as CSV with columns:
- Date
- Description  
- Amount

### 2. Use the Application

1. **Upload Zelle CSV**: Use the file uploader to select your Zelle transactions CSV
2. **Paste WhatsApp Messages**: Copy and paste your WhatsApp order messages into the text area
3. **View Insights**: The dashboard will automatically generate and display:
   - Parsed order data
   - Trending items
   - Top-selling products
   - Low stock alerts
   - Customer retention analysis
   - Reorder patterns

## 📊 Understanding the Insights

### Increasing Items
Items showing consistent growth over the last 3 weeks - consider increasing production.

### Top Items
Your best-selling products by quantity - focus on maintaining quality and availability.

### Low Stock
Items below the stock threshold (10 units) - time to restock.

### Customer Analysis
- **Retained Customers**: Ordered within 14 days - your loyal customer base
- **Churned Customers**: 
  - **Trial**: One-time customers
  - **Quick Churn**: Short-term customers (< 7 days)
  - **Slow Churn**: Long-term customers who stopped ordering

### Reordered Items
Products that customers buy repeatedly - indicates high satisfaction.

## 🏗️ Project Structure

```
whatsapp-insights-tool/
├── data_ingestion.py      # Main Streamlit application
├── requirements.txt       # Python dependencies
├── sample_zelle.csv      # Example Zelle data
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🛠️ Customization

### Modifying Stock Threshold
In `data_ingestion.py`, line 35:
```python
stock_threshold = 10  # Change this value
```

### Adjusting Customer Retention Period
In `data_ingestion.py`, line 42:
```python
retained = customer_orders[customer_orders['days_since_last_order'] <= 14]  # Change 14 to your preferred days
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/moonlightshimmer/whatsapp-insights-tool/issues) page
2. Create a new issue with detailed information about your problem

## 🎯 Perfect For

- **Tiffin Services**: Track daily meal orders and payments
- **Food Delivery**: Analyze order patterns and customer preferences
- **Small Restaurants**: Understand popular dishes and customer behavior
- **Meal Prep Services**: Monitor subscription patterns and retention
- **Any Small Business**: Using WhatsApp for orders and Zelle for payments

---

**Made with ❤️ for small businesses** 