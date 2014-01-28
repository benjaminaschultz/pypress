My reseach group maintains a wordpress blog as our lab notebook. Leaving the terminal to go make a post was disruptive to my workflow and resulted in limited use of the blog. I wrote pypress so that I could post markdown files, ipython notebooks and other file formats directly to a wordpress blog and upload the media they contain with a single command.

Titles, tags and categories can be specified on the command line or in files using html comment syntax. Multimarkdown is used to convert markdown to html, so Mathjax is supported with markdown math syntax - `\(( mathy bits \\)` for inline math and `\\[ mathy bits \\]` for display math. Once a file has been used to create a post, that post can be updated by just running the same command again. Media is not reuploaded unless it has been modified.

Making a post is as easy as

    $ wpup -f example.md -T "Look mom, no mouse!" -c tests -t pypress
This will make a post titled "Look mom, no mouse!" in category "test" with a tag of pypress and content contained in example.md. If you changed the content of example.md, you can simply edit the post from the command line by running 

    $ wpup -f example.md -T "Look mom, no mouse!" -c tests -t pypress
again.

    $ wpup -f example2.md -b http://someblog.com -u benjaminaschultz
This will make a post containing the contents of example.md, and title, tag and categorize the post using comment tags contained within example.md. In this example, you will post to someblog.com, rather than someotherblog.com with is in your ~/.pypress-config.json file.

pypress
===============
pypress contains a couple of convenience classes and scripts so that blog and post defaults can be handled read from a config file, as well as prompt the user for a password before posting so that your password doesn't need to be stored in a file anywhere.

### media\_to\_wp.py
This script will batch upload media to your wordpress blog

    usage: media_to_wp.py [-h] [-b URL] [-u USERNAME] [-p PASSWORD] files [files ...]

### file\_to\_wp.py
This script will batch upload markdown, txt, ipython notebooks and html files to your wordpress blog, automatically uploading any images and fixing image links. Direct uploading of markdown files requires multimarkdown

    usage: file_to_wp.py [-h] [-b URL] [-u USERNAME] [-p PASSWORD] [-T [TITLES [TITLES ...]]] [-t [TAGS [TAGS ...]]] [-c [CATS [CATS ...]]] [-s STATUS] -f FILES [FILES ...] [--show] [--post_type TYPE]

Installation
---------------
Begin by installing my fork of Max Culter's python-xmlrpc library

    git clone https://github.com/benjaminaschultz/pypress.git
    cd pypress
    sudo python setup.py install

Then install the wordpress helpers package

    cd ../
    git clone https://github.com/benjaminaschultz/pypress.git
    cd pypress
    sudo python setup.py install
I recommend adding some aliases to the scripts to your bashrc (e.g.)

    #pypress aliases
    alias wpcp='/path/to/pypress/scripts/media_to_wp.py'
    alias wpup='/path/to/pypress/scripts/file_to_wp.py'

*If you plan to use mathjax and markdown together, please install multimarkdown.* There are mac installers available [here](http://fletcherpenney.net/multimarkdown/download/), or you can compile from source if you're a linux user ([git repo](https://github.com/fletcher/MultiMarkdown))

If for whatever reason you can't get multimarkdown working, you can use python's markdown2 library, but math syntax will not work.

    sudo apt-get install python2.7-pip
or

    sudo port install py27-pip
then

    sudo pip install markdown2

Next we want to put the config file in place so that the scripts know who you are and where you want to blog to without supplying command line args every time..

    cp examples/pypress-config.json ~/.pypress-config.json
Edit the config file with your username, blog url, default post settings, etc.

Basic behavior
-------------
Read all about markdown syntax [here.](http://daringfireball.net/projects/markdown/). 

When you use these scripts to upload a markdown file e.g.,

    $ wpup -f some_file.md -b https://blogthatoverridesconfile/ -u me

The following things happen:
1. The command line args are parsed and override any settings in your ~/.wp-helpers.json file
2. Your markdown file is converted to html with multimarkdown
3. An xmlrpc client connects to the blog
4. The html text is parsed for images, title, tags, categories, a "more" tag and math content
5. Images are renamed by their md5 sum and uploaded to the server if they do not exist already
   + Note: To cut  down on the amount of data sent back from the server, only the 50 most recent media items are checked against the media contained in a particular post
6. Image links are replaced by links to media on the server
7. If this post does not contain a "more" tag, one is inserted to prevent large posts takings over the blog.
8. If this post contains math, a `[mathjax]` flag is added to the beginning of the post so WP knows to render equations.
9. Posts by this user are retrieved. If a post has previously been created using this file, then it is updated by default, but this behavior can be overridden. Otherwise, a new post is created.

New Features
-------------
Eventually I'd like to add support for:
+ LaTeX in some form. WordPress doesn't like the html that htlatex creates, and multimarkdown and mathjax work pretty well for now
+ I'd love to get support for wordpress's secure_xmlrpc plugin working. This would allow you to safely post to blog without typing in your password and without storing your wp password anywhere.
