from index import add_document

LOG_PATH = '/tmp/instant-search/logs'
DIR = '/tmp/instant-search/'
lists = []

with open(LOG_PATH) as f:
    line = f.readline()
    while line.strip():
        url, filePath = line.split('  ')
        url = url.strip()
        lists.append((url, DIR + filePath + '.html'))
        line = f.readline()

for url, path in lists:
    f = open(path)
    add_document(url, f.read())