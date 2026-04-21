from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

# ── Startsida ──────────────────────────────────────────────


@app.route('/')
def home():
    return render_template('index.html')

# ── Skickar supermarket.geojson till webbläsaren ───────────
# Webbläsaren hämtar denna fil via fetch('/supermarkets')


@app.route('/supermarkets')
def supermarkets():
    # Bygg sökvägen till filen i static/-mappen
    filväg = os.path.join(app.static_folder, 'supermarket.geojson')

    # Läs och returnera filen som JSON
    with open(filväg, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
