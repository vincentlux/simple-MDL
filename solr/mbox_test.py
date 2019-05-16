import argparse
import mailbox
import re


if __name__ == '__main__':
    with open("Archived.mbox", 'r', encoding='utf8') as f:
        res = ''
        for line in f:
            if " " not in line and line != "\n" and len(line) > 15: # 15 is arbitrary
                continue
            # if line.startswith("Content-Type: text/html"):
            res += line
    
    with open("Archived.txt", 'w') as wf:
        wf.write(res)
        print("finish")
                

