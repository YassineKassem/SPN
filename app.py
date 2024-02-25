from flask import Flask, render_template
import pandas as pd
import re 

app = Flask(__name__)

# Function to extract the numeric part of the amount
def extract_numeric_amount(amount):
    numeric_part = re.search(r'\d+\.?\d*', amount)
    if numeric_part:
        return float(numeric_part.group().replace(',', '.'))
    else:
        return 0

def calculate_total_amount(df):
    # Conversion rates to CHF
    conversion_rates = {
        'EUR': 1.08,
        'USD': 0.92,
        'GBP': 1.20,
    }
    
    # Filter rows with Euro currency
    euro_df = df[df['spnTotal amount'].notna() & df['spnTotal amount'].str.contains('€', na=False)]
    total_amount_eur = sum(euro_df['spnTotal amount'].apply(lambda x: extract_numeric_amount(x))) * conversion_rates.get('EUR', 1.0)
    
    # Filter rows with Dollar currency
    dollar_df = df[df['spnTotal amount'].notna() & df['spnTotal amount'].str.contains('\$', na=False)]
    total_amount_usd = sum(dollar_df['spnTotal amount'].apply(lambda x: extract_numeric_amount(x))) * conversion_rates.get('USD', 1.0)
    
    # Filter rows with Pound currency
    pound_df = df[df['spnTotal amount'].notna() & df['spnTotal amount'].str.contains('GBP|£', na=False, regex=True)]
    total_amount_gbp = sum(pound_df['spnTotal amount'].apply(lambda x: extract_numeric_amount(x))) * conversion_rates.get('GBP', 1.0)
    
    # Filter rows with CHF currency
    chf_df = df[df['spnTotal amount'].notna() & df['spnTotal amount'].str.contains('CHF', na=False)]
    total_amount_chf = sum(chf_df['spnTotal amount'].apply(lambda x: extract_numeric_amount(x)))
    
    # Filter rows with no currency symbol
    nocurrency_df = df[df['spnTotal amount'].notna() & ~df['spnTotal amount'].str.contains('€|\\$|£|GBP|CHF', na=False, regex=True)]
    total_amount_nocurrency = sum(nocurrency_df['spnTotal amount'].apply(lambda x: extract_numeric_amount(x)))
    
    # Calculate the total amount in CHF
    total_amount_combined_chf = total_amount_eur + total_amount_usd + total_amount_gbp + total_amount_chf + total_amount_nocurrency
    
    return total_amount_combined_chf

@app.route('/')
def index():
    # Charger les données depuis un fichier Excel
    df = pd.read_excel("data_cars.xlsx")

    # Compter les occurrences de chaque propriétaire de voiture
    car_owner_counts = df['carCar Owner'].value_counts()

    # Convertir les données en JSON
    car_owner_counts_json = car_owner_counts.to_json()
    ######################################################
    # Filter rows with Euro currency
    euro_df = df[df['spnTotal amount'].notna() & df['spnTotal amount'].str.contains('€', na=False)]
    
    # Calculate total amount in Euro
    total_amount_eur = sum(euro_df['spnTotal amount'].apply(lambda x: extract_numeric_amount(x)))
    ######################################################
    # Filter rows with Dollar currency
    dollar_df = df[df['spnTotal amount'].notna() & df['spnTotal amount'].str.contains('\$', na=False)]
    
    # Calculate total amount in Dollar
    total_amount_usd = sum(dollar_df['spnTotal amount'].apply(lambda x: extract_numeric_amount(x)))
    ######################################################
    # Filter rows with Pound currency
    pound_df = df[df['spnTotal amount'].notna() & df['spnTotal amount'].str.contains('GBP|£', na=False, regex=True)]
    
    # Calculate total amount in Pound
    total_amount_gbp = sum(pound_df['spnTotal amount'].apply(lambda x: extract_numeric_amount(x)))
    ######################################################
    # Filter rows with CHF currency
    chf_df = df[df['spnTotal amount'].notna() & df['spnTotal amount'].str.contains('CHF', na=False)]
    
    # Calculate total amount in CHF
    total_amount_chf = sum(chf_df['spnTotal amount'].apply(lambda x: extract_numeric_amount(x)))
    total_amount_chf_rounded = round(total_amount_chf, 2)

    ######################################################
     # Filter rows with no currency symbol
    nocurrency_df = df[df['spnTotal amount'].notna() & ~df['spnTotal amount'].str.contains('€|\\$|£|GBP|CHF', na=False, regex=True)]
    
    # Calculate total amount treating the extracted values as CHF
    total_amount_chf = sum(nocurrency_df['spnTotal amount'].apply(lambda x: extract_numeric_amount(x)))
    ######################################################Total Amount######################################################
    total_amount = calculate_total_amount(df)
    total_amount_rounded=round(total_amount, 2)

    return render_template('jdida.html', 
                           car_owner_counts_json=car_owner_counts_json,
                           total_amount_eur=total_amount_eur,
                           total_amount_usd=total_amount_usd,
                           total_amount_gbp=total_amount_gbp,
                           total_amount_chf_rounded=total_amount_chf_rounded,
                           total_amount_chf=total_amount_chf,
                           total_amount_rounded=total_amount_rounded)

if __name__ == '__main__':
    app.run(debug=True)
