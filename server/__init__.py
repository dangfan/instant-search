from flask import Flask, render_template, request
import suggestor
import searching.index as index

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/search/<keywords>')
@app.route('/search/<keywords>/<page>')
def search(keywords, page=1):
    page = int(page)
    return index.search(keywords, page)

@app.route('/suggest/<keywords>')
def suggest(keywords):
    return suggestor.suggest(keywords)

@app.route('/add/')
def add():
    index.add_document(request.form['url'], request.form['content'])
    return 'OK'