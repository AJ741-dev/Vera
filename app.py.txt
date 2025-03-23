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
st.set_page_config(page_title="VERA Check-In", layout="centered")
st.markdown("""
    <style>
    body {
        background-color: #f5f5f5;
        transition: background-color 0.5s ease;
    }
    .mood-ring {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin: auto;
        margin-bottom: 10px;
        box-shadow: 0 0 20px 8px rgba(0,0,0,0.1);
        animation: pulse 3s infinite ease-in-out;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 20px 8px rgba(0,0,0,0.05); }
        50% { box-shadow: 0 0 30px 15px rgba(0,0,0,0.15); }
        100% { box-shadow: 0 0 20px 8px rgba(0,0,0,0.05); }
    }
    .calm {
        background: radial-gradient(circle, #a3d5ff, #5caeff);
        background-color: #d3ecff !important;
    }
    .anxious {
        background: radial-gradient(circle, #d6ccff, #a48bf2);
        background-color: #ede5ff !important;
    }
    .motivated {
        background: radial-gradient(circle, #ffe49e, #f5b700);
        background-color: #fff6cc !important;
    }
    .tired {
        background: radial-gradient(circle, #ccc, #999);
        background-color: #e6e6e6 !important;
    }
    .excited {
        background: radial-gradient(circle, #ffc0cb, #ff69b4);
        background-color: #ffe4ec !important;
    }
    .focused {
        background: radial-gradient(circle, #94e0d1, #2c8d85);
        background-color: #d5f7f1 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧠 VERA - Daily Check-In")

st.write("How are you feeling today?")

# Mood ring visual based on selected mood
if 'mood' in locals():
    mood_class = mood.lower()
    st.markdown(f'<div class="mood-ring {mood_class}"></div>', unsafe_allow_html=True)
mood = st.selectbox("Mood", list(MOOD_TO_TONE.keys()))
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

# Optional: Display recent memory
with st.expander("📝 Recent Check-Ins"):
    memory = load_memory()
    sorted_entries = sorted(memory.items(), reverse=True)[0:5]
    for timestamp, entry in sorted_entries:
        st.markdown(f"**{timestamp}** — Mood: {entry['mood'].capitalize()}, Focus: {entry['focus']}  ")
        st.markdown(f"*{entry['note']}*  ")
        st.markdown(f"Tone: `{entry['tone']}`\n")
