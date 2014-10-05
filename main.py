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
    url = str(request.query.get('url'))
    # download image from URL
    # pretty bad code - oh well
    url_filename = url.split("/")[-1]
    url_uuid = str(uuid.uuid4())
    f = open(url_uuid+url_filename,'wb')
    f.write(urllib.urlopen(url).read())
    f.close()
    if imageStuff.googlyify(url_uuid+url_filename):
        return static_file(url_uuid+url_filename+"_result.jpg", root=".")
    return "Sorry, we could not process that image"
@post('/googlyifyImage')
def googImage():
    print "hi"
    # thanks to http://stackoverflow.com/a/17134909
    image = request.files.get('image')
    name, ext = os.path.splitext(image.filename)
    im_uuid = str(uuid.uuid4())  
    f = open(im_uuid+name,'wb')
    f.write(image.file.read())
    f.close()
    if imageStuff.googlyify(im_uuid+name):
        return static_file(im_uuid+name+"_result.jpg", root=".")
    return "Sorry, we could not process that image"
@route('/')
def main():
    return """<html>
    <body>
    <form action="http://0.0.0.0:8080/googlyifyImage"
    enctype="multipart/form-data" method="post">
    <p>
    <input type="file" name="image">
    </p>
    <div>
    <input type="submit" value="Send">
    </div>
    </form>
    </body>
    </hmtl>"""
run(host='0.0.0.0', port=8080, server="cherrypy")
