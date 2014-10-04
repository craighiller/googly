import time
import praw
from  imgur import *
r=praw.Reddit("Googly Bot")
def main():
	if(login()==-1):
		return -1
	scanSubreddit('all')
	
def login():
	try:
		r.login("googlybot", "bluebears")
	except:
		return -1
def scanSubreddit(subName):
	subreddit=r.get_subreddit(subName)
	for submission in subreddit.get_hot(limit=10):
		comments=praw.helpers.flatten_tree(submission.comments)
		return
		for comment in comments:
			if type(comment) is praw.objects.Comment and "/u/googlybot" in comment.body:
				if comment.is_root:
					handleRoot(comment, submission)
				else:
					handleNode(comment)
def handleRoot(comment, submission):
	if "imgur.com" not in submission.domain:
		postFail(comment)
		return
	imgurUrl=sub.url 
	newUrl = generateImgur(imgurUrl)
def handleNode(comment):
	pass
def postFail(comment):
	pass
main()