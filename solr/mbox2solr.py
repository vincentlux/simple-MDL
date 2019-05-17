import argparse, re, os
import mailbox



class mbox2solr:
    def __init__(self, f_name, dir_in, dir_out):
        self.txt = ''
        self.f_name = f_name
        self.dir_in = dir_in
        # create sep folder for different file
        self.dir_out = os.path.join(dir_out,f_name.split('.')[0])
        self.f_in = os.path.join(dir_in, f_name)
        self.create_dir(self.dir_in)
        self.create_dir(self.dir_out)

    def split(self, remove_trashcode=False):
        """convert mbox to separate txt files ready for xml indexing 
            only works for .mbox (gmail) right now
        """
        count = 0
        temp_doc = ''
        end = False
        with open(self.f_in, 'r', encoding='ISO-8859-1') as f:
            line = f.readline() # first (must start with From )
            temp_doc += line 
            line = f.readline() 
            while True:
                while not line.startswith('From '):
                    temp_doc += line
                    line = f.readline()
                    # only get Content-Type: text/plain
                    if remove_trashcode:
                        if line.startswith('Content-Type: text/plain'): # get content between two C-T
                            temp_doc += line
                            line = f.readline()
                            while not line.startswith('Content-Type:'):
                                temp_doc += line
                                line = f.readline()
                            # this doc ends, now to consume all trash from this doc
                            while not line.startswith('From '):
                                line = f.readline()
                                if not line:
                                    break
                    # if EOF, end
                    if not line:
                        end = True
                        break
    
                # print(count)
                with open(os.path.join(self.dir_out, str(count)+'.txt'), 'w') as ff:
                    ff.write(temp_doc)
                count += 1
                temp_doc = ''
                temp_doc += line # in order to add first line to each file
                line = f.readline()
                if end:
                    print(count)
                    break

    def txt2xml(self):
        raise NotImplementedError


    def create_dir(self, dir_in):
        if not os.path.exists(dir_in):
            os.mkdir(dir_in)
    
       

