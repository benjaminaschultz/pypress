#!/usr/bin/env python
import os,re,sys
import argparse

import datetime as dt
import markdown as md
import HTMLParser as hp
import StringIO as strio
import wordpress_xmlrpc as wp

from wordpress_helpers import *


# create a subclass and override the handler methods
class HTMLWPParser(hp.HTMLParser):
  def __init__(self):
    self.img_files=[]
    self.title = None
    self.cur_data=''
    self.has_more=False
    self.tags=[]
    self.cats=[]
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

  def handle_comment(self,data):
    if(re.match('^title:',data) is not None):
      self.title=data.lstrip('title:')
    if(re.match('^tags:',data) is not None):
      data=data.lstrip('tags:')
      PATTERN = re.compile(r'''((?:[^\s"']|"[^"]*"|'[^']*')+)''')
      self.tags+=[re.sub('''['"]''','',t) for t in PATTERN.split(data)[1::2]]
    if(re.match('^categories:',data) is not None):
      data=data.lstrip('categories:')
      PATTERN = re.compile(r'''((?:[^\s"']|"[^"]*"|'[^']*')+)''')
      self.cats+=[re.sub('''['"]''','',t) for t in PATTERN.split(data)[1::2]]
    if(re.match('^more',data) is not None):
      self.has_more=True
  
  def getTitle(self):
    return self.title

  def getTags(self):
    return self.tags

  def getCategories(self):
    return self.cats

  def hasMore(self):
    return self.has_more

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
    
    #handle different file types
    ext = os.path.splitext(f)[1]
    if ext in ['.html','.txt']:
      #read in html file
      txt=open(f).read()
    elif ext in [ '.markdown', '.mdown', '.mkdn', '.mdwn', '.mkd', '.md']:
      #convert markdown to html
      txt = md.markdown(open(f).read())

    else:
      print "cannot proceed uploading non html file: {}".format(f)
      pass
    
    #parser the html file to be posted
    html_parser = HTMLWPParser()
    html_parser.feed(txt)

    #if there is no more tag, insert one to avoid very long post previews
    if not html_parser.hasMore():
      lines= strio.StringIO(txt).readlines()
      if len(lines)>10:
        txt=''
        for line in lines[0:10]:
          txt+=line
        txt+='<!--more-->'
        for line in lines[10:]:
          txt+=line 

    #if no title was passed in on the command line, insert one here
    if title is None:
      title=html_parser.getTitle()

    #upload images and replace links to links on server
    imgs = html_parser.getImageFiles()
    if(len(imgs)>0):
      wpmu = WPMediaUploader(client)
      urls = wpmu.upload(imgs)
      for i,url in urls.iteritems():
        txt=re.sub('src="*{}"*'.format(i),'src="{}"'.format(url),txt)

    #setup the post object
    post = conf.getDefaultPost()
    post.title=title
    post.content=txt

    #add categories and tags to post that were specified in document via html tags
    post.terms_names['category'] += cats + html_parser.getCategories()
    post.terms_names['post_tag'] += tags + html_parser.getTags()

    #if this post has been posted before, just edit it, otherwise make a new post
    posts = client.call(wp.methods.posts.GetPosts())
    post_dict = {p.title:p.id for p in posts}
    if title in post_dict.keys():
      client.call(wp.methods.posts.EditPost(post_dict[title],post))
    else:
      client.call(wp.methods.posts.NewPost(post))

if __name__=="__main__":
  main(sys.argv[1:])
