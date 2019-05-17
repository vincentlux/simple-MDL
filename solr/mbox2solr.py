import argparse
import mailbox
import re



class mbox2solr:
    def __init__(self):
        self.txt = ''

    def split(self, remove_trashcode=False):
        """convert mbox to separate txt files ready for xml indexing 
            only works for .mbox (gmail) right now
        """
        count = 0
        temp_doc = ''
        end = False
        with open("./data/Mail/chunk_0_filtered.txt", 'r', encoding='ISO-8859-1') as f:
            line = f.readline() # first (must start with From )
            temp_doc += line 
            line = f.readline() 
            while True:
                while not line.startswith('From '):
                    temp_doc += line
                    line = f.readline()
                    # only get Content-Type: text/plain
                    if remove_trashcode:
                        if line.startswith('Content-Type: text'): # get content between two C-T
                            temp_doc += line
                            line = f.readline()
                            while not line.startswith('Content-Type:'):
                                temp_doc += line
                                line = f.readline()
                            break
                

                    # if eof, end
                    if not line:
                        end = True
                        break
                # save
                with open('./data/txt/'+str(count)+'.txt', 'w') as ff:
                    ff.write(temp_doc)
                count += 1
                temp_doc = ''
                temp_doc += line # in order to add first line to each file
                line = f.readline()
                if end:
                    print(count)
                    break

                # if count == 3:
                #     raise NotImplementedError

            # for line in f:
            #     if remove_trashcode:
            #         if " " not in line and line != "\n" and len(line) > 15: # 15 is arbitrary
            #             continue
                
            #     # start split
            #     if line.startswith('From ') and count != 0:
            #         while not f.next().startswith('From '):
            #             temp_txt += next(line)??? 
            #             next_line = next_line.next()
                    
            #         with open(str(count)+'.txt') as ff:
            #             ff.write(temp_txt)
            #         count += 1
            #         temp_txt = ''
                
            #     if count == 3:
            #         raise NotImplementedError


        # with open("./Archived.txt", 'w') as wf:
        #     wf.write(res)
        #     print("finish")
       

