import argparse, re, os, subprocess
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
        self.debug = []

        self.start           = '<add>\n<doc>\n'
        self.f_message_id    = '<field name="message_id">'
        self.f_date          = '<field name="date">'
        self.f_from          = '<field name="from">'
        self.f_to            = '<field name="to">'
        self.f_subject       = '<field name="subject">'
        self.f_content       = '<field name="content">'
        self.close           = '</field>\n'
        self.end             = '</doc>\n</add>'
        # self.f_from_name     = '<field name="from_name">'
        # self.f_to_name       = '<field name="to_name">'

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
                        if line.startswith('Content-Type: multipart'):
                            multi = True
                        if line.startswith('Content-Type: text/plain'): 
                            temp_doc += line
                            line = f.readline()
                            if multi:
                                while not line.startswith('Content-Type:'): #  and not(line.startswith('From ') and line[])
                                    temp_doc += line
                                    line = f.readline()
                                # this doc ends, now to consume all trash from this doc
                                while not line.startswith('From '):
                                    line = f.readline()
                                    if not line: # last one
                                        break
                            else:
                                while not line.startswith('From '): #  and not(line.startswith('From ') and line[])
                                    temp_doc += line
                                    line = f.readline()
                                    if not line: # last one
                                        break
                    # if EOF, end
                    if not line:
                        end = True
                        break

                multi = False
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
        idea: first split by \n then concat to a xml string
        """
        if not self.res_docs:
            print('does not have txt saved as var')
            raise NameError
        print(len(self.res_docs))
        count = 0
        for doc in self.res_docs:
            temp_dict = {}
            date = False
            content = False
            d = '\n'
            lines = [e+d for e in doc.split(d)]
            # start processing each file
            for line in lines[1:]:
                if not line.lower().startswith('content-type: text/plain') and not content:
                    if ':' in line:
                        if line.startswith('Date:') and not date:
                            split_line, date = self.process_date(line, date)        
                        else:
                            # if line.startswith("Date:"): # this is probably not possible because not yet to the content
                            #     print(count)
                            #     split_line[1] += self.xmlescape(line.strip())
                            split_line = line.strip().split(":", 1)
                            split_line[1] = self.xmlescape(split_line[1].strip())
                    else:
                        split_line[1] += self.xmlescape(re.sub(r"[\s+]", ' ', line))
                    temp_dict[split_line[0]] = split_line[1]

                else:
                    content = True
                    try:
                        # catch possible useful items under content-type (exception)
                        if (line.startswith('Message-Id') and 'Message-Id' not in temp_dict.keys()) \
                            or (line.startswith('Message-ID') and 'Message-ID' not in temp_dict.keys()) \
                            or (line.startswith('Message-id') and 'Message-id' not in temp_dict.keys()) \
                            or (line.startswith('Subject') and 'Subject' not in temp_dict.keys()) \
                            or (line.startswith('From') and 'From' not in temp_dict.keys()) \
                            or (line.startswith('To') and 'To' not in temp_dict.keys()):
                            split_line = line.strip().split(":", 1)
                            split_line[1] = self.xmlescape(split_line[1].strip())
                            temp_dict[split_line[0]] = split_line[1]
                        elif line.startswith('Date') and 'Date' not in temp_dict.keys():
                            split_line, _ = self.process_date(line, date)
                            split_line[1] = self.xmlescape(split_line[1].strip())
                            temp_dict[split_line[0]] = split_line[1]


                        else:
                            temp_dict['content'] += self.xmlescape(line)
                    except:
                        temp_dict['content'] = ''
                        temp_dict['content'] += self.xmlescape(line)

            # convert to xml
            xml = ''
            try:
                try:
                    _message_id = self.f_message_id + temp_dict['Message-ID'] + self.close
                except KeyError:
                    try:
                        _message_id = self.f_message_id + temp_dict['Message-Id'] + self.close
                    except KeyError:
                        _message_id = self.f_message_id + temp_dict['Message-id'] + self.close
                except:
                    print(temp_dict.keys())

                _date = self.f_date + temp_dict['Date'] + self.close
                _from = self.f_from + temp_dict['From'] + self.close
                try: 
                    _to = self.f_to + temp_dict['To'] + self.close
                except KeyError:
                    temp_dict['To'] = ''
                    _to = self.f_to + temp_dict['To'] + self.close
                try:
                    _subject = self.f_subject + temp_dict['Subject'] + self.close
                except:
                    temp_dict['Subject'] = ''
                    _subject = self.f_subject + temp_dict['Subject'] + self.close
                try:
                    _content = self.f_content + temp_dict['content'] + self.close
                except:
                    temp_dict['content'] = ''
                    _content = self.f_content + temp_dict['content'] + self.close
                xml = self.start + _message_id + _date + _from + _to + _subject + _content + self.end
            except Exception as e:
                # print(count,temp_dict)
                self.debug.append((e,count))
            with open(os.path.join(self.dir_out, str(count)+'.xml'), 'w') as ff:
                ff.write(xml)
            count += 1
        print(self.debug)

    def call_solr(self):
        raise NotImplementedError
        # in .sh: 
        # 1. add new core
        # 2. add field ?
        # 3. indexing by designated xml dir


        # output = subprocess.call(["./test.sh","xyz","1234"])
        # print(output)

    def create_dir(self, dir_in):
        if not os.path.exists(dir_in):
            os.mkdir(dir_in)
    
    def xmlescape(self, data):
        return escape(data, entities={
            "'": "&apos;",
            "\"": "&quot;"
        })
    
    def process_date(self, line, date):
        try:
            date = True
            split_line = line.strip().split(':', 1)
            # strip time zone and format time
            split_line[1] = split_line[1].strip()
            split_line[1] = datetime.strptime(split_line[1], '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%dT%H:%M:%SZ')
            
        except ValueError:
            try: # may contain (UTC) at the end
                split_line[1] = datetime.strptime(split_line[1][:-6].strip(), '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                try: # may be Sat, 28 May 2016 12:25:12 EDT
                    split_line[1] = datetime.strptime(split_line[1][:-4].strip(), '%a, %d %b %Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')
                except ValueError: # may be '3 Apr 2015 08:42:29 -0400'
                    split_line[1] = datetime.strptime(split_line[1], '%d %b %Y %H:%M:%S %z').strftime('%Y-%m-%dT%H:%M:%SZ')
            except Exception as e:
                print('error time!',e)
                print(line)

        finally:
            split_line[1] = self.xmlescape(split_line[1].strip())
        
        return split_line, date
    
       