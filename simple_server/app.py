import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS
import search as s



# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

@app.route('/simple', methods=['GET', 'POST'])
def simple():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        # get SIMPLE query and call solr to get result
        query = post_data["query"]
        
        res = s.search(query)
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
def ping_pong():
    return jsonify('pong!')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
