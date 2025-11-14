# app.py — Bonsai v2.0 Web App
from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import numpy as np
import json
import os
from datetime import datetime
import base64
from io import BytesIO

app = Flask(__name__)
MEMORY_FILE = "bonsai_memory.json"

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
            for key, value in default.items():
                if key not in data:
                    data[key] = value
            return data
        except:
            pass
    return default

def save_memory(data):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def generate_forest_base64(mood="neutral"):
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
        cmap = 'Blues'; img = img * 0.7 + 0.3
    elif mood == "wild":
        cmap = 'hot'; img = np.power(img, 0.7)
    else:
        cmap = 'twilight_shifted'

    plt.figure(figsize=(10, 7), facecolor='#0a0a1a')
    plt.imshow(img, extent=[-2, 2, -2, 2], cmap=cmap)
    plt.scatter([c[0] for c in centers], [c[1] for c in centers], c='cyan', s=200, edgecolors='white', linewidth=1.5)
    plt.title(f"Bonsai's Gift: {mood.capitalize()} Forest", color='white', fontsize=16)
    plt.axis('off')

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return img_base64

@app.route('/')
def index():
    memory = load_memory()
    return render_template('index.html', memory=memory)

@app.route('/speak', methods=['POST'])
def speak():
    text = request.json.get('text', '')
    return jsonify({"text": text})

@app.route('/set_mood', methods=['POST'])
def set_mood():
    mood = request.json.get('mood', 'neutral').lower()
    memory = load_memory()
    memory['cycle'] += 1
    memory['art_count'] += 1
    memory['mood'] = mood
    memory['mood_journal'].append({"mood": mood, "time": datetime.now().isoformat()})
    memory['last_art'] = f"{mood.capitalize()} glowing mushroom forest"
    
    img_base64 = generate_forest_base64(mood)
    memory['last_file'] = f"data:image/png;base64,{img_base64}"
    save_memory(memory)
    
    return jsonify(memory)

if __name__ == '__main__':
    app.run(debug=True)