#!/usr/bin/env python
import os,re,sys
import mimetypes as mt
import argparse
import wordpress_xmlrpc as wp

from wordpress_helpers import *

def main(argv,client=None):
  parser = argparse.ArgumentParser()
  parser.add_argument('files', help='file to be uploaded to the Glog',
                      nargs='+')

  args = parser.parse_args(argv)

  #make sure the total size is reasonable(<15MB)
  tot_size=0.0
  for f in args.files:
    tot_size+=os.path.getsize(f)

  tot_size/=(1024**2)
  if tot_size>15.0:
    resp =  raw_input("This will upload %5.2f MB of media to the Glog. Are you sure this is your intent? [y/N]"%(tot_size))
    if not resp=='y':
      exit(0)


  conf= WPConfig()
  if (client is None):
    client = conf.getDefaultClient()
  base_url = conf.getBaseURL()
  user = conf.getDisplayName()


  urls={}
  for f in args.files:
    mime = mt.guess_type(f)[0]
    name = os.path.split(f)[-1]
    bits = wp.compat.xmlrpc_client.Binary(open(f,'rb').read())
    data= {'name':name, 'type':mime, 'bits':bits }
    resp = client.call(wp.methods.media.UploadFile(data))
    urls[f]=resp['url']
    

    print(name,mime)
  print urls
  return urls

if __name__=="__main__":
  main(sys.argv[1:])
