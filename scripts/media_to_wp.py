#!/usr/bin/env python
import os,re,sys
import mimetypes as mt
import argparse
import wordpress_xmlrpc as wp
from pypress import *

def main(argv,client=None):
  parser = argparse.ArgumentParser()
  parser.add_argument('-b','--blog', help='url of wordpress blog to which you want to post',dest='url')
  parser.add_argument('-u','--user', help="username with which you'd like to post to the blog",dest='username')
  parser.add_argument('-p','--password', help="password with which you'd like to post to the blog",dest='password')
  parser.add_argument('files', help='file to be uploaded to the Glog',
                      nargs='+')

  args = parser.parse_args(argv)

  conf= WPConfig(url=args.url,username=args.username,password=args.password)
  if (client is None):
    client = conf.getDefaultClient()
  wmpu=WPMediaUploader(client)
  wmpu.upload(args.files)

if __name__=="__main__":
  main(sys.argv[1:])
