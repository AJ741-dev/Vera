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

# ----- Streamlit UI -----
st.set_page_config(page_title="VERA Check-In", layout="centered")
st.title("🧠 VERA - Daily Check-In")

st.write("How are you feeling today?")
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
