import pyimgur
#TODO: Change  to Craig's code when it finishes 
im=pyimgur.Imgur("26007e9656f428b")
def generateImgur(url):
	#Pass image to Craig's code and get response
	c="./test.jpg" #CHANGEME!
	uploaded_image=im.upload_image(c, title="You've Been Goog'd")
	return uploaded_image.link