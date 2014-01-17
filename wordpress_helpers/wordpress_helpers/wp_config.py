import json
import sys
import os
import wordpress_xmlrpc as wp
from wp_clients import *

## Helper class to make posting to wordpress a bit easier
# conf = WPConfig()
# post = conf.geteDefaultPost()
# post.title = 'title'
# post.content = 'content'
# client = conf.getDefaultClient()
class WPConfig:
  def __init__(self):
    cfg_file=''
    if os.path.isfile('.wp-helpers.cfg'):
      cfg_file='.wp-helpers.cfg'
    elif os.path.isfile(os.path.expanduser('~/.wp-helpers.cfg')):
      cfg_file=os.path.expanduser('~/.wp-helpers.cfg')
    

    #parse config file(
    try:
      self.config=json.load(open(cfg_file))
    except IOError:
      print('error opening cfg file {} falling back on defaults')
      exit(0)

  def getDefaultPost(self):
    post = wp.WordPressPost()
    try:
      post_attrs = (post.definition.keys())
      for k,v in self.config['post_defaults'].iteritems():
        if k in post_attrs:
          setattr(post,k,v)
    except KeyError:
      print('No post defaults defined')
    return post

  def getDefaultMedia(self):
    media = wp.WordPressMedia()
    try:
      media_attrs = (media.definition.keys())
      for k,v in self.config['media_defaults'].iteritems():
        if k in media_attrs:
          setattr(media,k,v)
    except KeyError:
      print('No media defaults defined')
    return media

  def getDefaultClient(self):
      try:
        if self.config.has_key('public_key') and self.config.has_key('private_key'):
          return wp.SecureClient(url=self.config['url'],public_key =self.config['public_key'], private_key=self.config['private_key'])
        else:
          username = None
          password = None
          if self.config.has_key('username'):
            username=self.config['username']
          if self.config.has_key('password'):
            password=self.config['password']
          return  UPClient(url=self.config['url'], username=username, password=password)
      except Exception,e:
        print('Could not create client. {}'.format(e))
        exit(2)

  def getBaseURL(self):
    url=''
    try:
      url =  self.config['url'].split('xmlrpc.php')[0]
    except KeyError:
      print('No URL specified')
    return url 

  def getDisplayName(self):
    if self.config.has_key('display_name'):
      return self.config['display_name']
    if self.config.has_key('username'):
      return self.config['username']
    return '' 

def main(argv):
  WPConfig().getDefaultClient()

if __name__=="__main__":
  main(sys.argv[1:])
