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
	for comment in subreddit.get_comments(limit=None):
		if type(comment) is praw.objects.Comment and "/u/googlybot" in comment.body:
			if comment.is_root:
				handleRoot(comment)
			else:
				handleNode(comment)
def handleRoot(comment):
	sub=r.get_info(thing_id=comment.parent_id)
	if "imgur.com" not in sub.domain:
		postFail(comment)
		return
	for child in comment.replies:
		if child.author==r.user:
			return
	imgurUrl=sub.url 
	newUrl = generateImgur(imgurUrl)
	postComment(comment, newUrl)
def handleNode(comment):
	parent=r.get_info(thing_id=comment.parent_id)
	for child in parent.replies:
		if child.author==r.user:
			return
	for word in parent.body.split():
		if 'imgur.com' in word:
			word=str(word)
			newUrl=generateImgur(word)
			postComment(comment, newUrl)
def postFail(comment):
	pass
def postComment(comment, url):
	comment.reply(url)
	#main()