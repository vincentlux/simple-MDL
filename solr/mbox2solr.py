import argparse, re, os
import mailbox
from datetime import datetime
from xml.sax.saxutils import escape


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
        self.res_docs = [] # save all docs in a list

        self.start           = '<add>\n<doc>\n'
        self.f_message_id    = '<field name="message_id">'
        self.f_date          = '<field name="date">'
        self.f_from          = '<field name="from">'
        self.f_to            = '<field name="to">'
        self.f_subject       = '<field name="subject">'
        # self.f_from_name     = '<field name="from_name">'
        # self.f_to_name       = '<field name="to_name">'
        self.f_content       = '<field name="content">'
        self.close           = '</field>\n'
        self.end             = '</doc>\n</add>'

    def split(self, remove_trashcode=False, save_as_txt=False):
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
                        # get content between two Cconten-Type
                        if line.startswith('Content-Type: text/plain'): 
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

                if save_as_txt:
                    with open(os.path.join(self.dir_out, str(count)+'.txt'), 'w') as ff:
                        ff.write(temp_doc)
                else:
                    # save list for future txt2xml call
                    self.res_docs.append(temp_doc)

                # update 
                count += 1
                temp_doc = ''
                temp_doc += line # in order to add first line to each file
                line = f.readline()
                if end:
                    print(count)
                    break

    def txt2xml(self):
        """try to convert a string to xml string directly 
        (instead of save .txt+.xml)
        idea: 先split by \n 再在最后加\n 合起来成xml string
        """
        if not self.res_docs:
            print('does not have txt saved as var')
            raise NameError
        print(len(self.res_docs))
        for doc in self.res_docs:
            temp_dict = {}
            date = False
            content = False
            d = '\n'
            lines = [e+d for e in doc.split(d)]
            # start processing each file
            for line in lines[1:]:
                if not line.startswith('Content-Type: text/plain') and not content:
                    if ":" in line:
                        if line.startswith("Date:") and not date:
                            try:
                                date = True
                                split_line = line.strip().split(":", 1)
                                # strip time zone and format time
                                split_line[1] = split_line[1].strip()
                                split_line[1] = datetime.strptime(split_line[1], "%a, %d %b %Y %H:%M:%S %z").strftime('%Y-%m-%dT%H:%M:%SZ')
                                split_line[1] = self.xmlescape(split_line[1].strip())
                                print(split_line)
                            except:
                                print('error time!')
                                print(line, lines)
                                break
                        else:
                            if line.startswith("Date:"): # add to the former attribute
                                split_line[1] += self.xmlescape(line.strip())
                                print('potential error')
                                print(split_line[1])
                            else:
                                split_line = line.strip().split(":", 1)
                                split_line[1] = self.xmlescape(split_line[1].strip())
                    else:
                        split_line[1] += self.xmlescape(re.sub(r"[\s+]", ' ', line))
                    temp_dict[split_line[0]] = split_line[1]
                else:
                    # content
                    # to remove useless content lines
                    # if line.startswith('Content-Type:') or line.startswith('Content-Transfer'):
                    #     content = True
                    #     continue
                    content = True
                    try:
                        temp_dict["content"] += self.xmlescape(line)
                    except:
                        temp_dict["content"] = ""
                        temp_dict["content"] += self.xmlescape(line)

            
            for k,v in temp_dict.items():
                print(k,v)
            raise NotImplementedError
            # convert to xml

            


    def create_dir(self, dir_in):
        if not os.path.exists(dir_in):
            os.mkdir(dir_in)
    
    def xmlescape(self, data):
        return escape(data, entities={
            "'": "&apos;",
            "\"": "&quot;"
        })
    
       

