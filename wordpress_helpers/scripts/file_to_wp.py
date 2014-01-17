#!/usr/bin/env python
import os,re,sys
import argparse

import datetime as dt
import markdown as md
import HTMLParser as hp
import wordpress_xmlrpc as wp

from wordpress_helpers import *


# create a subclass and override the handler methods
class HTMLWPParser(hp.HTMLParser):
  def __init__(self):
    self.img_files=[]
    self.title = None
    self.cur_data=''
    hp.HTMLParser.__init__(self)

  def handle_starttag(self, tag, attrs):
    self.cur_data=''
    if tag=='img':
      attrs={a[0]:a[1] for a in attrs}
      try:
        self.img_files.append(attrs['src'])
      except:
        print 'img tag contained no "src" attritube'
      
  def handle_data(self,data):
    self.cur_data+=data

  def handle_endtag(self,tag):
    if re.match('h[1-9]',tag):
      if not self.title:
        self.title=self.cur_data

  def getImageFiles(self):
    return self.img_files

  def getTitle(self):
    return self.title


def main(argv):
  parser = argparse.ArgumentParser()
  parser.add_argument('-T','--title', help='title of wordpress post, defaults to first header\
                      if unspecified.',dest='title')
  parser.add_argument('-t','--tags', help='tags for the wordpress post',
                      nargs='*',dest='tags',default=list())
  parser.add_argument('-c','--categories', help='categories for the wordpress post',
                      nargs='*',dest='cats',default=['Lab Notebook'])
  parser.add_argument('files', help='file to be uploaded to the Glog',
                      nargs='+')

  args = parser.parse_args(argv)

  title = args.title
  tags = args.tags
  cats = args.cats
  conf= WPConfig()
  client = conf.getDefaultClient()
  base_url = conf.getBaseURL()

  user = conf.getDisplayName()

  #get today's date
  date_str = dt.date.today().isoformat()
  
  
  for f in args.files:
    ext = os.path.splitext(f)[1]
    if ext == '.html':
      #read in html file
      txt=open(f).read()
    elif ext in [ '.markdown', '.mdown', '.mkdn', '.mdwn', '.mkd', '.md']:
      #convert markdown to html
      txt = md.markdown(open(f).read())

    else:
      print "cannot proceed uploading non html file: {}".format(f)
      pass
      
    html_parser = HTMLWPParser()
    html_parser.feed(txt)

    if title is None:
      title=html_parser.getTitle()
    imgs = html_parser.getImageFiles()
    if(len(imgs)>0):
      wpmu = WPMediaUploader(client)
      urls = wpmu.upload(imgs)
      for i,url in urls.iteritems():
        txt=re.sub('src="*{}"*'.format(i),'src="{}"'.format(url),txt)

    post = conf.getDefaultPost()
    post.title=title
    post.content=txt
    #post.terms_names = {'post_tag':tags,'category':['Lab Notebook']}
    post.terms_names['category'] += cats
    post.terms_names['post_tag'] += tags
    client.call(wp.methods.posts.NewPost(post))

if __name__=="__main__":
  main(sys.argv[1:])
