import streamlit as st
import requests

#  Spoonacular

API_KEY = "773933b2d1a64aa9851f9b6d5d28b2c2"
BASE_URL = "https://api.spoonacular.com/recipes/findByIngredients"

# Page Config

st.set_page_config(
    page_title="Culinary Oracle",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

#  Styling

st.markdown(
    """
    <style>
    [data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="stToolbar"], .stDeployButton{display:none!important}

    .stApp{background:#1a1a2e!important;display:flex!important;justify-content:center!important;align-items:flex-start!important;padding-top:30px!important;}
    .block-container{width:375px!important;max-width:375px!important;height:667px!important;border-radius:40px!important;background:linear-gradient(180deg,#fffbeb 0%,#ffeef8 40%,#e8f4fd 100%)!important;box-shadow:0 0 0 3px #2a2a3a,0 0 0 6px #555,0 0 0 8px #2a2a3a,0 20px 60px rgba(0,0,0,.5)!important;padding:0!important;margin:0 auto!important;overflow-y:auto!important;overflow-x:hidden!important;position:relative!important;}
    .block-container::-webkit-scrollbar{width:0;display:none}

    .app-header{text-align:center;padding:8px 16px 4px;}
    .app-header h1{font-size:20px!important;font-weight:800!important;margin:0!important;background:linear-gradient(135deg,#ff6699,#ff9944,#cc66ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:-0.5px;}
    .app-header .subtitle{font-size:10px;color:#888;margin-top:2px;}

    .input-card{background:rgba(255,255,255,0.85);backdrop-filter:blur(10px);border-radius:16px;margin:8px 14px;padding:10px 14px 6px;box-shadow:0 2px 12px rgba(0,0,0,0.06);}
    .input-card label{font-size:12px;font-weight:700;color:#555;display:flex;align-items:center;gap:6px;margin-bottom:4px;}

    .recipe-card{background:#fff;border-radius:18px;margin:10px 14px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.08);}
    .recipe-card .recipe-img{width:100%;height:160px;object-fit:cover;}
    .recipe-card .recipe-body{padding:14px;}
    .recipe-card .recipe-title{font-size:15px;font-weight:800;color:#333;margin:0 0 8px;}
    .ingredient-pill{display:inline-block;background:#f0f9e8;color:#4a8c1c;border-radius:20px;padding:3px 10px;font-size:10px;margin:2px;font-weight:600;}
    .missed-pill{display:inline-block;background:#fff3e0;color:#e67e22;border-radius:20px;padding:3px 10px;font-size:10px;margin:2px;font-weight:600;}

    .twist-card{background:linear-gradient(135deg,#fdf6ff,#fff5f0);border-left:4px solid #cc66ff;border-radius:14px;margin:10px 14px;padding:14px 16px;}
    .twist-card .twist-label{font-size:11px;font-weight:800;color:#cc66ff;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;}
    .twist-card .twist-text{font-size:13px;color:#555;line-height:1.5;}

    .history-section{margin:12px 14px 20px;}
    .history-section h3{font-size:13px;font-weight:800;color:#666;margin:0 0 8px;}
    .history-item{background:rgba(255,255,255,0.8);border-radius:12px;padding:10px 12px;margin-bottom:8px;font-size:11px;color:#555;line-height:1.4;border:1px solid rgba(0,0,0,0.04);}
    .history-item strong{color:#333;}

    .stButton>button{width:calc(100% - 28px)!important;margin:0 14px!important;border-radius:14px!important;background:linear-gradient(135deg,#ff6699,#ff9944)!important;color:#fff!important;font-weight:700!important;font-size:15px!important;border:none!important;padding:12px 0!important;box-shadow:0 4px 15px rgba(255,102,153,0.4)!important;}
    .stButton>button:hover{background:linear-gradient(135deg,#ff5588,#ff8833)!important;color:#fff!important;}
    </style>
    """,
    unsafe_allow_html=True,
)

# App Header

st.markdown(
    """
    <div class="app-header">
        <h1>🍓 Culinary Oracle 🔮</h1>
        <div class="subtitle">Recipes based on your ingredients, mood & weather ✨</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Inputs

ingredients = st.text_input(" -- Ingredients ", placeholder="e.g. chicken, rice, garlic")
mood = st.selectbox("-- Mood ", ["Lazy 😴", "Romantic 💕", "Adventurous 🌍", "Healthy 🥦", "Comfort Food 🍲"])
weather = st.selectbox("-- Weather ", ["Rain 🌧️", "Snow ❄️", "Sunny ☀️", "Cloudy ☁️", "Fog 🌁", "Wind 💨", "Frost 🧊"])

# Session State

if "history" not in st.session_state:
    st.session_state.history = []

# Creative Twist Generator

def generate_twist(mood, weather):
    twists = {
        "Healthy 🥦": {
            "Rain 🌧️": "🥗 Make a light salad with citrus dressing to brighten the rainy mood.",
            "Snow ❄️": "🍵 Warm up with a veggie broth packed with nutrients.",
            "Sunny ☀️": "🍋 Serve chilled with lemon water.",
        },
        "Romantic 💕": {
            "Rain 🌧️": "🌹 Add rose petals and serve with candlelight.",
            "Snow ❄️": "☕ Serve with hot cocoa and a cozy blanket.",
            "Sunny ☀️": "🍷 Pair with chilled wine outdoors.",
        },
    }
    return twists.get(mood, {}).get(weather, f"✨ Add a creative touch for {weather.lower()} days!")

# Summon Recipes

summoned = st.button("✨ Summon Recipes 🍴", use_container_width=True)

if summoned:
    if ingredients:
        try:
            params = {"ingredients": ingredients, "number": 1, "apiKey": API_KEY}
            response = requests.get(BASE_URL, params=params)
            data = response.json()

            if response.status_code == 200 and data:
                recipe = data[0]
                used_pills = "".join(
                    f'<span class="ingredient-pill">{i["name"]}</span>'
                    for i in recipe["usedIngredients"]
                )
                missed_pills = "".join(
                    f'<span class="missed-pill">{i["name"]}</span>'
                    for i in recipe["missedIngredients"]
                )

                st.markdown(
                    f"""
                    <div class="recipe-card">
                        <img class="recipe-img" src="{recipe["image"]}" alt="{recipe["title"]}">
                        <div class="recipe-body">
                            <div class="recipe-title">🍽️ {recipe["title"]}</div>
                            <div style="margin-bottom:6px">
                                ✅ Ingredients used:<br>{used_pills}
                            </div>
                            <div>
                                ➕ Extra needed:<br>{missed_pills}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                twist = generate_twist(mood, weather)
                st.markdown(
                    f"""
                    <div class="twist-card">
                        <div class="twist-label">✨ Oracle's Creative Twist</div>
                        <div class="twist-text">{twist}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.session_state.history.append((ingredients, recipe["title"], mood, weather, twist))
            else:
                st.markdown(
                    '<div class="twist-card"><div class="twist-text" style="color:#e74c3c">No recipe found. Try different ingredients! 🔍</div></div>',
                    unsafe_allow_html=True,
                )
        except Exception as e:
            st.markdown(
                f'<div class="twist-card"><div class="twist-text" style="color:#e74c3c">Error: {e}</div></div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="twist-card"><div class="twist-text" style="color:#e67e22">Please enter some ingredients first! 📝</div></div>',
            unsafe_allow_html=True,
        )
        
# History

if st.session_state.history:
    history_html = '<div class="history-section"><h3>📜 Past Recipes</h3>'
    for ing, rec, mood_h, weather_h, twist_h in reversed(st.session_state.history[-5:]):
        history_html += (
            f'<div class="history-item">'
            f'<strong>{mood_h}</strong> · {weather_h}<br>'
            f'🍳 <strong>{rec}</strong> — {ing}<br>'
            f'✨ {twist_h}'
            f'</div>'
        )
    history_html += '</div>'
    st.markdown(history_html, unsafe_allow_html=True)

