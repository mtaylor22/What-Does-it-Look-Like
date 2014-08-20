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
		if comment.id not in hit and reg_it.match(comment.body.lower()):
			if comment.is_root:
				#get name of submission
				target = comment.submission.title
				first = getFirst(target)
				if checkResponses(comment):
					if first:
						response =  first['unescapedUrl']
						comment.reply('[It might look something like this.](' + response + ')')
						print 'Replied to ' + comment.id
					else:
						print 'No results for ' + target
				else:
					print 'Already replied to ' + comment.id
				hit.add(comment.id)
			else:
				#get content of parent
				target = r.get_info(thing_id=comment.parent_id).body
				first = getFirst(target)
				if checkResponses(comment):
					if first:
						response =  first['unescapedUrl']
						comment.reply('[It might look something like this.](' + response + ')')
						print 'Replied to ' + comment.id
					else:
						print 'No results for ' + target
				else:
					print 'Already replied to ' + comment.id
				hit.add(comment.id)
		elif comment.id not in hit and reg_they.match(comment.body.lower()):
			if comment.is_root:
				#get poster of submission
				target = comment.submission.author.name
				first = getFirst(target)
				if checkResponses(comment):
					if first:
						response =  first['unescapedUrl']
						comment.reply('[They might look something like this.](' + response + ')')
						print 'Replied to ' + comment.id
					else:
						print 'No results for ' + target
				else:
					print 'Already replied to ' + comment.id
				hit.add(comment.id)
			else:
				#get poster of parent
				target = r.get_info(thing_id=comment.parent_id).author.name
				first = getFirst(target)

				if checkResponses(comment):
					if first:
						response =  first['unescapedUrl']
						comment.reply('[They might look something like this.](' + response + ')')
						print 'Replied to ' + comment.id
					else:
						print 'No results for ' + target
				else:
					print 'Already replied to ' + comment.id
				hit.add(comment.id)
		elif comment.id not in hit and reg_i.match(comment.body.lower()):
			#get poster of parent
			target = comment.author.name
			first = getFirst(target)

			if checkResponses(comment):
				if first:
					response =  first['unescapedUrl']
					comment.reply('[You might look something like this.](' + response + ')')
					print 'Replied to ' + comment.id
				else:
					print 'No results for ' + target
			else:
				print 'Already replied to ' + comment.id
			hit.add(comment.id)
	time.sleep(5)
