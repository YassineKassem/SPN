from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Charger les données depuis un fichier Excel
    df = pd.read_excel("data_cars.xlsx")

    # Compter les occurrences de chaque propriétaire de voiture
    car_owner_counts = df['carCar Owner'].value_counts()

    # Convertir les données en JSON
    car_owner_counts_json = car_owner_counts.to_json()

    return render_template('index.html', car_owner_counts_json=car_owner_counts_json)

if __name__ == '__main__':
    app.run(debug=True)
