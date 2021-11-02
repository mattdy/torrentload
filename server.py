# TorrentLoad v1.3.1
# 05/12/13
# Created by Matt Dyson
# mattdyson.org

# See mattdyson.org/projects/torrentload for more details

# Opens up a HTTP interface to which magnet details can be passed (via userscript from browser intercepting magnet: links)
# Details are then written in the form of a valid .torrent file to a watch folder for downloading

# Inspiration from:
#  - http://phill84.org/2009/12/rtorrent-with-magnet-link-support/comment-page-1/#comment-2608
#  - http://wiki.rtorrent.org/MagnetUri

# Version 1.3 - Updated 23/02/14
#   - Add secret key that is configured in browser plugin for security
# Version 1.3.1 - Updated 18/03/14
#   - Load secret key from file rather than hard-coding in here

import web
import urllib
import re

pat = re.compile('urn:btih:([^&/]+)')
magnetPath = "/home/matt/download/watch" # Watch directory for torrents
secret = '' # Secret key, entered into the configuration on the browser script, loaded from file in this directory called 'secret'

urls = (
    '/(.*)', 'magnet'
)
app = web.application(urls, globals())

class magnet:
    def GET(self, arg):
	query = web.input(tr=[])
	if not query.xt:
		return "Didn't recognise a magnet link"

	with open('secret', 'r') as f:
		secret = f.readline().rstrip()

	if not query.secret or query.secret!=secret:
		return "Secret key either not set, or didn't match"

	m = pat.search(query.xt)
	if not m:
		return "Couldn't find a valid hash"

	hash = m.group(1)

	magnet = "magnet:?xt={0}&dn={1}".format(query.xt,urllib.quote_plus(query.dn))

	for tracker in query.tr:
		magnet = "{0}&tr={1}".format(magnet,urllib.quote_plus(tracker))
	
	content = "d10:magnet-uri{0}:{1}e".format(len(magnet),magnet)

	return self.writeToFile(hash,content)


    def writeToFile(self, hash, value):
	path = "{0}/meta-{1}.torrent".format(magnetPath,hash)
	with open(path, 'w') as f:
		f.write(value)
	f.closed
	return "Writing to {0}".format(path)


if __name__ == "__main__":
    app.run()
