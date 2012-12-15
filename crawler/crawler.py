import os
import re
import urllib2
import urlparse
from bs4 import BeautifulSoup

SEEDS_FILE = "seeds"    # URLs to begin with
IGNORE_FILE = "ignore"  # ignore URLs matching reg patterns defined in the file
LOGS_FILE = "/tmp/instant-search/logs"      # log visited URLs and where files were saved
SAVE_TO = "/tmp/instant-search/"      # where the htmls save to

class SimpleCrawler(object):
    """ Simple Crawler by Heliumchen """
    def __init__(self, seedsFilePath, ignoreFilePath, logsFilePath, saveTo):
        super(SimpleCrawler, self).__init__()
        try:
            self.unvisitedURLs = self._initSeeds(seedsFilePath)
            self.ignorePatterns = self._initIgnore(ignoreFilePath)
            self.visitedURLs = self._initLogs(logsFilePath)
            self.logsFilePath = logsFilePath
            self.newLogs = ""
            self.saveTo = saveTo
            self.nextFileId = 0
            self.logCount = 0
        except Exception as e:
            print "Can't initialize SimpleCrawler: ", e
            exit()

    def _initSeeds(self, path):
        seedURLs = []
        with open(path, 'r') as f:
            url = f.readline()
            while url:
                seedURLs.append(url.strip())
                url = f.readline()

        print "Loaded %d seed URLs" % len(seedURLs)
        return seedURLs

    def _initIgnore(self, path):
        ignorePatterns = []
        with open(path, 'r') as f:
            reg = f.readline()
            while reg:
                ignorePatterns.append(re.compile(reg.strip()))
                reg = f.readline()

        print "Loaded %d ignore patterns" % len(ignorePatterns)
        return ignorePatterns

    def _initLogs(self, path, sepToken = "  "):
        visitedURLs = {}
        with open(path, 'r') as f:
            line = f.readline()
            while line.strip():
                url, filePath = line.split(sepToken)
                url = url.strip()
                visitedURLs[url] = filePath
                line = f.readline()

        print "Loaded logs"
        return visitedURLs

    def _log(self, url, fildId, sepToken = "  "):
        self.newLogs += url + sepToken + fildId + '\n'
        self.logCount += 1
        print self.logCount
        if self.logCount > 10:
            with open(self.logsFilePath, 'a') as f:
                f.write(self.newLogs)

            self.newLogs = ""
        return 0

    def _getURLValidator(self):
        ''' get a complied regex for url validation '''
        regex = re.compile(r'^(?:http|ftp)s?://(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|localhost|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?(?:/?|[/?]\S+)$', re.IGNORECASE)
        return regex

    def start(self):
        validator = self._getURLValidator()

        while len(self.unvisitedURLs) > 0:
            url = self.unvisitedURLs.pop()

            if (validator.match(url)):
                host = urlparse.urlparse(url)[0] + "://" + urlparse.urlparse(url)[1]

                try:
                    content = self._fetch(url)
                    self.visitedURLs[url] = self._saveFile(content)
                    self._log(url, self.visitedURLs[url])

                    self._parseURLs(content, host)
                    # print "host = ", host
                    # print "logs = ", self.newLogs
                    # raw_input("Press any Key to continue...")
                except Exception as e:
                    print "ERROR: ", e, ' when handling ', url
                    print "We will ignore this url"
            else:
                print "ERROR: not a valid url string - %s" % url

    def _fetch(self, url):
        ''' fire a HTTP request to fetch a HTML file '''
        f = urllib2.urlopen(url, timeout = 3)
        content = f.read()
        return content

    def _parseURLs(self, htmlDoc, baseURL):
        ''' parse valid URLs from the given file '''
        soup = BeautifulSoup(htmlDoc)
        tags = soup('a')
        for tag in tags:
            href = tag.get("href")
            if href is not None:
                # FIXME: need escape or urlencode?
                # add http:// by default?
                url = urlparse.urljoin(baseURL, href)
                tmp = urlparse.urlparse(url)
                url = tmp.scheme + "://" + tmp.netloc + tmp.path # remove query string

                if url[-1:] == "/":
                    url = url[:-1]
                # print "base url = ", baseURL
                # print "href = ", href
                # print "url = ", url
                # not in visitedURLs and not match any ignore patterns
                # print self._isURLIgnored(url)
                if url not in self.visitedURLs and url not in self.unvisitedURLs and not self._isURLIgnored(url):
                    self.unvisitedURLs.append(url)
        return 0

    def _isURLIgnored(self, url):
        for reg in self.ignorePatterns:
            if reg.search(url):
                return True
        return False

    def _saveFile(self, content):
        # get file name
        fileName = self._getNextFileName()
        with open(self.saveTo + fileName + '.html', 'w') as f:
            f.write(content)

        return fileName

    def _getNextFileName(self):
        # TODO: detect what id to start with
        self.nextFileId += 1
        return str(self.nextFileId)

if __name__ == "__main__":
    crawler = SimpleCrawler(SEEDS_FILE, IGNORE_FILE, LOGS_FILE, SAVE_TO)
    crawler.start()
