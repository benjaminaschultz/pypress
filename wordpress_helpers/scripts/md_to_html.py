#!/usr/bin/env python
import sys,re,os
import argparse as ap
import StringIO as strio
import markdown2 as md
import webbrowser as wb

def extractMathJax(file_in):
  str_out = strio.StringIO
  file_out = open(str_out)

  #mathjax sections will be extracted if they are between $, $$ or [latex][/latex] tags
  tag_dict = {r'\$':r'\$',r'\$$':r'\$$',r'\[latex\]':r'\[\/latex\]'}
  

  #Iterate through the input and extract all mathjax tags that do not reside within codeblocks
  #Replace the mathjax sections with html comments, process with markdown and reinsert mathjax bits
  for line in file_in:
    #am i in a list thinger
    #else am 
    pass

def main(argv):
  parser = ap.ArgumentParser()
  parser.add_argument('--preview', help='automatically launch a preview html window?',
                       action='store_true')
  parser.add_argument('files', help='file to be uploaded to the Glog',
                      nargs='+')

  args = parser.parse_args(argv)
  for f in args.files:
    fout_name=f.split('.')[0] + '.html'
    fout = open(fout_name,'w')
    fout.write(md.markdown(open(f).read()))
    if(args.preview):
      wb.open(fout_name)


if __name__=="__main__":
  main(sys.argv[1:])
