import praw
import urllib2
import urllib
import simplejson

def getFirst(query):
	url = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&'+urllib.urlencode({'q': query}))
	request = urllib2.Request(url, None, {})
	response = urllib2.urlopen(request)

	# Process the JSON string.
	results = simplejson.load(response)
	first = results['responseData']['results'][0]
	return first




# Thanks
# http://amertune.blogspot.com/2014/04/tutorial-create-reddit-bot-with-python.html
r = praw.Reddit(user_agent='wdill_bot 0.1')
r.login(os.environ['ruser'], os.environ['rpass'])

while True:
    for submission in r.get_subreddit('learnpython').get_hot(limit=5):
        print(submission)
    time.sleep(30)

print getFirst('marmalade')['unescapedUrl']