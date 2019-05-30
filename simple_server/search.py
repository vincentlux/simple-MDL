import pysolr
import requests
import argparse
import cymantix_grammar as cg

class Search():
    def __init__(self):
        self.corename = 'mdl'
        
    def setSolr(self, corename):    
        self.corename = corename
        print('set!', self.corename)

    def search(self, command, test=False):
        # convert json to solr query
        # get json file
        inp_json = cg.c_json(command)
        # define field
        try:
            # '&' for multiple person
            inp_json["from"] = ' '.join(inp_json["from"].split())
            inp_json["from"] = inp_json["from"].replace("' '", "&")
            if self.corename == 'mdl':
                from_name = "from_name:"+inp_json["from"]
            else: # all files except demo only have from field instead of from_name
                from_name = "from:"+inp_json["from"]
        except:
            if self.corename == 'mdl':
                from_name = "from_name:*"
            else:
                from_name = "from:*"
        try:
            subject = "subject:"+inp_json["topic"]
        except:
            subject = "subject:*"
        try:
            content = "content:" + inp_json["attachment"]
        except:
            content = "content:*"
        try:
            if inp_json["total"]:
                num_rows = 10000
        except:
            pass
        try:
            num_rows = inp_json["piece"]
        except:
            # if not specified last x piece, return all results
            num_rows = 50000
        try:
            date = inp_json["time"]
            if "all" in date:
                num_rows = 50000
                date = "date:*"
            else:
                try:
                    num = eval(''.join([n for n in inp_json["time"] if n.isdigit()]))
                except:
                    num = 1
                if "day" in inp_json["time"].lower():
                    pass
                elif "month" in inp_json["time"].lower():
                    num *= 30
                elif "year" in inp_json["time"].lower():
                    num *= 365
                else:
                    num = 50000
                if self.corename == 'mdl':
                    date = "date:[2004-02-04T00:00:00Z-{:d}DAY TO NOW]".format(num)
                else:
                    date = "date:[NOW-{:d}DAY TO NOW]".format(num)
        except:
            date = "date:*"
        # combine string
        query = from_name
        fquery = subject + " AND " + content + " AND " + date
        # https://github.com/django-haystack/pysolr
        if test:
            # solr = pysolr.Solr("http://104.248.61.45:8983/solr/mdl/")
            if self.corename == 'mdl':
                solr = pysolr.Solr("http://localhost:8983/solr/mdl/")
            else:
                url = 'http://localhost:8983/solr/' + str(self.corename) + '/'
                solr = pysolr.Solr(url)

        # api mode; return json
        else: 
            if self.corename == 'mdl':
                solr = pysolr.Solr("http://localhost:8983/solr/mdl/", results_cls=dict)
            else:
                url = url = 'http://localhost:8983/solr/' + str(self.corename) + '/'
                solr = pysolr.Solr(url, results_cls=dict)
        # results = solr.search(q="from_name:Yates, Mike AND subject:* AND to_name:*", sort="date desc", rows=100)
        results = solr.search(q=query, fq=fquery, sort="date desc", rows=num_rows)
        return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--command', type=str, default='',
                        help='Test mode. Cymantix command eg. ?LAST all EMAIL from "Mike" ')
    args = parser.parse_args()

    # pass args to search
    results = search(args.command, test=True)
    print("Saw {0} result(s).".format(len(results)))

    # Just loop over it to access the results.
    for result in results:
        try:
            print("Message-ID: {0}.".format(result['message_id'][0]))
            print("From name: {0}.".format(result['from_name'][0]))
            print("To name: {0}.".format(result['to_name'][0]))
            print("From: {0}.".format(result['from'][0]))
            try:
                print("To: {0}.".format(result['to'][0]))
            except:
                pass
            print("Date: {0}.".format(result['date']))
            print("Subject: {0}.".format(result['subject'][0]))
            print("Content: {0}.".format(result['content'][0]))
            print("==========================================\n")
        except Exception as e:
            print(e)
            pass
    print("Retrieved {0} result(s).".format(len(results)))
