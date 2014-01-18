#!/usr/bin/env python
import os,re,sys
import mimetypes as mt
import wordpress_xmlrpc as wp

## Helper class to handle the bulk uploading of media to a WP Blog
class WPMediaUploader:

  def __init__(self,client):
    self.client=client

  ##this function uploads the files in "files" to a wp blog
  #files = list of files to upload
  #max_size = maximum size in MB to upload without a warning
  def upload(self,files,max_size=15):

    #make sure the total size is reasonable(<15MB)
    tot_size=0.0
    real_files = [os.path.realpath(os.path.expanduser(f)) for f in files]
    for f in real_files:
      tot_size+=os.path.getsize(f)

    tot_size/=(1024**2)
    if tot_size>max_size:
      resp =  raw_input("This will upload %5.2f MB of media to the Glog. Are you sure this is your intent? [y/N]"%(tot_size))
      if not resp=='y':
        exit(0)

    urls={}
    for f,rf in zip(files,real_files):
      mime = mt.guess_type(rf)[0]
      name = os.path.split(rf)[-1]
      bits = wp.compat.xmlrpc_client.Binary(open(rf,'rb').read())
      data= {'name':name, 'type':mime, 'bits':bits }
      resp = self.client.call(wp.methods.media.UploadFile(data))
      urls[f]=resp['url']


    return urls
