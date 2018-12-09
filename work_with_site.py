import urllib

def get_html(url):
	print(url)
	f = urllib.urlopen(url)
	s = f.read()
	f.close()
	return s
