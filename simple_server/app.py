import uuid, re
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import search as s


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, supports_credentials=True)


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
            res = s.search(query)
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

#@app.after_request
#def af_request(resp):     
#    """
#    :param resp:
#    :return:
#    """
#    resp.headers['Access-Control-Allow-Origin'] = '*'
#    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
#    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
#    return resp





# regex for speech to result
@app.route('/speech_regex', methods=['GET','POST'])
def speech_regex():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        print(post_data)
        raw_query = post_data["query"]
        response_object['raw_query'] = raw_query
        # v1
        # judge if the raw query is the keyboard input or speech input
        print(response_object['raw_query'])
        if not raw_query.startswith('?'):
            response_object['res_query'] = raw_query
            print("This should not be the case")
            return jsonify(response_object)
        else:
            # regex to convert keyword ('question mark', 'quote') into ('?','"')
            raw_query = raw_query.lower()
            res_query = raw_query.replace("quotes ", "'") \
                                .replace("quotes", "'") \
                                .replace("quote ", "'") \
                                .replace("quote", "'") \
                                .replace("on", "ON") \
                                .replace("email", "EMAIL")
                                

            response_object['res_query'] = res_query
            return jsonify(response_object)


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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
