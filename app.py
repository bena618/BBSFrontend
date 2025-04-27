from flask import Flask,render_template
import csv

app = Flask(__name__, static_folder='static', static_url_path='/')

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/mlb')
def feed():
    # Load NRFI/YRFI data
    with open('model_outputs/nrfi_yrfi_picks.csv', newline='') as f:
        nrfi_reader = csv.reader(f)
        nrfi_rows = list(nrfi_reader)
    nrfi_header = nrfi_rows[0]
    nrfi_data = nrfi_rows[1:]

    # Load Hits data
    with open('model_outputs/hit_picks.csv', newline='') as f:
        hits_reader = csv.reader(f)
        hits_rows = list(hits_reader)
    hits_header = hits_rows[0]
    hits_data = hits_rows[1:]

    # Similarly load other CSVs if needed

    return render_template('baseball.html',
                           nrfi_header=nrfi_header,
                           nrfi_data=nrfi_data,
                           hits_header=hits_header,
                           hits_data=hits_data)
@app.route('/nba')
@app.route('/nfl')
@app.route('/ncaaf')
@app.route('/nhl')
def comingsoon():
    return render_template('comingsoon.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404