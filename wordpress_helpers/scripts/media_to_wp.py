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
  conf= WPConfig()
  if (client is None):
    client = conf.getDefaultClient()
  wmpu=WPMediaUploader(client)
  wmpu.upload(args.files)

if __name__=="__main__":
  main(sys.argv[1:])
