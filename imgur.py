import pyimgur
import urllib
import os
#TODO: Change  to Craig's code when it finishes 
im=pyimgur.Imgur("26007e9656f428b")
def generateImgur(url):
	#Pass image to Craig's code and get response
	request="http://googly.craighiller.com/googlyifyURL?url="+url
	f=open("answer.jpg", 'wb')
	holder = urllib.urlopen(request).read()
	if "Sorry" in holder or "Soz" in holder:
		f.close()
		print "failed to find goog"
		os.remove("answer.jpg")
		return
	f.write(urllib.urlopen(request).read())
	f.close()
	uploaded_image=im.upload_image("answer.jpg", title="You've Been Goog'd")
	os.remove("answer.jpg")
	return uploaded_image.link
def postImgur(image):
	uploaded_image=im.upload_image(image, title="You've Been Goog'd")
	return uploaded_image.link