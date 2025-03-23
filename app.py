import streamlit as st
import json
from datetime import datetime
import random

# ----- Memory File Setup -----
MEMORY_FILE = "vera_memory.json"

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_memory(data):
    memory = load_memory()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    memory[timestamp] = data
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)

# ----- Tone Templates -----
TONE_PROFILES = {
    "calm": [
        "You're centered. Keep breathing and stay focused on {focus}.",
        "Peaceful energy today. Let’s carry that into your focus: {focus}"
    ],
    "hype": [
        "Let’s gooo! Big energy. Stay locked in on {focus} today!",
        "You’re on fire — keep that momentum and crush your focus: {focus}"
    ],
    "therapist": [
        "Let’s take it slow. I hear you. We’ll stay grounded in {focus} today.",
        "That’s okay — we’ll work through it. Just return to your focus: {focus}"
    ],
    "default": [
        "Thanks for checking in. Let’s stay mindful of {focus} today.",
        "Got it. Keep {focus} in view, and let’s take it one step at a time."
    ]
}

MOOD_TO_TONE = {
    "Calm": "calm",
    "Anxious": "therapist",
    "Motivated": "hype",
    "Tired": "therapist",
    "Excited": "hype",
    "Focused": "default"
}

# ----- Streamlit UI + Mood Visuals -----

mood_colors = {
    "Calm": "#d3ecff",
    "Anxious": "#ede5ff",
    "Motivated": "#fff6cc",
    "Tired": "#e6e6e6",
    "Excited": "#ffe4ec",
    "Focused": "#d5f7f1"
}
st.set_page_config(page_title="VERA Check-In", layout="centered")
st.markdown("""
    <style>
    body {
        background-color: #f5f5f5;
        transition: background-color 2s ease-in-out;
        transition: background-color 0.5s ease;
    }
    .mood-ring {
        transition: background 1s ease, background-color 1s ease;
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin: auto;
        margin-bottom: 10px;
        box-shadow: 0 0 20px 8px rgba(0,0,0,0.1);
        animation: pulse 4s infinite ease-in-out;
    }
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0px 0px rgba(0,0,0,0.05), 0 0 30px 10px rgba(0,0,0,0.1);
            transform: scale(1);
        }
        50% {
            box-shadow: 0 0 40px 20px rgba(0,0,0,0.08), 0 0 60px 30px rgba(0,0,0,0.05);
            transform: scale(1.1);
        }
        100% {
            box-shadow: 0 0 0px 0px rgba(0,0,0,0.05), 0 0 30px 10px rgba(0,0,0,0.1);
            transform: scale(1);
        }
    }
    }
    .calm {
        transition: background 1s ease, background-color 1s ease;
        background: radial-gradient(circle, #a3d5ff, #5caeff);
        background-color: #d3ecff !important;
        transition: background-color 2s ease-in-out;
    }
    .anxious {
        transition: background 1s ease, background-color 1s ease;
        background: radial-gradient(circle, #d6ccff, #a48bf2);
        background-color: #ede5ff !important;
        transition: background-color 2s ease-in-out;
    }
    .motivated {
        transition: background 1s ease, background-color 1s ease;
        background: radial-gradient(circle, #ffe49e, #f5b700);
        background-color: #fff6cc !important;
        transition: background-color 2s ease-in-out;
    }
    .tired {
        transition: background 1s ease, background-color 1s ease;
        background: radial-gradient(circle, #ccc, #999);
        background-color: #e6e6e6 !important;
        transition: background-color 2s ease-in-out;
    }
    .excited {
        transition: background 1s ease, background-color 1s ease;
        background: radial-gradient(circle, #ffc0cb, #ff69b4);
        background-color: #ffe4ec !important;
        transition: background-color 2s ease-in-out;
    }
    .focused {
        transition: background 1s ease, background-color 1s ease;
        background: radial-gradient(circle, #94e0d1, #2c8d85);
        background-color: #d5f7f1 !important;
        transition: background-color 2s ease-in-out;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧠 VERA - Daily Check-In")

# Background container simulation

st.write("How are you feeling today?")
mood = st.selectbox("Mood", list(MOOD_TO_TONE.keys()))
selected_bg = mood_colors.get(mood, "#f5f5f5")
st.markdown(f"""
    <div style='background-color: {selected_bg}; padding: 20px; border-radius: 10px;'>
    <!-- Removed the SVG ripple to simplify the mood ring -->
<div class="mood-ring {mood.lower()} mood-wave"></div>
""", unsafe_allow_html=True)
focus = st.text_input("What’s your focus today?")
note = st.text_area("Anything on your mind?")

if st.button("Submit Check-In"):
    tone = MOOD_TO_TONE.get(mood, "default")
    response = random.choice(TONE_PROFILES[tone]).format(focus=focus)

    reflection = {
        "mood": mood.lower(),
        "focus": focus,
        "note": note,
        "tone": tone
    }
    save_memory(reflection)

    st.success("✅ VERA heard you.")
    st.markdown(f"**VERA ({tone}):** {response}")

st.markdown("</div>", unsafe_allow_html=True)

# Optional: Display recent memory
with st.expander("📝 Recent Check-Ins"):
    memory = load_memory()
    sorted_entries = sorted(memory.items(), reverse=True)[0:5]
    for timestamp, entry in sorted_entries:
        st.markdown(f"**{timestamp}** — Mood: {entry['mood'].capitalize()}, Focus: {entry['focus']}  ")
        st.markdown(f"*{entry['note']}*  ")
        st.markdown(f"Tone: `{entry['tone']}`")
    
