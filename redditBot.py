import time
import praw
from  imgur import *
r=praw.Reddit("Googly Bot")

def main():
	if(login()==-1):
		return -1
	i=0
	while True:
		x=time.time()
		print i
		i+=1
		try:
			print int(time.time()/60)
			scanSubreddit('all')
		except:
			print "Failed"
		y=time.time()
		waittime=60-y+x
		print "waiting"
		print waittime
		if waittime>0:
			time.sleep(waittime+1)
	
def login():
	try:
		r.login("googlybot", "bluebears")
	except:
		return -1
login()
myName=r.user
def scanSubreddit(subName):
	subreddit=r.get_subreddit(subName)
	iterator = subreddit.get_new(limit=400)
	counter=0
	iterator.next()
	for submission in iterator:
		newUrl=submission.url
	#	counter+=1
	#	if counter==4:
	#		counter = 0
		print submission
		if ".png" in newUrl or ".jpg" in newUrl:
			alreadyPosted=False
			for comment in submission.comments:
				print comment.author
				if comment.author == myName:
					print "already posted"
					alreadyPosted=True
					break
			if alreadyPosted:
				continue
			newUrl=generateImgur(newUrl)
			if newUrl:
				postComment(submission, newUrl)
				print "sleeping"
				time.sleep(30)
				print "wokeup"

#def handleRoot(comment):
#	sub=r.get_info(thing_id=comment.parent_id)
#	if "imgur.com" not in sub.domain:
#		postFail(comment)
#		return
#	user=r.user
#	replies=comment.replies
#	for child in replies:
#		if str(child.author)==str(user):
#			return
#	imgurUrl=sub.url 
#	if ".png" not in imgurUrl or ".jpg" not in imgurUrl:
#		imgurUrl+=".jpg"
#	newUrl = generateImgur(imgurUrl)
#	postComment(comment, newUrl)
#def handleNode(comment):
#	parent=r.get_info(thing_id=comment.parent_id)
#	user = r.user
#	replies=comment.replies
#	for child in replies:
#		if str(child.author)==str(user):
#			return
#	pBody=parent.body
#	for word in pbody.split():
#		if 'imgur.com' in word:
#			word=str(word)
#			if ".png" not in word or ".jpg" not in word:
#				word+=".jpg"
#			newUrl=generateImgur(word)
#			postComment(comment, newUrl)
def postFail(comment):
	pass


def postComment(sub, url):
	print "hi"
	sub.add_comment("You've been Goog'd! \n\n"+url+"\n\n\n\nNote this bot is in development.  We'd love it if you messaged us with any feedback!")
	print "posted!"
	#main()
scanSubreddit('faces')