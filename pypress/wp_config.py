import json
import sys
import os
import wordpress_xmlrpc as wp
from wp_clients import *
from wp_media import *

## Helper class to make posting to wordpress a bit easier
# conf = WPConfig()
# post = conf.geteDefaultPost()
# post.title = 'title'
# post.content = 'content'
# client = conf.getDefaultClient()
class WPConfig:
  def __init__(self, url=None, username=None, password=None):
    cfg_file=''
    if os.path.isfile('.pypress-config.json'):
      cfg_file='.pypress-config.json'
    elif os.path.isfile(os.path.expanduser('~/.pypress-config.json')):
      cfg_file=os.path.expanduser('~/.pypress-config.json')
    

    #parse config file(
    try:
      self.config=json.load(open(cfg_file))
    except IOError:
      print('error opening configuration file "{}" falling back on defaults'.format(cfg_file))

    self.url=url
    if url is None and  self.config.has_key('url'):
      self.url=self.config['url']

    self.username=username
    if username is None and self.config.has_key('username'):
      self.username=self.config['username']

    self.password=password
    if password is None and self.config.has_key('password'):
      self.password=self.config['password']

  def getDefaultPost(self):
    post = wp.WordPressPost()
    try:
      post_attrs = (post.definition.keys())
      for k,v in self.config['post_defaults'].iteritems():
        if k in post_attrs:
          setattr(post,k,v)
    except KeyError:
      print('No post defaults defined')

    setattr(post,'terms_names',{'category':list(),'post_tag':list()})
    return post

  def getDefaultClient(self):
      try:
        if self.config.has_key('public_key') and self.config.has_key('private_key'):
          return wp.Client(url=self.url+'/xmlrpc.php', public_key=self.config['public_key'], private_key=self.config['private_key'])
        else:
          return  UPClient(url=self.url+'/xmlrpc.php', username=self.username, password=self.password)
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
