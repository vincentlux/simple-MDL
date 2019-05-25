To split .mbox into 3 small chunks:

1. Count number of emails in .mbox `grep -c '^From ' mbox_file` 

2. Split by ^From `awk 'BEGIN{chunk=0} /^From /{msgs++;if(msgs==1300){msgs=0;chunk++}}{file="chunk_" chunk ".txt";print > file}' Archived.mbox`

# to automate indexing
1. convert single mbox file to n single files
2. indexing with modified .py
