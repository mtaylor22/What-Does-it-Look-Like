import praw
import urllib2
import urllib
import simplejson
import re
import time
import os

def getFirst(query):
	url = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&'+urllib.urlencode({'q': query}))
	request = urllib2.Request(url, None, {})
	response = urllib2.urlopen(request)
	results = simplejson.load(response)
	if results['responseData']['results']:
		return results['responseData']['results'][0]
	else:
		return ''

def checkResponses(comment):
	for reply in comment.replies:
		if reply.author.name == 'wdill_bot':
			return False
	return True

r = praw.Reddit(user_agent='wdill_bot 0.1')
r.login(os.environ['ruser'], os.environ['rpass'])

def handle(target, comment, term):
	first = getFirst(target)
	if checkResponses(comment):
		if first:
			response =  first['unescapedUrl']
			try:
				comment.reply('['+term+' might look something like this.](' + response + ')')
				print 'Replied to ' + comment.id
				return True
			except praw.errors.RateLimitExceeded:
				print 'Rate Limit Exceeded, can\'t reply'
		else:
			print 'No results for ' + target
	else:
		print 'Already replied to ' + comment.id
	hit.add(comment.id)
	return False

def handleIt(comment):
	if comment.id not in hit and reg_it.match(comment.body.lower()):
		if comment.is_root:
			return handle(comment.submission.title, comment, 'It')
		else:
			return handle(r.get_info(thing_id=comment.parent_id).body, comment, 'It')
	return False

def handleThey(comment):
	if comment.id not in hit and reg_they.match(comment.body.lower()):
		if comment.is_root:
			return handle(comment.submission.author.name, comment, 'They')
		else:
			return handle(r.get_info(thing_id=comment.parent_id).author.name, comment, 'They')
	return False

def handleI(comment):
	if comment.id not in hit and reg_i.match(comment.body.lower()):
		return handle(comment.author.name, comment, "You")
	return False

hit = set()
s = r.get_subreddit('test')
comments = s.get_comments()
rex_it = 'what(s|\'s)? ?(does|did|will|would)? ?(it|that|this) look like\??'
rex_they = 'what(s|\'s)? ?(does|did|will|would)? ?(they|he|she) look like\??'
rex_i = 'what(s|\'s)? ?(does|did|will|would)? ?(i) look like\??'
reg_it = re.compile(rex_it)
reg_they = re.compile(rex_they)
reg_i = re.compile(rex_i)
while True:
	comments = s.get_comments()
	for comment in comments:
		if handleIt(comment):
			print 'Handled "it" item'
		elif handleThey(comment):
			print 'Handled "them" item'
		elif handleI(comment):
			print 'Handled "I" item'
	time.sleep(5)
