from flask import Flask, request, send_file
from flask_restful import Resource, Api
import json
import Packages


from myApp import MyApp

app = Flask(__name__)
api = Api(app)

class FileParser(Resource):
    def post(self, fileType):
        if fileType == 'TXT' or fileType == 'XML' or fileType == 'CSV':
            # Get Environment Variables
            # project_id = os.environ['GCLOUD_PROJECT']
            # bucket_val = os.environ['CLOUD_STORAGE_BUCKET']
            # print('project_id is : {0}'.format(project_id))
            # print('bucket_val is : {0}'.format(bucket_val))

            # File for Parsing
            # Get input from Post Request
            print("Request Recieved is: " , request)
            try:
                # file = request.files['ParsingFile']
                file = request.form['ParsingFile']
            except Exception as Ex:
                Packages.writeLogFile("Error Encountered in Getting Input Variables: ParsingFile ")
                Packages.writeLogFile((repr(Ex)))
                return Packages.createReturnDict(Return_Status=400, errorMessage='Error in Getting Value of ParsingFile from request')
            try:
                #parsing parameters
                req_data = request.form['ParsingRules']
                # convert json to dictionary to be passed to parsing functions
                request_data = json.loads(req_data)
                request_data["funcName"] = fileType
                Packages.writeLogFile("ParsingRules : ")
                for inputdata,values in request_data.items():
                    Packages.writeLogFile('{0} : {1}'.format(inputdata,values))
            except Exception as Ex:
                Packages.writeLogFile("Error Encountered in Getting Input Variables: ParsingRules ")
                Packages.writeLogFile((repr(Ex)))
                return Packages.createReturnDict(Return_Status=400,
                                                 errorMessage='Error in Getting Value of ParsingRules from Input Request')

            retval = MyApp.main(file,**request_data)

            if retval["Parsing_Status"] == Packages.sv.XL_FAILURE:
                    return retval,retval["Return_Status"]
            else:
                try:
                    return retval
                except Exception as Ex:
                    print(retval)
                    retval["Parsing_Status"] = Packages.sv.XL_FAILURE
                    retval["Return_Status"] = 500
                    retval["Record_count"] = 0
                    return retval, retval["Return_Status"]
        else:
            return "Invalid File Type passed"
api.add_resource(FileParser,'/FileParser/<string:fileType>')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)