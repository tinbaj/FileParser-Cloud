 # myApp.py
"""
This is the file which contains the main function
"""
import sys

print(sys.path)
from ReadFile import ReadFile
import Packages


class MyApp:
    def __init__(self):
        pass
    def __call__(self, *args,  **kwargs):
        pass
    @staticmethod
    def main( InputFile, **kwargs):
        """
        This is the main function of the App
        :param InputFile: Input file Stream for parsing
        :param kwargs:
        :return:
        """
        returnVal = {}
        retval = {}
        recordCount = 0


        Packages.writeLogFile("-----------------Starting new Parsing-------------")
        Packages.writeLogFile('Entering function main(self,**kwargs) of Module: ' + __name__)

        try:
            funcName = Packages.getValuefromDict(kwargs, 'funcName', 'Y')
            funcInput = Packages.getValuefromDict(kwargs, 'funcInput', 'Y')

            print('funcName : ', funcName)
        except ValueError as error:
            Packages.writeLogFile(repr(error))
            Packages.writeLogFile('Exiting function main(self,**kwargs) of Module: ' + __name__)
            returnVal["retval"] = Packages.sv.XL_FAILURE
            returnVal["recordCount"] = recordCount
            returnVal["Return_Status"] = 500
            return returnVal

        try:
            if str(funcName).upper() == "CSV":
                retval = ReadFile.file_tokenizer_csv(InputFile, funcInput)
                recordCount = dict(retval)['Record_count']
                Packages.writeLogFile('Value returned from function:file_tokenizer_txt is:  {0}  of Module: '.format(retval) + __name__)
            elif str(funcName).upper() == "TXT":
                retval = ReadFile.file_tokenizer_txt(InputFile, funcInput)
                recordCount = dict(retval)['Record_count']
                Packages.writeLogFile('Value returned from function:file_tokenizer_txt is:  {0}  of Module: '.format(retval) + __name__)

            elif str(funcName).upper() == "XML":
                retval = ReadFile.file_tokenizer_xml(InputFile, funcInput)

                recordCount = dict(retval)['Record_count']
                Packages.writeLogFile("Number of records processed = {0}".format(recordCount))
                Packages.writeLogFile('Value returned from function:file_tokenizer_txt is:  {0}  of Module: '.format(retval) + __name__)
            else:
                Packages.writeLogFile("Invalid value: {0} passed for parameter: funcName.".format(funcName))
                raise ValueError('Invalid value: {0} passed for parameter: funcName.'.format(funcName))

        except ValueError as error:
            Packages.writeLogFile(repr(error))
            Packages.writeLogFile('Exiting function main(self,**kwargs) of Module: ' + __name__)
            returnVal["retval"] = Packages.sv.XL_FAILURE
            returnVal["recordCount"] = recordCount
            returnVal["Return_Status"] = 500
            return returnVal

        Packages.writeLogFile('Exiting function main(self,**kwargs) of Module: ' + __name__)
        Packages.writeLogFile("-----------------End ofParsing-------------")
        returnVal = retval
        return returnVal
