import uuid, re, os, sys
sys.path.append('./solr')
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from werkzeug import secure_filename
from post_processing import str_to_mdl
from search import Search 
from solr.indexing import indexing


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, supports_credentials=True)

# extension
ALLOWED_EXTENSIONS = set(['txt', 'mbox'])
test_search = Search()

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, no_ques_mark=False, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.no_ques_mark = no_ques_mark
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        print(self.message)
        # Add error-hinting here
        self.message = err_hinting(str(self.message), self.no_ques_mark)
        rv['message'] = str(self.message)
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/simple', methods=['GET', 'POST'])
@cross_origin(origin='http://localhost:8080')
def simple():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        # get SIMPLE query and call solr to get result
        query = post_data["query"]
        try:        
            res = test_search.search(query)
        except Exception as e:
            if '?' not in query:
                raise InvalidUsage(e,True, status_code=404)
            else:
                raise InvalidUsage(e,False, status_code=404)

        # restructure json 
        response_object["QTime"] = res["responseHeader"]["QTime"]

        response_object["docs"] = {}
        # convert docs string to json
        for i in range(len(res["response"]["docs"])):
            response_object['docs'][i] = res["response"]["docs"][i]
        
        # response_object["docs"] = res["response"]["docs"]
        # print(response_object)
        # print(res["response"]["docs"])
    return jsonify(response_object)


# regex for speech to result
@app.route('/speech_regex', methods=['GET','POST'])
def speech_regex():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        print(post_data)
        raw_query = post_data['query']
        response_object['raw_query'] = raw_query
        print(response_object['raw_query'])
        # convert string to mdl query
        response_object['res_query'] = str_to_mdl(raw_query)
        return jsonify(response_object)


@app.route('/upload_file', methods=['GET','POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      if f and allowed_file(f.filename):
          f.save(os.path.join('./data/Mail', secure_filename(f.filename)))
          filename = secure_filename(f.filename)
          
          # next thing to do: pass filename to indexing.py then automating
          corename = indexing(filename=filename)
          print(corename, 'start setSolr')
          
          test_search.setSolr(corename)

          return 'upload successfully'

      else:
          return 'only allow .txt or .mbox'

# regex for speech to result
@app.route('/reset_solr', methods=['GET','POST'])
def reset_solr():
    if request.method == 'POST':
        post_data = request.get_json()
        print(post_data)
        test_search.setSolr('demo')
        return 'reset to demo'

# connction check route
@app.route('/ping', methods=['GET'])
@cross_origin(origin='*')
def ping_pong():
    return jsonify('pong!')

def err_hinting(err_in, no_ques_mark=False):
    if no_ques_mark:
        return "Missing '?' at the start of the query. "
    else:
        err = re.sub("[\(\[].*?[\)\]]", "", str(err_in))
        return err

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
