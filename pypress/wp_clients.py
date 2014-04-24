import sys
from . import wp_config as wpc
import wordpress_xmlrpc as wp
import getpass as gp
## WordPressPost class that 
# conf = wpc.WPConfig()
# p = WordPressPost():
# conf.configureDefaultPost(post)
#username/password client
class UPClient(wp.Client):
  def __init__(self,url, username=None, password=None): 
    #first, prompt the user for their pase
    if username is not None:
      print('Username: {}'.format(username))
    else:
      username=raw_input('Username: ')

    if password is None:
      not_auth=True
      i=0
      while not_auth and i<3:
        password=gp.getpass()
        try:
          i=i+1
          wp.Client.__init__(self,url,username,password)
          self.call(wp.methods.posts.GetPosts())
          not_auth=False
        except:
          e =  sys.exc_info()[0]
          print('Password not accepted, Error: {}'.format(e))
          not_auth=True
      if i==3:
        print('Authentication failed. Exiting')
        exit(0)

