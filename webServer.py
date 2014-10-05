#!/usr/bin/env python
import sys, os
import logging

package_dir = "packages"
package_dir_path = os.path.join(os.path.dirname(__file__), package_dir)
sys.path.insert(0, package_dir_path)

from bottle import get, route, run, post, static_file, error, request
import urllib
import uuid
import imageStuff
@error(404)
def error404(error):
    return "And where was I supposed to get this page from?"
@error(500)
def error500(error):
    return "Soz, we dun goofed."

## Yeah - we don't verify anything    
@route('/googlyifyURL')
def googURL():
    redirect("ec2-54-68-15-222.us-west-2.compute.amazonaws.com/googlyifyURL")
    # url = str(request.query.get('url'))
    #  # download image from URL
    #  # pretty bad code - oh well
    #  url_filename = url.split("/")[-1]
    #  url_uuid = str(uuid.uuid4())
    #  f = open(url_uuid+url_filename,'wb')
    #  f.write(urllib.urlopen(url).read())
    #  f.close()
    #  if imageStuff.googlyify(url_uuid+url_filename):
    #      return static_file(url_uuid+url_filename+"_result.jpg", root=".")
    #  return "Sorry, we could not process that image"
@post('/googlyifyImage')
def googImage():
    redirect("ec2-54-68-15-222.us-west-2.compute.amazonaws.com/googlyifyImage")
    
    # print "hi"
    #   # thanks to http://stackoverflow.com/a/17134909
    #   image = request.files.get('image')
    #   name, ext = os.path.splitext(image.filename)
    #   im_uuid = str(uuid.uuid4())  
    #   f = open(im_uuid+name,'wb')
    #   f.write(image.file.read())
    #   f.close()
    #   if imageStuff.googlyify(im_uuid+name):
    #       return static_file(im_uuid+name+"_result.jpg", root=".")
    #   return "Sorry, we could not process that image"
@route('/')
def main():
    return """<!DOCTYPE HTML>
    <html>
    	<head>
    		<link class="jsbin" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1/themes/base/jquery-ui.css" rel="stylesheet" type="text/css" />
    		<script class="jsbin" src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
    		<script class="jsbin" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.0/jquery-ui.min.js"></script>

    		<meta charset="utf-8" />
            <meta content="IE=Edge" http-equiv="X-UA-Compatible" />
            <title>GooglyBot</title>
            <link rel="stylesheet" type="text/css" href="style.css">
    	</head>

    	<body>
    		<script type="text/javascript">
    			function readURL(input) {
    				if (input.files && input.files[0]){
    					var reader = new FileReader();

    					reader.onload = function(e) {
    						$('#before')
    							.attr('src', e.target.result)
    					};

    					reader.readAsDataURL(input.files[0]);
    				}
    			}
    		</script>

    		<header>GoogMe</header>
    		<nav>
    			<form id="myform" action="ec2-54-68-15-222.us-west-2.compute.amazonaws.com/googlyifyImage"
    			enctype="multipart/form-data" method="post" onsubmit="return validate(this);" target="after">
    				<p>
    					Please specify a file, or a set of files:<br>
    					<input type="file" name="image" onchange="readURL(this);">
    				</p>
    				<div>
    					<input type="submit" value="Send">
    				</div>
    				<div id="before_container">
    					<img id="before" src="#" />
    				</div>
    			</form>
    			<div>
    			</div>
    		</nav>
    		<section>
    			<iframe id="after" name="after" src=""/>
    		</section>
    	</body>

    	<footer>
    	</footer>
    </html>

    """
run(host='0.0.0.0', port=80, server="cherrypy")
