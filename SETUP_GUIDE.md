# ChronoForge Setup Guide

## Getting Started with ChronoForge

Follow these steps to set up and run ChronoForge on your system.

## Step 1: Get Your Groq API Key

1. **Visit [console.groq.com](https://console.groq.com/keys)**
2. **Sign up for a free account** (if you don't have one)
3. **Generate a new API key**
4. **Copy the API key** (it looks like: `gsk_...`)

## Step 2: Configure Your API Key

### Option A: For Local Development (Recommended)

1. **Create a `.env` file** in your project directory:
   ```bash
   # Create .env file
   touch .env
   ```

2. **Add your API key to the .env file**:
   ```
   GROQ_API_KEY=your_actual_api_key_here
   ```

3. **Make sure `.env` is in your `.gitignore`** (already included)

### Option B: Set Environment Variable

**Windows:**
```cmd
set GROQ_API_KEY=your_actual_api_key_here
```

**Mac/Linux:**
```bash
export GROQ_API_KEY=your_actual_api_key_here
```

### Option C: Manual Input (Fallback)

If the above methods don't work, the app will prompt you to enter your API key manually when you run it.

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Run the Application

```bash
streamlit run app.py
```

## Step 5: For Streamlit Cloud Deployment

1. **Push your code to GitHub** (without the .env file)
2. **Go to [share.streamlit.io](https://share.streamlit.io/)**
3. **Deploy your app**
4. **In the app settings, add your secrets**:
   ```toml
   [general]
   GROQ_API_KEY = "your_actual_api_key_here"
   ```

## Troubleshooting

### Error: "Failed to initialize Groq client"

**Solution 1**: Check your API key format
- Make sure it starts with `gsk_`
- Ensure there are no extra spaces or quotes
- Verify the key is active on console.groq.com

**Solution 2**: Verify environment setup
- Check if `.env` file exists and contains the key
- Restart your terminal/IDE after setting environment variables
- Try the manual input option in the app

**Solution 3**: Check API limits
- Ensure you haven't exceeded free tier limits
- Verify your Groq account is active

### App runs but no quests generate

**Solution**: 
- Check the "System Status" in the sidebar
- Click "Check API Health" to test connection
- Look at the event log for error messages

### Images not loading

**Solution**: 
- This is normal - Pollinations AI images may take time to load
- Check your internet connection
- Try refreshing the page

## Getting Help

1. **Check the sidebar** - Look for error messages in "Recent Events"
2. **Use API Health Check** - Test your connection in the sidebar
3. **Check GitHub Issues** - Report bugs or ask questions
4. **Try Quick Quest** - Use the faster model if primary model fails

## System Requirements

- **Python 3.8 or higher**
- **Internet connection** (for AI services)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- **Groq API account** (free tier available)

## Optional: Advanced Configuration

### Custom Model Selection
You can modify the model preferences in `app.py`:
```python
MODEL_NAME = "llama-3.3-70b-versatile"  # Primary model
FAST_MODEL = "llama3-8b-8192"           # Quick quests
CREATIVE_MODEL = "mixtral-8x7b-32768"   # Creative content
```

### Performance Tuning
For better performance on slower connections:
- Use "Quick Quest" option more often
- Reduce image generation frequency
- Lower the creativity temperature in model calls

Enjoy your adventure in ChronoForge! ⚔️ 