#!/usr/bin/env python
import os,re,sys
import hashlib as hl
import mimetypes as mt
import wordpress_xmlrpc as wp

## Helper class to handle the bulk uploading of media to a WP Blog
class WPMediaUploader:

  def __init__(self,client,reupload=False):
    self.client=client
    self.reupload=reupload

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
        print('exiting')
        exit(0)

    #compute the md5 hash for each of the files, this will help us uniquely identify them
    md5s = {f:hl.md5(open(rf,'rb').read()).hexdigest() for f,rf in zip(files,real_files)}
    #get the file extenstions
    exts = {f:os.path.splitext(rf)[1] for f,rf in zip(files,real_files)}
    urls={}

    media_lib = {}
    if not self.reupload: 
      #retrieve the media library
      media_list=self.client.call(wp.methods.media.GetMediaLibrary({'number':max(50,int(1.5*len(files)))}))
      media_lib = {os.path.split(m.link)[1]:m.link for m in media_list}
     
    for f,rf in zip(files,real_files):
      server_filename= os.path.split(f)[1] if self.reupload else md5s[f] + exts[f]
      if server_filename in media_lib:
        urls[f]=media_lib[server_filename]
        print('file {} is already on the server and was not reuploaded.'.format(f))
      else:
        mime = mt.guess_type(rf)[0]
        name = os.path.split(rf)[-1]
        bits = wp.compat.xmlrpc_client.Binary(open(rf,'rb').read())
        data= {'name':server_filename, 'type':mime, 'bits':bits }
        resp = self.client.call(wp.methods.media.UploadFile(data))
        urls[f]=resp['url']


    return urls
