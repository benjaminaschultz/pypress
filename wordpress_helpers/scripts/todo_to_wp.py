#!/usr/bin/env python
import os,re
import datetime as dt
import wordpress_xmlrpc as wp
from wordpress_helpers import *

conf= WPConfig()
client = conf.getDefaultClient()
post = conf.getDefaultPost()
base_url = conf.getBaseURL()

user = conf.getDisplayName()

#find done.txt
todo_cfg = open(os.path.expanduser('~/.todo.cfg'))
found=False
line = todo_cfg.readline()
while not found and not line=='':
  if re.match('export\s+TODO_DIR',line) is not None:
    found = True
    todo_dir = os.path.expanduser(line.split('TODO_DIR="')[-1]).rstrip().rstrip('"')
  line = todo_cfg.readline()

if not found:
  print('Could not locate done.txt')
#if you have admin priveledges you can list users 
try:
  users = [u.username  for u in client.call(wp.methods.users.GetUsers())]
except:
  users=None


#get today's date
date_str = dt.date.today().isoformat()
done_file = todo_dir+'/done.txt'

#list of today's accomplishments
accomplishments=[]

if(os.path.isfile(done_file)):
  for line in open(done_file):
  
    if (re.search('#glotzer',line) is not None 
        and re.match('^x {}'.format(date_str),line) is not None):
      accomplishments.append(line.split(date_str)[-1].replace('#glotzer',''))
else:
  print('Could not open done.txt')
  print todo_dir
  exit(0)
#construct html list
html_list=[]
tags=[]
for a in accomplishments:
  if re.search('@\w+',a) is not None:
    names = set([s[1:] for s in  re.findall('@\w+',a)])
    for n in names:
      if (users is None) or (n in users):
        link = '<a href={0}blog/author/{1}>@{1}</a>'.format(base_url,n)
        a=a.replace('@'+n,link)

  if re.search('\+',a) is not None:
    tags += [s[1:] for s in  re.findall('\+\w+',a)]
    a = a.replace('\+','')

  html_list.append('<li>{}</li>'.format(a))

if len(html_list)>=3:
  html_list = html_list[0:2]+['<!--more-->']+html_list[2:]

title='{}\'s Work Log for {}'.format(user,date_str)
content = '<ui>'+''.join(html_list)+'</ui>'
tags=list(set(tags))

post.title=title
post.content=content
post.terms_names = {'post_tag':tags,'category':['Lab Notebook']}
#post.terms_names = {'category':['Lab Notebook']}
client.call(wp.methods.posts.NewPost(post))
print post 
print content
print tags
