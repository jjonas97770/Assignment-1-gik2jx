from flask import Flask, render_template, jsonify, request
import json
import os
import csv
import math
import random

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

# Läser school_locs.csv och skickar innehållet som JSON
# till webbläsaren när JavaScript anropar fetch('/schools')


@app.route('/schools')
def schools():
    filväg = os.path.join(app.static_folder, 'school_locs.csv')
    skolor = []
    with open(filväg, 'r', encoding='utf-8') as f:
        läsare = csv.DictReader(f)
        for rad in läsare:
            skolor.append({
                'name': rad['Name'],
                'lat':  float(rad['ycoord']),
                'lng':  float(rad['xcoord'])
            })
    return jsonify(skolor)

# Tar emot koordinater och antal kluster (k) från webbläsaren,
# utför k-means klustring och returnerar vilket kluster
# varje punkt tillhör samt centroidernas positioner


@app.route('/kmeans', methods=['POST'])
def kmeans():
    data = request.get_json()
    punkter = data['punkter']
    k = data['k']

    koordinater = [[p['lat'], p['lng']] for p in punkter]
    etiketter, centroids = kör_kmeans(koordinater, k)
    return jsonify({'etiketter': etiketter, 'centroids': centroids})


def kör_kmeans(koordinater, k, max_iter=100):
    '''
    Implementering av k-means algoritmen.

    Steg 1: Välj k slumpmässiga startpunkter som centroids.
    Steg 2: Tilldela varje punkt till närmaste centroid.
    Steg 3: Flytta varje centroid till medelvärdet av sina punkter.
    Steg 4: Upprepa steg 2-3 tills ingenting förändras.
    '''
    random.seed(42)
    centroids = random.sample(koordinater, k)
    etiketter = [0] * len(koordinater)

    for _ in range(max_iter):
        nya_etiketter = []

        for punkt in koordinater:
            avstånd = [euklidiskt_avstånd(punkt, c) for c in centroids]
            nya_etiketter.append(avstånd.index(min(avstånd)))

        if nya_etiketter == etiketter:
            break

        etiketter = nya_etiketter

        for ki in range(k):
            kluster_punkter = [koordinater[i]
                               for i, e in enumerate(etiketter) if e == ki]
            if kluster_punkter:
                centroids[ki] = [
                    sum(p[0] for p in kluster_punkter) / len(kluster_punkter),
                    sum(p[1] for p in kluster_punkter) / len(kluster_punkter)
                ]

    return etiketter, centroids


def euklidiskt_avstånd(a, b):
    '''
    Beräknar det euklidiska avståndet mellan två koordinatpar.
    Används av k-means för att hitta närmaste centroid.
    '''
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


if __name__ == '__main__':
    app.run(debug=True)
