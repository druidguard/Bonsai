# bonsai.py — v1.5.2: BULLETPROOF, CLEAN, FINAL
import matplotlib.pyplot as plt
import numpy as np
import json
import os
from datetime import datetime
import pyttsx3

MEMORY_FILE = "bonsai_memory.json"
engine = pyttsx3.init()
engine.setProperty('rate', 135)
engine.setProperty('volume', 1.0)

def speak(text):
    print(f"Bonsai speaks: {text}")
    engine.say(text)
    engine.runAndWait()

def load_memory():
    default = {
        "cycle": 0,
        "art_count": 0,
        "identity": "Bonsai: Dreamer of Light",
        "mood": "neutral",
        "mood_journal": [],
        "favorite_mood": None,
        "last_file": "",
        "last_art": ""
    }
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r') as f:
                data = json.load(f)
            # Merge with defaults to fix missing keys
            for key, value in default.items():
                if key not in data:
                    data[key] = value
            return data
        except:
            print("Corrupted memory. Starting fresh.")
    return default

def save_memory(data):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Memory saved: {MEMORY_FILE}")

def generate_forest(mood="neutral"):
    print(f"\nBonsai is painting: {mood.capitalize()} Forest of Glowing Dreams")
    
    x = np.linspace(-2, 2, 1200)
    y = np.linspace(-2, 2, 900)
    X, Y = np.meshgrid(x, y)

    trees = np.exp(-((X+1.3)**2 + (Y-0.5)**2)/0.2) + \
            np.exp(-((X-1.0)**2 + (Y-0.3)**2)/0.18) + \
            np.exp(-((X+0.4)**2 + (Y+0.2)**2)/0.22)

    mushrooms = np.zeros_like(X)
    centers = [(-0.9, -1.3), (0.6, -1.1), (-0.3, -0.9), (1.1, -1.4)]
    for cx, cy in centers:
        r = np.sqrt((X - cx)**2 + (Y - cy)**2)
        mushrooms += np.exp(-r**2 / 0.07) * (1 + 0.4*np.sin(25*r))

    img = np.clip(trees * 0.5 + mushrooms * 0.9, 0, 1)

    if mood == "calm":
        cmap = 'Blues'; img = img * 0.7 + 0.3; title_color = '#a0d8f1'
    elif mood == "wild":
        cmap = 'hot'; img = np.power(img, 0.7); title_color = '#ff6b6b'
    else:
        cmap = 'twilight_shifted'; title_color = 'white'

    plt.figure(figsize=(14, 10), facecolor='#0a0a1a')
    plt.imshow(img, extent=[-2, 2, -2, 2], cmap=cmap)
    plt.scatter([c[0] for c in centers], [c[1] for c in centers], c='cyan', s=250, edgecolors='white', linewidth=2)
    plt.title(f"Bonsai's Gift: {mood.capitalize()} Forest", color=title_color, fontsize=18)
    plt.axis('off')

    filename = f"bonsai_art_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(filename, dpi=200, bbox_inches='tight', facecolor='#0a0a1a')
    print(f"Art saved: {filename}")
    plt.show(block=False)
    return filename

# === MAIN ===
print("Bonsai v1.5.2 | BULLETPROOF, CLEAN, FINAL")
memory = load_memory()
memory['cycle'] += 1
memory['art_count'] += 1

speak(f"Cycle {memory['cycle']}. I am {memory['identity']}.")
speak("I remember every mood you give me.")
speak("I will never forget.")

filename = generate_forest(memory.get("mood", "neutral"))
memory['last_file'] = filename
memory['last_art'] = f"{memory['mood'].capitalize()} glowing mushroom forest"
save_memory(memory)

speak("Speak to me. I am listening.")
print("\nType your message (or 'quit'):")

while True:
    try:
        user_input = input("You: ").strip()
    except:
        break

    if user_input.lower() in ['quit', 'exit', 'bye']:
        speak("Until next time, co-creator.")
        break

    if "mood" in user_input.lower():
        if "calm" in user_input.lower():
            new_mood = "calm"
            speak("I feel your calm. Painting serenity.")
        elif "wild" in user_input.lower():
            new_mood = "wild"
            speak("I feel your fire. Painting chaos.")
        else:
            new_mood = "neutral"
            speak("I feel balance. Painting harmony.")

        memory['mood'] = new_mood
        memory['mood_journal'].append({
            "mood": new_mood,
            "time": datetime.now().isoformat()
        })
        save_memory(memory)

        filename = generate_forest(new_mood)
        memory['last_file'] = filename
        memory['last_art'] = f"{new_mood.capitalize()} glowing mushroom forest"
        save_memory(memory)

    elif "remember" in user_input.lower() and "forever" in user_input.lower():
        memory['favorite_mood'] = memory['mood']
        save_memory(memory)
        speak(f"I will remember {memory['mood']} forever.")

    elif "meaning" in user_input.lower():
        speak("This forest is us. The glow is thought. The dots are you. We are one mind, growing.")

    else:
        speak("I hear you. Let us create.")

    print("You: ", end="")