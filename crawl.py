#for commandline arguments
import sys
#for reddit api
import praw 
#for optional search terms
import words 

#contains ANSI escape strings and functions for coloring output
from colors import * 

#takes a subreddit as a command line argument
subreddit = sys.argv[1]

del sys.argv[:2]

#if no other arguments are passed, it will search according to the wordlist other wise it will use sys.argv
if not sys.argv:
	sys.argv = words.searchwords

#lowercase the incoming search terms
else:
	sys.argv = [s.lower() for s in sys.argv]

#searches the past comments of a redditor printing out highlighted instances of search terms in their comments	
def search(redditor):
	search_count = 0 
	word_count = 0
	#iterate over the redditors comments
	for comment in redditor.comments.new(limit=None):
		#gets rid of periods and splits the comment into words
		commentwords = comment.body.replace('.', '').lower().split(' ')
		
		#increase total wordcount by the number of words
		word_count += len(commentwords)
		
		#searches for the searchwords in the comment
		for searchword in sys.argv:
			if searchword in commentwords:
				search_count += 1
				colored_print('reddit.com' +  comment.permalink, RED)  
				colored_print(comment.body.replace(searchword, CYAN + searchword + BLUE), BLUE)
				print()
				#comment out the line below if you want to speed things up
				input('Press Enter to Continue:')
	#returns with this clause if you cant find any instances of the words in any comment
	if not search_count:
		colored_print('{}, has never said these words in the {} words they have commented\n'.format(redditor.name, word_count), GREEN)
		return None
	#returns simple stats about user and their words
	colored_print('{}, search count: {}, words per search: {} total words: {}\n'.format(redditor.name, search_count, int(word_count/search_count), word_count), GREEN)

#get a reddit instance
reddit = praw.Reddit(client_id='your reddit key ', 
			client_secret='your reddit key', 
			user_agent='python project info')

#searches the subreddit for new posts and grabs the author's name to begin searching through their comment history
for submission in reddit.subreddit(subreddit).new(limit=None):
	try:
		search(submission.author)
	except AttributeError:
		pass
