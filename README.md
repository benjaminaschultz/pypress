Using the Glog is already pretty painless, but I wanted an easy way to make posts with media from the command line and maintain records of my work. I wanted to have it in a language with _normal_ sized font so that others could easily extend it. Well...

    $wpup README.md
    Username: baschult
    Password: 
    New post titled "Introducing GlogPy" created from file "README.md" 
![mission accomplished](~/Downloads/accomplished.jpg "mission accomplished")
Ah, rats! I forgot to categorize or tag the post

    $wpup -f README.md -c Knowledgebase Announcement -t glog wordpress 'command line'
    Username:baschult 
    Password: 
    Post titled "Introducing GlogPy" updated from file "README.md"
That's better. 
<!--more-->
Titles, tags and categories can be specified on the command line or in files using html comment syntax
<!--congrats, you found the surprise--><!--title:Introducing GlogPy--><!--tags:'super secret tag'-->

    <!--title:Introducing GlogPy-->
    <!--tags:glog, python, wordpress-->
    <!--categories:Knowledgebase-->
"more" tags are automatically inserted after 10 lines if there is not one in the file already to prevent posts. for example...
    
    header1
    =======
    content
    <!--more-->
    more content
Right now the biggest problem is that it does not support markdown files with mathjax directly. However, if you use another markdown tool and provide these scripts with the html output, everything will be hunky dory. It would be great if we could get this working with latex in some form, but wordpress doesn't like the output from htlatex, so that'll be added later.

glogpy 
===============
glogpy contains two python libraries (python-wordpress-xmlrpc and wordpress\_helpers) that allow for easy posting to wordpress from python scripts. It also contains a few scripts to automatically upload markdown, html and txt files directly to the wordpress along with any images they contain.

Get glogpy from codeblue:
    
    git clone https://$USER@codeblue.umich.engin.umich.edu/git/glogpy
python\_xmlrpc
--------------
This is a branch of this [repository](https://github.com/maxcutler/python-wordpress-xmlrpc) that I have modified to work with the secure\_xmlrpc wordpress plugin. Of course, the secure\_xmlrpc plugin does not work right now, but when it does this library will let you securely post to wordpress without entering your password.

wordpress\_helpers
--------------
These are some convenience classes and scripts I wrote so that blog defaults can be handled read from a config file, as well as prompt the user for a password before posting so that your password doesn't need to be stored in a file anywhere.

this folder also contains three scripts that I wrote and file useful.

### media\_to\_wp.py
This script will batch upload media to your wordpress blog

    usage: media_to_wp.py [-h] [-b URL] [-u USERNAME] [-p PASSWORD] files [files ...]
    optional arguments:
      -h, --help  show this help message and exit
      -b URL, --blog URL  url of wordpress blog to which you want to post
      -u USERNAME, --user USERNAME  username with which you'd like to post to the blog
      -p PASSWORD, --password PASSWORD  password with which you'd like to post to the blog

### file\_to\_wp.py
This script will batch upload markdown, txt and html files to your wordpress blog, automatically uploading any images and fixing image links. Direct uploading of markdown files requires the python markdown package

    usage: file\_to\_wp.py [-h] [-b URL] [-u USERNAME] [-p PASSWORD] [-T TITLE] [-t [TAGS [TAGS ...]]] [-c [CATS [CATS ...]]] -f FILES [FILES ...]
    optional arguments:
        -h, --help            show this help message and exit
        -b URL, --blog URL    url of wordpress blog to which you want to post
        -u USERNAME, --user USERNAME  username with which you'd like to post to the blog
        -p PASSWORD, --password PASSWORD  password with which you'd like to post to the blog
        -T TITLE, --title TITLE  title of wordpress post, defaults to first header if unspecified.
        -t [TAGS [TAGS ...]], --tags [TAGS [TAGS ...]]  tags for the wordpress post
        -c [CATS [CATS ...]], --categories [CATS [CATS ...]]  categories for the wordpress post
        -f FILES [FILES ...], --files FILES [FILES ...]  files to be posted to the Glog

### todo\_to\_wp.py
This script integrates with todo.txt to post a report of tasks you've accomplished, automatically tagging posts with todo.txt project tags and linking to collaborators with todo.txt person handles.

I think todo.txt is a really awesome tool. Get it [here.](http://todotxt.com/) I'll write a separate post about how I use this script and todo.txt to easily maintain a worklog.

    usage: todo_to_wp.py [-h] [-b URL] [-u USERNAME] [-p PASSWORD] [-d DELTA] [-t [HTAGS [HTAGS ...]]]
    optional arguments:
     -h, --help            show this help message and exit
     -b URL, --blog URL    url of wordpress blog to which you want to post
     -u USERNAME, --user USERNAME username with which you'd like to post to the blog
     -p PASSWORD, --password PASSWORD password with which you'd like to post to the blog
     -d DELTA, --delta DELT  number of days back from to post you worklog from. defaults to posting only todays accomplishments
     -t [HTAGS [HTAGS ...]], --tags [HTAGS [HTAGS ...]]  task hashtags to post to the worklog. defaults to posting all tasks


Installation
---------------
Begin by installing the python xml

    cd python-wordpress-xmprc
    sudo python setup.py install

Then install the wordpress helpers package

    cd ../wordpress_helpers
    sudo python setup.py install

I recommend adding some aliases to the scripts to your bashrc (e.g.)

    #Glogpy aliases
    alias wptd='/path/to/wordpress_helpers/scripts/todo_to_wp.py'
    alias wpcp='/path/to/wordpress_helpers/scripts/media_to_wp.py'
    alias wpup='/path/to/wordpress_helpers/scripts/file_to_wp.py'

If you plan to upload markdown files with my script, you should also install the markdown library via pip. If you don't have pip install it via your package manaager

    sudo apt-get install python2.7-pip
or

    sudo port install py27-pip
then

    sudo pip install markdown2
Next we want to put the config file in place so that the scripts know who you are and where you want to blog to without using command line args every time.
  
    cp /path/to/wordpress_helper/examples/wp-helper-example.json ~/.wp-helper.json
Edit the config file with your username, blog url, default post settings, etc.

New Features
-------------
I had josh make this repository so that it be easy for others to correct my mistakes and add new features. Everyone in the group should be able to commit, so have at it!
