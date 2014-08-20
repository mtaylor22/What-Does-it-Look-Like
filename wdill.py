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

class Wdill:
	def __init__(self):
		self.hit = set()
		self.rex_it = 'what(s|\'s)? ?(does|did|will|would)? ?(it|that|this) look like\??'
		self.rex_they = 'what(s|\'s)? ?(does|did|will|would)? ?(they|he|she) look like\??'
		self.rex_i = 'what(s|\'s)? ?(does|did|will|would)? ?(i) look like\??'
		self.reg_it = re.compile(self.rex_it)
		self.reg_they = re.compile(self.rex_they)
		self.reg_i = re.compile(self.rex_i)
		self.r = praw.Reddit(user_agent='wdill_bot 0.1')
		self.r.login(os.environ['ruser'], os.environ['rpass'])


	def checkResponses(self, comment):
		for reply in comment.replies:
			if reply.author.name == 'wdill_bot':
				return False
		return True

	def handle(self, target, comment, term):
		if self.checkResponses(comment):
			first = getFirst(target)
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
		self.hit.add(comment.id)
		return False

	def handleIt(self, comment):
		if comment.id not in self.hit and self.reg_it.match(comment.body.lower()):
			if comment.is_root:
				return self.handle(comment.submission.title, comment, 'It')
			else:
				return self.handle(self.r.get_info(thing_id=comment.parent_id).body, comment, 'It')
		return False

	def handleThey(self, comment):
		if comment.id not in self.hit and self.reg_they.match(comment.body.lower()):
			if comment.is_root:
				return self.handle(comment.submission.author.name, comment, 'They')
			else:
				return self.handle(self.r.get_info(thing_id=comment.parent_id).author.name, comment, 'They')
		return False

	def handleI(self, comment):
		if comment.id not in self.hit and self.reg_i.match(comment.body.lower()):
			return self.handle(comment.author.name, comment, "You")
		return False

	def scan(self):
		comments = self.r.get_comments('test')
		for comment in comments:
			if self.handleIt(comment):
				print 'Handled "it" item'
			elif self.handleThey(comment):
				print 'Handled "them" item'
			elif self.handleI(comment):
				print 'Handled "I" item'


wdill_bot = Wdill()		
while True:
	wdill_bot.scan()
	time.sleep(30)
