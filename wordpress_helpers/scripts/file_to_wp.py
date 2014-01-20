#!/usr/bin/env python
import os,re,sys
import argparse

import HTMLParser as hp
import StringIO as strio
import wordpress_xmlrpc as wp

from wordpress_helpers import *

'''
#mathjax safe markdown
def markdown(txt):
  import markdown2 as md
  marked = '':
  equation_nabber = re.compile(r'(\$\$|\$|\[\\?latex\])')
  markdown_escaper = re.compile(r'^(\t\t|[+.*#(0-9.)]')
  buff =''
  for line in txt:
    #if we're not in a codeblock, let's suck out the MathJax bits and process the rest with tex
    if re.match(r'^\t\t') is None:
      buff+=line
  
  txt = md.markdown(txt)
'''

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
        file_path = attrs['src']
        #don't try to upload images that are alreadly online!
        if re.match('^https*://',file_path) is None:
          self.img_files.append(file_path)
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
  parser.add_argument('-b','--blog', help='url of wordpress blog to which you want to post',dest='url')
  parser.add_argument('-u','--user', help="username with which you'd like to post to the blog",dest='username')
  parser.add_argument('-p','--password', help="password with which you'd like to post to the blog",dest='password')
  parser.add_argument('-T','--title', help='title of wordpress post, defaults to first header\
                      if unspecified.',dest='title')
  parser.add_argument('-t','--tags', help='tags for the wordpress post',
                      nargs='*',dest='tags',default=list())
  parser.add_argument('-c','--categories', help='categories for the wordpress post',
                      nargs='*',dest='cats',default=[])
  parser.add_argument('-f','--files', help='file to be uploaded to the Glog',dest='files',
                      nargs='+',required=True)

  args = parser.parse_args(argv)

  #intit
  conf= WPConfig(url=args.url,username=args.username,password=args.password)
  client = conf.getDefaultClient()

  #read in any title, tags or categories specified from the command line
  title = args.title
  tags = args.tags
  cats = args.cats

  for f in args.files:

    #handle different file types
    ext = os.path.splitext(f)[1]
    if ext in ['.html','.txt']:
      #read in html file
      txt=open(f).read()
    elif ext in [ '.markdown', '.mdown', '.mkdn', '.mdwn', '.mkd', '.md']:
      import markdown2 as md
      txt=md.markdown(open(f).read())
    else:
      print "cannot proceed uploading non html file: {}".format(f)
      exit() 
    
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
    if title is None:
      title=f

    #upload images and replace links to links on server
    imgs = html_parser.getImageFiles()


    # change directory to the file containing html so that
    # relative and absolute image paths easily and correctly
    dir_init = os.path.realpath(os.getcwd())
    dir_file = os.path.realpath(os.path.split(os.path.expanduser(f))[0])

    #ship out the files and replace the links
    if(len(imgs)>0):
      wpmu = WPMediaUploader(client)
      urls = wpmu.upload(imgs)
      for i,url in urls.iteritems():
        txt=re.sub('src="*{}"*'.format(i),'src="{}"'.format(url),txt)
    os.chdir(dir_init)

    #setup the post object
    title=title.strip().lstrip()
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
      print("Post titled \"{}\" updated from file \"{}\"".format(title,f))
    else:
      client.call(wp.methods.posts.NewPost(post))
      print("New post titled \"{}\" created from file \"{}\"".format(title,f))


if __name__=="__main__":
  main(sys.argv[1:])
