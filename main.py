from flask import Flask, request, send_from_directory,send_file
from flask_restful import Resource, Api
import json
import Packages
from myApp import MyApp
import uwsgi

app = Flask(__name__)
api = Api(app)

class FileParser(Resource):

    def post(self, fileType):
        if fileType == 'TXT' or fileType == 'XML' or fileType == 'CSV':
            # Get input from Post Request
            #File for Parsing
            file = request.files['ParsingFile']

            #parsing parameters
            req_data = request.form['request']

            # convert json to dictionary to be passed to parsing functions
            request_data = json.loads(req_data)
            request_data["funcName"] = fileType

            retval = MyApp.main(file,**request_data)
            if retval["retval"] == Packages.sv.XL_FAILURE:
                return retval
            else:
                return send_file(retval['outputFileName'])
        else:
            return "Invalid File Type passed"
api.add_resource(FileParser,'/FileParser/<string:fileType>')

if __name__ == '__main__':
    app.run(port=8000,debug=True)