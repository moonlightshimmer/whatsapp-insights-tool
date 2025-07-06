# Streamlit Cloud Deployment Guide

## 🚀 Deploying to Streamlit Cloud

### Prerequisites
1. **GitHub Repository**: Your code must be in a GitHub repository
2. **Streamlit Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **Requirements File**: Ensure `requirements.txt` is in your root directory

### Step-by-Step Deployment

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Add WhatsApp integration and visualizations"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Set the main file path: `data_ingestion.py`
   - Click "Deploy"

### 🔧 Troubleshooting WhatsApp Integration

#### Issue: WhatsApp Integration Section Not Showing

**Cause**: Import errors in Streamlit Cloud environment

**Solution**: The app now includes robust error handling and fallback options:

1. **Check the deployment logs** in Streamlit Cloud dashboard
2. **Verify all files are uploaded** to GitHub:
   - `whatsapp_integration/` directory with `__init__.py` and `core.py`
   - `visualizations/` directory with `__init__.py` and `core.py`
   - `requirements.txt`

3. **If imports fail**, the app will show:
   - Warning messages about missing modules
   - Fallback to original text input method
   - Basic functionality without advanced features
   - Multiple import path attempts for better compatibility

#### File Structure for Deployment

Ensure your repository has this structure:
```
whatsapp-insights-tool/
├── data_ingestion.py              # Main application
├── whatsapp_integration/          # WhatsApp integration module
│   ├── __init__.py               # Module initialization
│   └── core.py                   # Core integration functionality
├── visualizations/                # Visualizations module
│   ├── __init__.py               # Module initialization
│   └── core.py                   # Core visualization functionality
├── requirements.txt               # Dependencies
├── sample_whatsapp_export.txt     # Sample exported WhatsApp chat
├── sample_zelle_comprehensive.csv # Sample Zelle data
├── sample_whatsapp_messages.txt   # Sample WhatsApp messages
├── README.md                      # Documentation
└── DEPLOYMENT_GUIDE.md            # This guide
```

### 📋 Requirements.txt for Streamlit Cloud

Your `requirements.txt` should include:
```
streamlit==1.35.0
pandas==2.2.2
plotly==5.18.0
numpy==1.24.3
```

### 🏗️ Module Structure Benefits

The new module structure provides several advantages:

1. **Better Organization**: Code is separated into logical modules
2. **Easier Maintenance**: Each module has a single responsibility
3. **Improved Testing**: Modules can be tested independently
4. **Better Documentation**: Each module has clear docstrings and type hints
5. **Streamlit Cloud Compatible**: Multiple import paths ensure deployment success
6. **Logging Support**: Comprehensive logging for debugging

#### Module Components

- **`whatsapp_integration/`**: Handles WhatsApp chat parsing and order extraction
  - `__init__.py`: Module initialization and exports
  - `core.py`: Core integration functionality with logging

- **`visualizations/`**: Creates interactive charts and dashboards
  - `__init__.py`: Module initialization and exports
  - `core.py`: Core visualization functionality with error handling

### 🔍 Debugging Steps

1. **Check Streamlit Cloud Logs**
   - Go to your app dashboard
   - Click "Manage app"
   - Check "App logs" for error messages

2. **Test Locally First**
   ```bash
   streamlit run data_ingestion.py
   ```

3. **Verify File Paths**
   - Ensure all Python files are in the root directory
   - Check that file names match exactly

4. **Check Import Statements**
   - All imports should be relative to the root directory
   - No absolute paths should be used

### 🛠️ Common Issues and Solutions

#### Issue 1: ModuleNotFoundError
**Error**: `ModuleNotFoundError: No module named 'whatsapp_integration'`

**Solution**: 
- Ensure `whatsapp_integration/` directory exists with `__init__.py` and `core.py`
- Check that the directory name matches exactly
- Verify all files are committed to GitHub
- The app now tries multiple import paths for better compatibility

#### Issue 2: Import Error for Plotly
**Error**: `ImportError: No module named 'plotly'`

**Solution**:
- Add `plotly==5.18.0` to `requirements.txt`
- Redeploy the app
- The app will show a warning and continue without visualizations

#### Issue 3: File Upload Issues
**Error**: File uploader not working

**Solution**:
- Check that the file is a valid CSV
- Ensure the CSV has the expected columns (Date, Description, Amount)
- Try with the sample files first

### 📱 Testing the Deployment

1. **Test with Sample Data**
   - Use `sample_whatsapp_export.txt` for WhatsApp chat export
   - Use `sample_whatsapp_messages.txt` for text input
   - Use `sample_zelle_comprehensive.csv` for payment data

2. **Verify Features**
   - WhatsApp export upload should work
   - Text input fallback should work
   - Visualizations should display with interactive charts
   - Insights should generate with detailed metrics
   - Module imports should work with proper error handling

### 🔄 Redeployment

If you make changes:
1. **Update your local files**
2. **Commit and push to GitHub**
   ```bash
   git add .
   git commit -m "Fix deployment issues"
   git push origin main
   ```
3. **Streamlit Cloud will automatically redeploy**

### 📞 Getting Help

If issues persist:
1. **Check Streamlit Cloud documentation**
2. **Review the app logs** for specific error messages
3. **Test locally** to isolate the issue
4. **Verify all dependencies** are in requirements.txt

### 🎯 Best Practices

1. **Use proper module structure** with `__init__.py` files
2. **Test module imports locally** before deploying
3. **Monitor app logs** after deployment for import issues
4. **Use sample data** for testing all features
5. **Verify all dependencies** are in requirements.txt
6. **Check file permissions** for module directories

---

**Note**: The app now includes robust error handling and proper module structure. Even if some modules fail to import, the basic functionality will still work with fallback options. The new module structure provides better organization and maintainability. 