from flask import Flask, request, render_template
from Cometa import cometa_process

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file1 = request.files['stock.csv']
        file2 = request.files['VANZARI.csv']
        # run the processing script in the background
        cometa_process(file1, file2)
        return "Processing the files in the background..."
    return render_template('index.html')

@app.route('/download')
def download_file():
    # get the path to the processed CSV file
    output_file = "output.csv"
    # send the file to the user as a downloadable attachment
    return send_file(output_file, as_attachment=True)

app.run(host='0.0.0.0', port=8080)