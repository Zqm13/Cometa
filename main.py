from flask import Flask, render_template, request, send_file
import pandas as pd
from Cometa import cometa_process

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_files', methods=['POST'])
def process_files():
    stock_file = request.files['stock']
    VANZARI_file = request.files['VANZARI']
    
    # Read CSV files
    stock = pd.read_csv(stock_file)
    vanzari = pd.read_csv(VANZARI_file)
    
    # Process CSV files
    result_df = cometa_process(stock, vanzari)
    
    # Save processed CSV file to disk
    result_df.to_csv('result.csv', index=False)
    
    return send_file('result.csv', as_attachment=True)

@app.route('/download_file')
def download_file():
    return send_file('result.csv', as_attachment=True)


app.run(host='0.0.0.0', port=8080)