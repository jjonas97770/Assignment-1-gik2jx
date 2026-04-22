from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

# Startsida – laddar index.html från templates-mappen


@app.route('/')
def home():
    return render_template('index.html')

# Skickar supermarket.geojson till webbläsaren när
# JavaScript anropar fetch('/supermarkets')


@app.route('/supermarkets')
def supermarkets():
    filväg = os.path.join(app.static_folder, 'supermarket.geojson')
    with open(filväg, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

# Skickar fuel.geojson till webbläsaren när
# JavaScript anropar fetch('/fuel')


@app.route('/fuel')
def fuel():
    filväg = os.path.join(app.static_folder, 'fuel.geojson')
    with open(filväg, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
