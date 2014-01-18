#!/usr/bin/env python
import os,re,sys
import argparse as ap
import datetime as dt
import wordpress_xmlrpc as wp
from wordpress_helpers import *

parser = ap.ArgumentParser()
parser.add_argument('-d','--delta', help='number of days back from to post you worklog from. defaults to posting only todays accomplishments',default=1,dest='delta',type=int)
parser.add_argument('-t','--tags', help='task hashtags to post to the worklog. defaults to posting all tasks',nargs='*',dest='htags')

args = parser.parse_args(sys.argv[1:])

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
dates=[date_str]
for delta in range(args.delta):
  dates.append((dt.date.today()-dt.timedelta(days=delta)).isoformat())
done_file = todo_dir+'/done.txt'

#list of today's accomplishments
accomplishments={d:list() for d in dates}

if(os.path.isfile(done_file)):
  for line in open(done_file):
    for d in dates:
       if re.match('^x {}'.format(d),line) is not None:
        if any([re.search('#glotzer',line) is not None for ht in args.htags]) or len(args.htags)==0: 
          for ht in args.htags:
            line = line.split(d)[-1].replace('#{}'.format(ht),'')
        accomplishments[d].append(line)
else:
  print('Could not open done.txt')
  print todo_dir
  exit(0)


#construct html list
html_list=[]
tags=[]
for d in dates:
  if (len(accomplishments[d])>0):
    html_list.append('<h2>{}</h2>\n'.format(d))
    html_list.append('<ui>')
    for a in accomplishments[d]:
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
    html_list.append('</ui>')

if len(html_list)>=6:
  html_list = html_list[0:5]+['<!--more-->']+html_list[2:]

if len(dates)>1:
  title='{}\'s Work Log: {} to {}'.format(user,dates[-1],dates[0])
else:
  title='{}\'s Work Log: {}'.format(user,dates[0])
content = '<ui>'+''.join(html_list)+'</ui>'
tags=list(set(tags))

post.title=title
post.content=content
post.terms_names = {'post_tag':tags,'category':['Lab Notebook']}
#post.terms_names = {'category':['Lab Notebook']}

#if this post has been posted before, just edit it, otherwise make a new post
posts = client.call(wp.methods.posts.GetPosts())
post_dict = {p.title:p.id for p in posts}
if title in post_dict.keys():
  client.call(wp.methods.posts.EditPost(post_dict[title],post))
else:
  client.call(wp.methods.posts.NewPost(post))
