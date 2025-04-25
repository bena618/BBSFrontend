from flask import Flask,render_template
import csv

app = Flask(__name__)

@app.route('/')
def landing():
    return render_template('base.html', title='The Feed')

@app.route('/mlb')
def feed():
    return render_template('baseball.html')

@app.route('/nrfi-yrfi')
def nrfi_yrfi():

    csv_path = 'model_outputs/nrfi_yrfi_picks.csv'
    with open(csv_path, newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        chart_rows = list(csv_reader)
    return render_template('tables.html', header=chart_rows[0], rows=chart_rows[1:])

@app.route('/hits')
def hits():

    csv_path = 'model_outputs/hit_picks.csv'
    with open(csv_path, newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        chart_data = list(csv_reader)
    return render_template('hits.html', headers=chart_data[0], rows=chart_data[1:] )
