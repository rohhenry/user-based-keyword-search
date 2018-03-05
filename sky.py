import sys
import praw 
import badwords 
from colors import * 

subreddit = sys.argv[1]

del sys.argv[:2]

if not sys.argv:
	sys.argv = badwords.badwords
else:
	sys.argv = [s.lower() for s in sys.argv]

def search(redditor):
	search_count = 0 
	word_count = 0
	for comment in redditor.comments.new(limit=None):
		commentwords = comment.body.replace('.', '').lower().split(' ')

		word_count += len(commentwords)
		for searchword in sys.argv:
			if searchword in commentwords:
				search_count += 1
				colored_print('reddit.com' +  comment.permalink, RED)  
				colored_print(comment.body.replace(searchword, CYAN + searchword + BLUE), BLUE)
				print()
				input('Press Enter to Continue:')
	if not search_count:
		colored_print('{}, has never said these words in the {} words they have commented\n'.format(redditor.name, word_count), GREEN)
		return None
	colored_print('{}, search count: {}, words per search: {} total words: {}\n'.format(redditor.name, search_count, int(word_count/search_count), word_count), GREEN)


reddit = praw.Reddit(client_id='your reddit key ', 
			client_secret='your reddit key', 
			user_agent='python project info')


for submission in reddit.subreddit(subreddit).new(limit=None):
	try:
		search(submission.author)
	except AttributeError:
		pass
