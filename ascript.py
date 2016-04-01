import urllib
import json
import indicoio
import time
import sys
	
# u.s.
# world
# technology
# health
# nyregion
# politics
# sports
# arts
# science
# fashion
# travel
# opinion
# food
# section = "world"
sections = ["u.s.", "world", "technology", "health", "nyregion", "politics", "sports", "arts", "science", "fashion", "travel", "opinion", "food"]

# check if in debug mode:
debug = False
try:
	if sys.argv[1] == "debug":
		debug = True
except:
	debug = False


# get API keys:	
for line in open("api_keys/keys.txt", "r"):
	line = line.strip()
	words = line.split()
	if words[0] == "indico":
		indico_key = words[1]
	if words[0] == "nytimes":
		nytimes_key = words[1]

#to get terminal width and print centered:
# from here: http://stackoverflow.com/a/566752
def getTerminalSize():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

    return int(cr[1]), int(cr[0])

(width, height) = getTerminalSize()


# start indico api
indicoio.config.api_key = indico_key


for section in sections:
	# get the abstract of mostviewed nytimes articles
	url = "http://api.nytimes.com/svc/mostpopular/v2/mostviewed/" + section + "/1.json?api-key=" + nytimes_key
	plainData = urllib.urlopen(url).read()
	data = json.loads(plainData)

	# print out the header
	print "\n"*height
	the_date = time.strftime("%B") + " " + time.strftime("%d") + " " + time.strftime("%Y") + ", " + time.strftime("%X")
	header = "The *" + section.upper() + "* News of the Day - A Worst Of"
	print header.center(width, ' ')
	print "-".center(width, ' ')
	print the_date.center(width, ' ')
	print "\n"*2

	# the actual code:
	lastLineText = False
	for r in data["results"]:
		# print r["abstract"]
		words = r["abstract"].split()
		s = list()
		for i in range(len(words)):
			enough = True 
			try:
				# print words[i], words[i + 1], words[i + 2]
				nw = [words[i], words[i + 1], words[i + 2], words[i + 3]]
				nw = " ".join(nw)
				if "&#" in nw:
					enough = False
			except:
				enough = False
			if enough:
				# print nw
				s.append(nw)
		
		# print s
		sel_w = ""
		lowest = 1
		for w in s:
			i = indicoio.sentiment(w, version=1)
			if i < lowest:
				lowest = i
				sel_w = w
		if lowest <  0.1:
			print sel_w.center(width, ' ')
			if(debug): print str(lowest)
			lastLineText = True
		else:
			if(lastLineText):
				print ""
				lastLineText = False
			if(debug): print sel_w
			if(debug): print str(lowest)

	print "\n"*3
print "\n"*(int(round(height/2)))
