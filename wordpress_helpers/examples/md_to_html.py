import markdown as md

txt = open('md_ex.txt').read()
fout = open('md_ex.html','w')
fout.write(md.markdown(txt))
fout.close()
