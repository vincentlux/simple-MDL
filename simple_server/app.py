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
CORS(app)


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
@cross_origin(origin='*')
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

# sanity check route
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
