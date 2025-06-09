# ⚔️ ChronoForge: An AI Saga

![ChronoForge Banner](https://via.placeholder.com/800x300/1a1a2e/8b9dc3?text=ChronoForge%3A+An+AI+Saga)

A mystical RPG adventure powered by AI, where you embark on quests generated dynamically by artificial intelligence in the enchanted realms of ChronoForge.

## 🌟 Features

- **🤖 AI-Generated Quests**: Dynamic storylines created by Groq AI
- **🎨 AI-Generated Images**: Beautiful quest scenes powered by Pollinations AI
- **📈 Progress Tracking**: Level up system with XP and achievements
- **💎 Virtual Economy**: Earn and spend Chrono Shards
- **🏆 Achievement System**: Unlock rewards as you progress
- **📊 Analytics Dashboard**: Track your journey with beautiful charts
- **🎒 Inventory Management**: Collect mystical items
- **💾 Save/Export Data**: Download your progress

## 🚀 Live Demo

**Deploy your own:** [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- A free Groq API key ([Get it here](https://console.groq.com/keys))

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/chronoforge-ai-saga.git
   cd chronoforge-ai-saga
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 🌐 Deployment Guide

### Deploy on Streamlit Cloud (Recommended)

1. **Fork this repository** to your GitHub account

2. **Get your Groq API key:**
   - Visit [Groq Console](https://console.groq.com/keys)
   - Create a free account and generate an API key

3. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io/)
   - Click "New app"
   - Connect your GitHub account
   - Select your forked repository
   - Set the main file path: `app.py`
   - Add your environment variables:
     - Variable name: `GROQ_API_KEY`
     - Variable value: Your actual Groq API key
   - Click "Deploy!"

4. **Your app will be live** at a URL like: `https://yourappname.streamlit.app`

### Alternative: Deploy on Heroku

<details>
<summary>Click to expand Heroku deployment guide</summary>

1. **Create a Procfile:**
   ```
   web: sh setup.sh && streamlit run app.py
   ```

2. **Create setup.sh:**
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [general]\n\
   email = \"your-email@domain.com\"\n\
   " > ~/.streamlit/credentials.toml
   echo "\
   [server]\n\
   headless = true\n\
   enableCORS=false\n\
   port = \$PORT\n\
   " > ~/.streamlit/config.toml
   ```

3. **Deploy to Heroku**
</details>

## 🎮 How to Play

1. **Enter your hero name** to begin your adventure
2. **Click "Discover New Quest"** to generate an AI-powered scenario
3. **Read the quest description** and challenge carefully
4. **Submit your creative solution** to the challenge
5. **Earn Chrono Shards and XP** for successful completions
6. **Level up** and unlock achievements
7. **Track your progress** in the Analytics tab
8. **Generate epic images** in the Gallery tab

## 🏗️ Tech Stack

- **Frontend**: Streamlit with custom CSS animations
- **AI Models**: 
  - Groq (Llama 3.3 70B) for quest generation
  - Pollinations AI for image generation
- **Data Visualization**: Plotly Express
- **Data Processing**: Pandas, NumPy
- **Styling**: Custom CSS with gradient animations

## 🎨 Screenshots

| Quest Hub | Analytics | Gallery |
|-----------|-----------|---------|
| ![Quest](https://via.placeholder.com/300x200/2c2c3e/8b9dc3?text=Quest+Hub) | ![Analytics](https://via.placeholder.com/300x200/2c2c3e/a8b2d1?text=Analytics) | ![Gallery](https://via.placeholder.com/300x200/2c2c3e/c5cae9?text=Gallery) |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## 🔧 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key for AI quest generation | Yes |

## 🐛 Troubleshooting

**Common Issues:**

- **"AI Game Master is unavailable"**: Check your GROQ_API_KEY is set correctly
- **Import errors**: Make sure all dependencies are installed: `pip install -r requirements.txt`
- **Deployment issues**: Ensure your repository is public and environment variables are set

## 🌟 Support

If you like this project, please give it a ⭐ on GitHub!

For support, please open an issue on GitHub or contact [your-email@domain.com](mailto:your-email@domain.com).

---

**Built with ❤️ using Streamlit and AI magic** ✨ 