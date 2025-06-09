import streamlit as st
import groq
import os
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import json
from typing import Dict, Any, List
import hashlib
import requests
import base64
from io import BytesIO
from PIL import Image
import numpy as np

# --- 1. CONFIGURATION & INITIALIZATION ---

# Load environment variables from .env file
load_dotenv()

# Set up Streamlit page config with enhanced styling
st.set_page_config(
    page_title="ChronoForge: An AI Saga",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Advanced CSS styling with animations and modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap');
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #2c2c3e 25%, #3a3a4e 50%, #4a4a5e 75%, #5a5a6e 100%);
        background-size: 400% 400%;
        animation: gradientShift 12s ease infinite;
        color: #e8e8e8;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Enhanced button styling */
    .stButton>button {
        background: linear-gradient(45deg, #6b73ff, #5a67d8, #4c51bf);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 15px;
        font-family: 'Orbitron', monospace;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(107, 115, 255, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 25px rgba(107, 115, 255, 0.3);
        background: linear-gradient(45deg, #7c3aed, #6b73ff, #5a67d8);
    }
    
    .stButton>button:active {
        transform: translateY(-2px) scale(1.02);
    }
    
    /* Glowing text effects */
    .main-title {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #8b9dc3, #a8b2d1, #c5cae9, #9fa8da);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 6s ease infinite, glow 4s ease-in-out infinite alternate;
        text-shadow: 0 0 20px rgba(139, 157, 195, 0.3);
        margin-bottom: 2rem;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 10px rgba(139, 157, 195, 0.3)); }
        to { filter: drop-shadow(0 0 15px rgba(168, 178, 209, 0.5)); }
    }
    
    /* Enhanced containers */
    .custom-container {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 25px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(139, 157, 195, 0.2);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .custom-container::before {
        content: '';
        position: absolute;
        top: -1px;
        left: -1px;
        right: -1px;
        bottom: -1px;
        background: linear-gradient(45deg, #8b9dc3, #a8b2d1, #c5cae9, #9fa8da);
        border-radius: 15px;
        z-index: -1;
        animation: borderGlow 6s linear infinite;
    }
    
    @keyframes borderGlow {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.6; }
    }
    
    .custom-container:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 15px 35px rgba(139, 157, 195, 0.2);
    }
    
    /* Sidebar enhancements */
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, rgba(15, 15, 35, 0.9), rgba(26, 26, 46, 0.9));
        border-radius: 15px;
    }
    
    /* Metrics styling */
    .metric-container {
        background: linear-gradient(135deg, rgba(139, 157, 195, 0.15), rgba(168, 178, 209, 0.15));
        border-radius: 12px;
        padding: 15px;
        border: 1px solid rgba(139, 157, 195, 0.25);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        background: linear-gradient(135deg, rgba(139, 157, 195, 0.25), rgba(168, 178, 209, 0.25));
        transform: scale(1.02);
    }
    
    /* Quest card styling */
    .quest-card {
        background: linear-gradient(135deg, rgba(168, 178, 209, 0.15), rgba(197, 202, 233, 0.15));
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(168, 178, 209, 0.3);
        backdrop-filter: blur(8px);
        position: relative;
    }
    
    .quest-card::before {
        content: '⚔️';
        position: absolute;
        top: -8px;
        left: -8px;
        font-size: 1.8rem;
        background: linear-gradient(45deg, #8b9dc3, #a8b2d1);
        border-radius: 50%;
        padding: 8px;
        box-shadow: 0 0 15px rgba(139, 157, 195, 0.3);
    }
    
    /* Image styling */
    .game-image {
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
        border: 3px solid rgba(0, 212, 255, 0.5);
    }
    
    .game-image:hover {
        transform: scale(1.05);
        box-shadow: 0 25px 50px rgba(0, 212, 255, 0.6);
    }
    
    /* Loading animations */
    .loading-spinner {
        display: inline-block;
        width: 40px;
        height: 40px;
        border: 3px solid rgba(0, 212, 255, 0.3);
        border-radius: 50%;
        border-top-color: #00d4ff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 15px;
        padding: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(45deg, rgba(0, 212, 255, 0.2), rgba(0, 255, 136, 0.2));
        border-radius: 10px;
        padding: 10px 20px;
        font-family: 'Orbitron', monospace;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #00d4ff, #00ff88);
        color: #000;
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background: linear-gradient(45deg, rgba(0, 255, 136, 0.2), rgba(78, 205, 196, 0.2));
        border: 2px solid #00ff88;
        border-radius: 15px;
    }
    
    .stError {
        background: linear-gradient(45deg, rgba(255, 107, 107, 0.2), rgba(255, 99, 99, 0.2));
        border: 2px solid #ff6b6b;
        border-radius: 15px;
    }
    
    /* Particle effect background */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .particle {
        position: absolute;
        width: 3px;
        height: 3px;
        background: rgba(139, 157, 195, 0.4);
        border-radius: 50%;
        animation: float 8s infinite linear;
    }
    
    @keyframes float {
        0% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh) rotate(360deg);
            opacity: 0;
        }
    }
</style>
""", unsafe_allow_html=True)

# Add particle effect
st.markdown("""
<div class="particles">
    <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
    <div class="particle" style="left: 20%; animation-delay: 1s;"></div>
    <div class="particle" style="left: 30%; animation-delay: 2s;"></div>
    <div class="particle" style="left: 40%; animation-delay: 3s;"></div>
    <div class="particle" style="left: 50%; animation-delay: 4s;"></div>
    <div class="particle" style="left: 60%; animation-delay: 5s;"></div>
    <div class="particle" style="left: 70%; animation-delay: 0.5s;"></div>
    <div class="particle" style="left: 80%; animation-delay: 1.5s;"></div>
    <div class="particle" style="left: 90%; animation-delay: 2.5s;"></div>
</div>
""", unsafe_allow_html=True)

# --- 2. INTEGRATED POLLINATIONS AI CLASS ---

class PollinationsAI:
    def __init__(self):
        self.base_url = "https://pollinations.ai/p"
    
    def generate_image(self, prompt, style="fantasy art, digital painting, high quality", width=512, height=512):
        """Generate an image using Pollinations AI"""
        try:
            # Clean and enhance the prompt
            enhanced_prompt = f"{prompt}, {style}, ultra detailed, 8k resolution, masterpiece"
            
            # URL encode the prompt
            import urllib.parse
            encoded_prompt = urllib.parse.quote(enhanced_prompt)
            
            # Construct the image URL
            image_url = f"{self.base_url}/{encoded_prompt}?width={width}&height={height}&nologo=true&enhance=true"
            
            # Return the URL for direct display
            return image_url
        except Exception as e:
            st.error(f"Error generating image: {str(e)}")
            return None
    
    def generate_quest_image(self, quest_title, quest_description):
        """Generate a specific image for a quest"""
        prompt = f"Epic fantasy quest scene: {quest_title}. {quest_description}. Cinematic lighting, dramatic atmosphere"
        return self.generate_image(prompt)
    
    def generate_achievement_image(self, achievement_title):
        """Generate an image for an achievement"""
        prompt = f"Glowing magical trophy representing {achievement_title}, golden aura, mystical energy"
        return self.generate_image(prompt)
    
    def generate_character_image(self, character_name):
        """Generate character portrait"""
        prompt = f"Fantasy RPG character portrait: {character_name}, heroic pose, detailed armor, magical aura"
        return self.generate_image(prompt)

# Initialize Pollinations AI
pollinations = PollinationsAI()

# Initialize Groq client
try:
    groq_client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
    MODEL_NAME = "llama-3.3-70b-versatile"
except Exception as e:
    st.error(f"Failed to initialize Groq client: {e}")
    groq_client = None

# --- 3. ENHANCED GAME STATE MANAGEMENT ---

if 'player_data' not in st.session_state:
    st.session_state.player_data = {
        'name': '',
        'shards': 100,
        'quests_completed': 0,
        'inventory': ["✨ Mystic Compass", "🗡️ Starter Blade"],
        'achievements': [],
        'history': pd.DataFrame(columns=['timestamp', 'shards']),
        'nft_collection': [],
        'wallet_address': None,
        'last_quest_time': None,
        'daily_streak': 0,
        'total_earnings': 0,
        'character_image': None,
        'level': 1,
        'experience': 0,
        'health': 100,
        'mana': 50
    }

# Initialize other session state variables
if 'game_log' not in st.session_state:
    st.session_state.game_log = []

if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = None

if 'active_quest' not in st.session_state:
    st.session_state.active_quest = None

# Enhanced achievements with better rewards
ACHIEVEMENTS = {
    'first_quest': {
        'title': '🌟 First Steps',
        'description': 'Complete your first quest in ChronoForge',
        'requirement': 1,
        'reward': 75,
        'xp_reward': 50,
        'icon': '🌟'
    },
    'quest_master': {
        'title': '⚔️ Quest Master',
        'description': 'Complete 5 challenging quests',
        'requirement': 5,
        'reward': 200,
        'xp_reward': 150,
        'icon': '⚔️'
    },
    'shard_collector': {
        'title': '💎 Shard Collector',
        'description': 'Accumulate 500 Chrono Shards',
        'requirement': 500,
        'reward': 150,
        'xp_reward': 100,
        'icon': '💎'
    },
    'legendary_hero': {
        'title': '👑 Legendary Hero',
        'description': 'Complete 10 quests and become a legend',
        'requirement': 10,
        'reward': 500,
        'xp_reward': 300,
        'icon': '👑'
    }
}

# --- 4. ENHANCED GAME LOGIC FUNCTIONS ---

def log_event(message: str):
    """Adds an event to the game log with timestamp."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    st.session_state.game_log.insert(0, f"[{timestamp}] {message}")
    if len(st.session_state.game_log) > 50:  # Keep only last 50 events
        st.session_state.game_log = st.session_state.game_log[:50]

def update_shard_history():
    """Records the current shard count with a timestamp."""
    new_record = pd.DataFrame([{
        'timestamp': datetime.now(), 
        'shards': st.session_state.player_data['shards'],
        'level': st.session_state.player_data['level']
    }])
    st.session_state.player_data['history'] = pd.concat([st.session_state.player_data['history'], new_record], ignore_index=True)

def gain_experience(amount: int):
    """Add experience and handle level ups"""
    st.session_state.player_data['experience'] += amount
    
    # Level up calculation
    level = st.session_state.player_data['level']
    xp_needed = level * 100  # 100 XP per level
    
    if st.session_state.player_data['experience'] >= xp_needed:
        st.session_state.player_data['level'] += 1
        st.session_state.player_data['experience'] -= xp_needed
        st.session_state.player_data['health'] = 100  # Full heal on level up
        st.session_state.player_data['mana'] += 10  # Increase max mana
        
        st.balloons()
        st.success(f"🎉 LEVEL UP! You are now level {st.session_state.player_data['level']}!")
        log_event(f"Level up! Now level {st.session_state.player_data['level']}")

def check_achievements():
    """Enhanced achievement checking with better feedback"""
    player = st.session_state.player_data
    new_achievements = []
    
    for key, ach in ACHIEVEMENTS.items():
        if key not in player['achievements']:
            condition_met = False
            
            if key == 'first_quest' and player['quests_completed'] >= 1:
                condition_met = True
            elif key == 'quest_master' and player['quests_completed'] >= 5:
                condition_met = True
            elif key == 'shard_collector' and player['shards'] >= 500:
                condition_met = True
            elif key == 'legendary_hero' and player['quests_completed'] >= 10:
                condition_met = True
            
            if condition_met:
                player['achievements'].append(key)
                player['shards'] += ach['reward']
                gain_experience(ach['xp_reward'])
                new_achievements.append(ach)
                log_event(f"🏆 Achievement Unlocked: {ach['title']}! +{ach['reward']} Shards, +{ach['xp_reward']} XP")
    
    if new_achievements:
        for ach in new_achievements:
            st.success(f"🏆 **Achievement Unlocked!** {ach['icon']} {ach['title']}")
        update_shard_history()

def call_ai_gm(system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
    """Enhanced AI Game Master with better error handling"""
    if not groq_client:
        st.error("AI Game Master is unavailable. Please check your API configuration.")
        return None
    
    try:
        completion = groq_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=2048,
            response_format={"type": "json_object"},
        )
        response_content = completion.choices[0].message.content
        log_event(f"🤖 AI GM Response received")
        return response_content
    except Exception as e:
        st.error(f"The AI Game Master is currently resting... (Error: {str(e)[:50]}...)")
        log_event(f"ERROR: AI GM call failed: {e}")
        return None

def generate_scenario_and_quest():
    """Enhanced quest generation with better variety"""
    system_prompt = """
    You are the ultimate Game Master for 'ChronoForge', a mystical realm where magic meets technology.
    Create an immersive scenario and challenging quest based on the player's progression.
    
    The world contains:
    - Ancient ruins with forgotten technology
    - Mystical forests with magical creatures
    - Floating cities powered by crystal energy
    - Time rifts that lead to different eras
    - Dragons that guard temporal artifacts
    
    Generate a unique scenario (2-3 vivid sentences) and a quest that matches the player's level.
    Higher level players should face more complex challenges with greater rewards.
    
    Output ONLY valid JSON with keys: 'scenario', 'quest'.
    Quest object needs: 'title', 'description', 'reward' (50-400 based on difficulty), 'challenge', 'difficulty' (1-5).
    
    Example:
    {
      "scenario": "The Crystalline Spires of Aethermoor pulse with unstable energy, creating temporal anomalies that threaten reality itself. Ancient guardians stir from their millennium slumber.",
      "quest": {
        "title": "The Temporal Convergence",
        "description": "Stabilize the crystal network before the timeline fractures permanently.",
        "reward": 250,
        "challenge": "You must solve the ancient riddle of the Crystal Masters: 'I am the beginning of eternity, the end of time and space, the beginning of every end, and the end of every place. What am I?'",
        "difficulty": 3
      }
    }
    """
    
    player_level = st.session_state.player_data['level']
    user_prompt = f"""
    Player Status:
    - Level: {player_level}
    - Shards: {st.session_state.player_data['shards']}
    - Quests Completed: {st.session_state.player_data['quests_completed']}
    - Recent Inventory: {', '.join(st.session_state.player_data['inventory'][-3:])}
    
    Generate a level-appropriate quest with escalating difficulty and rewards.
    """
    
    response_str = call_ai_gm(system_prompt, user_prompt)
    if response_str:
        try:
            data = json.loads(response_str)
            st.session_state.current_scenario = data['scenario']
            st.session_state.active_quest = data['quest']
            log_event(f"🗺️ New Quest: {data['quest']['title']}")
        except (json.JSONDecodeError, KeyError) as e:
            st.error("The mystical energies are disrupted. Try exploring again.")
            log_event(f"ERROR: Failed to parse quest data: {e}")

def evaluate_quest_solution(quest: Dict[str, Any], solution: str):
    """Enhanced quest evaluation with dynamic rewards"""
    system_prompt = """
    You are the wise Game Master of ChronoForge. Evaluate the player's creative solution fairly.
    Consider creativity, logic, and effort. Be encouraging even for partial solutions.
    
    Provide detailed, immersive feedback that makes the player feel their actions matter.
    Award bonus rewards for exceptionally creative or clever solutions.
    
    Output ONLY valid JSON with keys: 'success' (boolean), 'feedback' (narrative response), 'bonus_reward' (0-100 extra shards for creativity).
    """
    
    user_prompt = f"""
    Quest: {quest['title']}
    Challenge: {quest['challenge']}
    Player's Solution: {solution}
    Player Level: {st.session_state.player_data['level']}
    
    Evaluate this solution with rich, immersive feedback.
    """
    
    response_str = call_ai_gm(system_prompt, user_prompt, temperature=0.6)
    if response_str:
        try:
            result = json.loads(response_str)
            if result['success']:
                total_reward = quest['reward'] + result.get('bonus_reward', 0)
                complete_quest(total_reward, result['feedback'])
                if result.get('bonus_reward', 0) > 0:
                    st.info(f"🌟 Creativity Bonus: +{result['bonus_reward']} Shards!")
            else:
                log_event(f"❌ Quest Failed: {quest['title']}")
                st.warning(f"**Quest Outcome:** {result['feedback']}")
            st.session_state.active_quest = None
        except (json.JSONDecodeError, KeyError) as e:
            st.error("The Game Master's wisdom is unclear. The quest continues.")
            log_event(f"ERROR: Failed to parse evaluation: {e}")

def complete_quest(reward: int, feedback: str):
    """Enhanced quest completion with level-appropriate rewards"""
    player = st.session_state.player_data
    player['shards'] += reward
    player['quests_completed'] += 1
    
    # XP based on quest reward
    xp_gain = reward // 5
    gain_experience(xp_gain)
    
    log_event(f"✅ Quest Complete! +{reward} Shards, +{xp_gain} XP")
    st.success(f"**🎉 QUEST COMPLETED!** {feedback}")
    
    # Random item reward for higher level quests
    if reward > 150 and np.random.random() > 0.5:
        rare_items = ["🔮 Mystic Orb", "⚡ Lightning Rod", "🛡️ Dragon Scale Shield", "🗝️ Ancient Key", "💍 Ring of Power"]
        new_item = np.random.choice(rare_items)
        player['inventory'].append(new_item)
        st.info(f"🎁 Bonus Item Found: {new_item}")
    
    update_shard_history()
    check_achievements()

# --- 5. ENHANCED UI RENDERING ---

def render_enhanced_sidebar():
    """Ultra-modern sidebar with rich visuals"""
    with st.sidebar:
        # Character header with image
        player_name = st.session_state.player_data.get('name', 'Adventurer')
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, rgba(0,212,255,0.2), rgba(0,255,136,0.2)); border-radius: 15px; margin-bottom: 20px;'>
            <h2 style='color: #00d4ff; font-family: Orbitron; margin: 0;'>⚔️ {player_name}</h2>
            <p style='color: #4ecdc4; margin: 5px 0;'>Level {st.session_state.player_data['level']} Hero</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Character image
        if not st.session_state.player_data['character_image'] and player_name:
            st.session_state.player_data['character_image'] = pollinations.generate_character_image(player_name)
        
        if st.session_state.player_data['character_image']:
            st.image(st.session_state.player_data['character_image'], caption="Your Character", use_column_width=True)
        
        # Enhanced stats display
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class='metric-container'>
                <h3 style='color: #00d4ff; margin: 0;'>💎 {st.session_state.player_data['shards']}</h3>
                <p style='margin: 0; font-size: 0.8em;'>Chrono Shards</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-container'>
                <h3 style='color: #00ff88; margin: 0;'>📜 {st.session_state.player_data['quests_completed']}</h3>
                <p style='margin: 0; font-size: 0.8em;'>Quests Done</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Progress bars
        st.markdown("### 📊 Character Stats")
        
        # Health bar
        health_pct = st.session_state.player_data['health']
        st.markdown(f"❤️ Health: {health_pct}/100")
        st.progress(health_pct / 100)
        
        # Mana bar
        mana = st.session_state.player_data['mana']
        st.markdown(f"💙 Mana: {mana}")
        st.progress(min(mana / 100, 1.0))
        
        # XP bar
        xp = st.session_state.player_data['experience']
        level = st.session_state.player_data['level']
        xp_needed = level * 100
        st.markdown(f"⭐ XP: {xp}/{xp_needed}")
        st.progress(xp / xp_needed if xp_needed > 0 else 0)
        
        # Inventory with icons
        st.markdown("### 🎒 Mystical Inventory")
        if st.session_state.player_data['inventory']:
            for item in st.session_state.player_data['inventory'][-5:]:  # Show last 5 items
                st.markdown(f"• {item}")
            if len(st.session_state.player_data['inventory']) > 5:
                st.caption(f"... and {len(st.session_state.player_data['inventory']) - 5} more items")
        else:
            st.caption("Your inventory awaits magical items...")
        
        # Achievements showcase
        st.markdown("### 🏆 Hall of Glory")
        if st.session_state.player_data['achievements']:
            for key in st.session_state.player_data['achievements']:
                ach = ACHIEVEMENTS[key]
                st.markdown(f"🏅 **{ach['icon']} {ach['title']}**")
                st.caption(ach['description'])
        else:
            st.caption("Complete quests to unlock achievements...")
        
        # Game log section
        st.markdown("### 📜 Recent Events")
        if st.session_state.game_log:
            for event in st.session_state.game_log[:5]:  # Show last 5 events
                st.caption(event)
        else:
            st.caption("Your journey begins...")

def render_main_dashboard():
    """Enhanced main dashboard with tabs and rich content"""
    st.markdown('<h1 class="main-title">⚔️ ChronoForge: An AI Saga ⚔️</h1>', unsafe_allow_html=True)
    
    # Player name input if not set
    if not st.session_state.player_data['name']:
        st.markdown("### 🌟 Welcome, Hero! What shall we call you?")
        col1, col2 = st.columns([3, 1])
        with col1:
            name = st.text_input("Enter your heroic name:", placeholder="Legendary Adventurer")
        with col2:
            if st.button("Begin Journey!", type="primary"):
                if name.strip():
                    st.session_state.player_data['name'] = name.strip()
                    st.session_state.player_data['character_image'] = pollinations.generate_character_image(name.strip())
                    log_event(f"🌟 Hero {name.strip()} has entered ChronoForge!")
                    st.rerun()
                else:
                    st.error("Please enter a name to begin your adventure!")
        return
    
    # Main game tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Quest Hub", "📊 Analytics", "🖼️ Gallery", "⚙️ Settings"])
    
    with tab1:
        render_quest_hub()
    
    with tab2:
        render_analytics()
    
    with tab3:
        render_gallery()
    
    with tab4:
        render_settings()

def render_quest_hub():
    """Enhanced quest hub with dynamic content"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Current scenario display
        if st.session_state.current_scenario:
            st.markdown(f"""
            <div class='custom-container'>
                <h3 style='color: #00d4ff;'>🌍 Current Realm</h3>
                <p style='font-size: 1.1em; line-height: 1.6;'>{st.session_state.current_scenario}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display quest image if available
            if st.session_state.active_quest:
                quest_image = pollinations.generate_quest_image(
                    st.session_state.active_quest['title'],
                    st.session_state.active_quest['description']
                )
                if quest_image:
                    st.image(quest_image, caption="Quest Scene", use_column_width=True, clamp=True)
        
        # Active quest
        if st.session_state.active_quest:
            quest = st.session_state.active_quest
            st.markdown(f"""
            <div class='quest-card'>
                <h3 style='color: #ff6b6b; margin-top: 20px;'>{quest['title']}</h3>
                <p style='font-size: 1.1em; margin: 15px 0;'>{quest['description']}</p>
                <p style='color: #4ecdc4;'><strong>Challenge:</strong> {quest['challenge']}</p>
                <p style='color: #00ff88;'><strong>Reward:</strong> {quest['reward']} Chrono Shards</p>
                <p style='color: #ffd700;'><strong>Difficulty:</strong> {'⭐' * quest['difficulty']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Solution input
            st.markdown("### 💭 Your Response")
            solution = st.text_area(
                "How do you tackle this challenge?",
                placeholder="Describe your creative solution...",
                height=100
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🚀 Submit Solution", type="primary"):
                    if solution.strip():
                        with st.spinner("The Game Master evaluates your actions..."):
                            time.sleep(2)  # Dramatic pause
                            evaluate_quest_solution(quest, solution)
                    else:
                        st.error("You must provide a solution to proceed!")
            
            with col2:
                if st.button("⏭️ Skip Quest"):
                    st.session_state.active_quest = None
                    st.session_state.current_scenario = None
                    st.info("Quest abandoned. New adventures await!")
        
        else:
            # No active quest
            st.markdown("""
            <div class='custom-container' style='text-align: center; padding: 40px;'>
                <h3 style='color: #00d4ff;'>🗺️ Ready for Adventure?</h3>
                <p style='font-size: 1.2em; margin: 20px 0;'>The mystical realms of ChronoForge await your exploration!</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🌟 Discover New Quest", type="primary", key="new_quest"):
                with st.spinner("Consulting the mystical forces..."):
                    time.sleep(2)
                    generate_scenario_and_quest()
                    st.rerun()
    
    with col2:
        # Quick stats
        st.markdown("### ⚡ Quick Stats")
        player = st.session_state.player_data
        
        stats_data = {
            "💎 Shards": player['shards'],
            "📜 Quests": player['quests_completed'],
            "🏆 Achievements": len(player['achievements']),
            "⭐ Level": player['level'],
            "🎒 Items": len(player['inventory'])
        }
        
        for label, value in stats_data.items():
            st.metric(label, value)
        
        # Daily quest button
        st.markdown("### 🌅 Daily Challenge")
        if st.button("🎲 Random Quest", help="Get a quick random quest"):
            with st.spinner("Generating challenge..."):
                generate_scenario_and_quest()
                st.rerun()

def render_analytics():
    """Enhanced analytics with beautiful charts"""
    st.markdown("### 📈 Your Journey Statistics")
    
    player = st.session_state.player_data
    
    if not player['history'].empty:
        # Shards over time
        fig = px.line(
            player['history'], 
            x='timestamp', 
            y='shards',
            title='💎 Chrono Shards Over Time',
            line_shape='spline'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Level progression
        if 'level' in player['history'].columns:
            fig2 = px.bar(
                player['history'],
                x='timestamp',
                y='level',
                title='⭐ Level Progression',
                color='level',
                color_continuous_scale='viridis'
            )
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Complete some quests to see your analytics!")
    
    # Achievement progress
    st.markdown("### 🏆 Achievement Progress")
    for key, ach in ACHIEVEMENTS.items():
        is_unlocked = key in player['achievements']
        progress_val = 0
        
        if key == 'first_quest':
            progress_val = min(player['quests_completed'], 1)
        elif key == 'quest_master':
            progress_val = min(player['quests_completed'], 5)
        elif key == 'shard_collector':
            progress_val = min(player['shards'], 500)
        elif key == 'legendary_hero':
            progress_val = min(player['quests_completed'], 10)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if is_unlocked:
                st.success(f"🏅 {ach['icon']} {ach['title']} - COMPLETED!")
            else:
                st.info(f"{ach['icon']} {ach['title']}")
                st.progress(progress_val / ach['requirement'])
        with col2:
            st.caption(f"{ach['reward']} shards")

def render_gallery():
    """Image gallery showing generated quest and character images"""
    st.markdown("### 🖼️ Your Adventure Gallery")
    
    # Character image
    if st.session_state.player_data['character_image']:
        st.markdown("#### 👤 Your Character")
        st.image(st.session_state.player_data['character_image'], width=300)
    
    # Generate sample gallery images
    col1, col2, col3 = st.columns(3)
    
    sample_images = [
        ("Mystical Forest", "An enchanted forest with glowing trees and magical creatures"),
        ("Dragon's Lair", "A dark cave with a massive dragon guarding ancient treasures"),
        ("Floating City", "A magnificent city floating in the clouds with crystal spires")
    ]
    
    for i, (title, desc) in enumerate(sample_images):
        with [col1, col2, col3][i]:
            if st.button(f"Generate {title}", key=f"gen_{i}"):
                with st.spinner(f"Creating {title}..."):
                    image_url = pollinations.generate_image(desc)
                    if image_url:
                        st.image(image_url, caption=title, use_column_width=True)

def render_settings():
    """Game settings and data management"""
    st.markdown("### ⚙️ Game Settings")
    
    # Export/Import data
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📤 Export Data")
        if st.button("Download Save File"):
            save_data = {
                'player_data': st.session_state.player_data,
                'game_log': st.session_state.game_log,
                'timestamp': datetime.now().isoformat()
            }
            # Convert DataFrame to dict for JSON serialization
            if not st.session_state.player_data['history'].empty:
                save_data['player_data']['history'] = st.session_state.player_data['history'].to_dict('records')
            
            json_data = json.dumps(save_data, indent=2, default=str)
            st.download_button(
                label="📁 Download ChronoForge Save",
                data=json_data,
                file_name=f"chronoforge_save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        st.markdown("#### 🗑️ Reset Progress")
        if st.button("⚠️ Reset All Data", type="secondary"):
            if st.button("🚨 Confirm Reset", type="secondary"):
                # Reset all session state
                for key in list(st.session_state.keys()):
                    if key.startswith('player_') or key in ['game_log', 'current_scenario', 'active_quest']:
                        del st.session_state[key]
                st.success("Game data reset! Refresh the page to start over.")
    
    # Game statistics
    st.markdown("#### 📊 Session Statistics")
    stats = {
        "Session Duration": "N/A",  # Could implement session tracking
        "API Calls Made": len(st.session_state.game_log),
        "Images Generated": "Dynamic",
        "Total Events": len(st.session_state.game_log)
    }
    
    for label, value in stats.items():
        st.metric(label, value)

# --- 6. MAIN APPLICATION ---

def main():
    """Main application entry point"""
    try:
        # Render sidebar
        render_enhanced_sidebar()
        
        # Render main content
        render_main_dashboard()
        
        # Auto-save periodically
        if st.session_state.player_data['name']:
            update_shard_history()
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Try refreshing the page or contact support if the issue persists.")

if __name__ == "__main__":
    main()