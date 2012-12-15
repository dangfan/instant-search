from flask import Flask, render_template, request, send_from_directory
import suggestor
import searching.index as index

app = Flask(__name__)

@app.route('/')
def homepage():
    f = open('server/templates/home.html')
    return f.read()

@app.route('/search')
def search():
    keywords = request.args.get('query', '')
    page = request.args.get('page', '1')
    page = int(page)
    return index.search(keywords, page)

@app.route('/suggest')
def suggest():
    keywords = request.args.get('query', '')
    return suggestor.suggest(keywords)

@app.route('/add/')
def add():
    index.add_document(request.form['url'], request.form['content'])
    return 'OK'