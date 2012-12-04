from flask import Flask, render_template
from searching import searcher
from suggestor import suggestor

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/search/<keywords>')
def search(keywords):
    return searcher(keywords)

@app.route('/suggest/<keywords>')
def suggest(keywords):
    return suggestor(keywords)