# ReadFile.py

"""
This file contains class ReadFile which has functions to parse xml, csv and text files

"""
import operator
import os
import re
import xmltodict
import Packages
import itertools
from datetime import datetime
import csv

class ReadFile:

    recCounter = 0

    def __init__(self):
        pass
    @staticmethod
    def file_tokenizer_csv(fileName,funcInputs: dict):
        """
        This is a function to tokenize a csv file and create an output file which contains column indexes provided in the input
        The Output File will be names: <Input File Name>_output.csv in the same directory as the source file
        :param
        fileName: Name of the source file. The File name should have the absolute path to the file
        funcInputs: Dictionary containing a list with the indexes of all the columns that need to be extracted.
        :return: True = Success/ False = Failure
        """

        Packages.writeLogFile("Entering function file_tokenizer_csv(fileName: str,funcInputs: dict) of Module: "+__name__)

        try:
            file = os.path.dirname(__file__)
            #Changed to remove saving of Temporary file 01/01/2019 STARTS
            # tmpFileName='tmp.csv'
            # Changed to remove saving of Temporary file 01/01/2019 ENDS
            outputStringBuffer = ""
            FieldIndex = []
            # Changed to remove saving of Temporary file 01/02/2019 STARTS
            # writeFile = open(outputFileName, mode='w')
            # outputFileName = os.path.join(file, 'OUTPUT', 'CSV',
            #                               'CSV_' + datetime.now().strftime('%d_%m_%y_%H_%M_%S') + "_output.csv")
            # Changed to remove saving of Temporary file 01/02/2019 ENDS
            ReadFile.recCounter = 0

            try:
                attribute_list = Packages.getValuefromDict(funcInputs, 'attribute_list', 'Y')
                delimiter = Packages.getValuefromDict(funcInputs, 'delimiter', 'Y')

            except ValueError as error:
                Packages.writeLogFile('1.' + repr(error))
                Packages.writeLogFile(
                    'Exiting function file_tokenizer_csv(fileName: str,funcInputs: dict) of Module: ' + __name__)
                return Packages.createReturnDict(Return_Status=500, Record_count=ReadFile.recCounter,
                                                 errorMessage='Error in Getting Inputs for parsing CSV File')

            # Changed to remove saving of Temporary file 01/01/2019 STARTS
            # fileName.save(tmpFileName)
            # fileName.close()
            # Changed to remove saving of Temporary file 01/01/2019 ENDS
            headerList = Packages.extract_field_names(fileName, delimiter=delimiter)
            header = list(headerList)

            for tableFields in attribute_list:
                fieldIndex = (list(header)).index(tableFields)
                FieldIndex.append(fieldIndex)
                print(len(FieldIndex))
                headerrow = operator.itemgetter(*FieldIndex)(header)


            if len(FieldIndex) == 1:
                outputStringBuffer = Packages.writeFile(outputStringBuffer, headerrow)
            else:
                outputStringBuffer = Packages.writeFile(outputStringBuffer,delimiter.join(headerrow))
            csvdata = Packages.Extract_data(fileName, delimiter=delimiter)

            for t in csvdata:
                ReadFile.recCounter += 1
                row = operator.itemgetter(*FieldIndex)(t)
                print(row)
                if len(FieldIndex) == 1:
                    outputStringBuffer = Packages.writeFile(outputStringBuffer, row)
                else:
                    outputStringBuffer = Packages.writeFile(outputStringBuffer, delimiter.join(row))

            # Changed to remove saving of Temporary file 01/02/2019 STARTS
            # writeFile.write(outputStringBuffer)
            # Changed to remove saving of Temporary file 01/02/2019 ENDS
        except Exception as error:
            Packages.writeLogFile(repr(error))
            Packages.writeLogFile("Exiting function file_tokenizer_csv(fileName: str,funcInputs: dict) of Module: " + __name__)
            return Packages.createReturnDict(Return_Status=500, Record_count=ReadFile.recCounter,errorMessage='Error in parsing csv file')
        finally:
            # Changed to remove saving of Temporary file 01/02/2019 STARTS
            # if not writeFile.closed:
            #     writeFile.close()
            # Changed to remove saving of Temporary file 01/02/2019 ENDS
            Packages.writeLogFile("Exiting function file_tokenizer_csv(fileName: str,funcInputs: dict) of Module: " + __name__)
        return Packages.createReturnDict(Return_Status=200, Parsing_Status=Packages.sv.XL_SUCCESS,Record_count=ReadFile.recCounter, outputFile=outputStringBuffer)

    @staticmethod
    def file_tokenizer_txt(fileName,funcInputs: dict):
        """
        This is a function to tokenize a txt file and create an output csv file which contains column provided in the input
        The Output File will be names: <Input File Name>_output.csv in the same directory as the source file
        :param
        fileName: Name of the source file. The File name should have the absolute path to the file
        funcInputs: Dictionary containing a list with the indexes of all the columns that need to be extracted.
            recordMarkerStartText (Mandatory): Text indicating the start of one record
            recordMarkerEndText (Mandatory): Text indicating the end of one record
            tableMarkerStartText (Mandatory): Text indicating the start of table withing a record
            tabledMarkerEndText (Mandatory): Text indicating the end of table withing a record
            headerMarkerStartText (Mandatory): Text indicating the start of header withing a record
            headerMarkerEndText (Mandatory): Text indicating the end of header withing a record
            headerFieldsSelection (Optional): List containing all the fields required from header
            tableFieldsSelection (Mandatory): List containing all the fields required from Table
            delimiter (Mandatory): delimiter for the values

        :return: Dictionary with below values:
        Parsing_Status = Success/ False = Failure
        Record_count = Number of Records
        Return_Status = Return Status for API
        outputFileName = Path of the Output File (if parsing is successful)
        """
        Packages.writeLogFile('Entering function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)

        #Extract input Variables from the dictionary: funcInputs
        try:
            recordMarkerStartText = Packages.getValuefromDict(funcInputs, 'recordMarkerStartText', 'Y')
            recordMarkerEndText = Packages.getValuefromDict(funcInputs, 'recordMarkerEndText', 'Y')
            tableMarkerStartText = Packages.getValuefromDict(funcInputs, 'tableMarkerStartText', 'Y')
            tableMarkerEndText = Packages.getValuefromDict(funcInputs, 'tableMarkerEndText', 'Y')
            headerMarkerStartText = Packages.getValuefromDict(funcInputs, 'headerMarkerStartText', 'N')
            headerMarkerEndText = Packages.getValuefromDict(funcInputs, 'headerMarkerEndText', 'N')
            headerFieldsSelection = Packages.getValuefromDict(funcInputs, 'headerFieldsSelection', 'Y')
            tableFieldsSelection = Packages.getValuefromDict(funcInputs, 'tableFieldsSelection', 'Y')
            delimiter = Packages.getValuefromDict(funcInputs, 'delimiter', 'Y')

        except ValueError as error:
            Packages.writeLogFile('1.' + repr(error))
            Packages.writeLogFile('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
            return Packages.createReturnDict(Return_Status=500, Record_count=ReadFile.recCounter,errorMessage='Error in Getting Inputs for parsing TXT File')

        tableHeaderHasUnits = True
        tableSeperator = 1

        OutputFileBuffer = ""
        tablerecCounter = 0
        outputFileName= " "
        headerPrinted = False

        file = os.path.dirname(__file__)
        print(file)

        #creating objects of File Stream
        # Changed to remove saving of Temporary file 01/01/2019 STARTS
        # outputFileName = os.path.join(file,'OUTPUT','TXT', 'TXT_' + datetime.now().strftime('%d_%m_%y_%H_%M_%S') + "_output.csv")
        # Changed to remove saving of Temporary file 01/01/2019 ENDS
        print(outputFileName)
        ReadFile.recCounter = 0
        try:
            # Changed to remove saving of Temporary file 01/01/2019 STARTS
            # writeFile = open(outputFileName, mode='w')
            # Changed to remove saving of Temporary file 01/01/2019 ENDS
            # Code Changed 01/01/2019 to handle the file stream as a string rather than a file STARTS
            # file_contents = fileName.read().decode('cp1252')
            # file_contents = fileName.decode('cp1252')
            # Code Changed 01/01/2019 to handle the file stream as a string rather than a file ENDS

            for RecordText in Packages.getRecordRegex(fileName, recordMarkerStartText, recordMarkerEndText):
                ReadFile.recCounter += 1
                headfieldList = []
                tableFieldList = []
                # Get Header for a Record
                for header in Packages.getRecordRegex(RecordText, headerMarkerStartText, headerMarkerEndText):
                    # Split the records of Header into a list, each record identified by seperator = \n
                    headerText = Packages.itersplit(header, sep='\n')
                    for headText in headerText:
                        """ For each header filed in input list, check in the header text, if value is present
                            if value is found, then get the index of headerfield in the  list headerText. its value will be the next element
                        """
                        for headerField in headerFieldsSelection:
                            if headerField in headText:
                                if headText.count(delimiter):
                                    fieldDetails = headText.replace('"', '').split(delimiter)
                                    fd = iter(fieldDetails)
                                    while True:
                                        if headerField in next(fd):
                                            break
                                    headfieldList.append(next(fd).strip())
                reportHeader = ','.join(headerFieldsSelection + tableFieldsSelection)
                # print(reportHeader)

                if not headerPrinted:
                    OutputFileBuffer = Packages.writeFile(OutputFileBuffer, reportHeader)
                    if not tableHeaderHasUnits:
                        headerPrinted = True
                for table in Packages.getRecordRegex(RecordText, tableMarkerStartText, tableMarkerEndText):
                    tableText = Packages.itersplit(table, sep='\n')
                    tableData = Packages.getTableDetails(tableText, tableFieldsSelection, tableMarkerEndText,
                                               tableHeaderHasUnits=tableHeaderHasUnits)
                    if tableHeaderHasUnits:
                        if headerPrinted:
                            next(tableData)
                        else:
                            OutputFileBuffer = Packages.writeFile( OutputFileBuffer,
                                                                  ',' * len(headerFieldsSelection) + ','.join(
                                                                      next(tableData)))
                            headerPrinted = True
                    for data in tableData:
                        print(data)
                        tablerecCounter += 1
                        OutputFileBuffer = Packages.writeFile( OutputFileBuffer,
                                                              ','.join(headfieldList + list(data)))

            # Changed to remove saving of Temporary file 01/01/2019 STARTS
            # writeFile.write(OutputFileBuffer)
            # Changed to remove saving of Temporary file 01/01/2019 ENDS
            Packages.writeLogFile('Total Number of Records parsed in TXT : {0} '.format(ReadFile.recCounter))
            Packages.writeLogFile('Total Number of Table Records in TXT : {0} '.format(tablerecCounter))
        except IOError:
            Packages.writeLogFile('Cannot open file: {0} in read mode'.format(fileName))
            Packages.writeLogFile('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
            return Packages.createReturnDict(Return_Status=500, Record_count=ReadFile.recCounter,errorMessage='Cannot open file: {0} in read mode'.format(fileName))

        except StopIteration:
            pass
        except Exception as error:
            print(repr(error))
            Packages.writeLogFile('1. Exception Encountered in function: file_tokenizer_txt')
            Packages.writeLogFile('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
            return Packages.createReturnDict(Return_Status=500, Record_count=ReadFile.recCounter,errorMessage='Error in parsing TXT file')
        # finally:
            #Changed to remove saving of Temporary file 01/01/2019 STARTS
            #writeFile.close()
            #Changed to remove saving of Temporary file 01/01/2019 ENDS
        Packages.writeLogFile('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
        return Packages.createReturnDict(Return_Status=200, Parsing_Status=Packages.sv.XL_SUCCESS,Record_count=ReadFile.recCounter, outputFile=OutputFileBuffer)

    @staticmethod
    def file_tokenizer_xml(fileName, funcInputs: dict):
        """
        This is a function to tokenize a xml file and create an output csv file which contains details for tags provided in the input
        The Output File will be names: <Input File Name>_output.csv in the same directory as the source file
        :param
        fileName: Name of the source file. The File name should have the absolute path to the file
        funcInputs: Dictionary containing a list with the indexes of all the columns that need to be extracted.
            parentTag (Mandatory): Tag which breaks two records
            headerFields (Mandatory): A List containing all the attributes which will be marked as header records, format: parentTag:tag
            tableFields (Mandatory): A List containing all the attributes which will be marked as table records tags, format: parentTag:tag
            tabledMarkerEndText (Mandatory): Text indicating the end of table withing a record

        :return: Dictionary with below values:
        Parsing_Status = Success/ False = Failure
        Record_count = Number of Records
        Return_Status = Return Status for API
        outputFileName = Path of the Output File (if parsing is successful)
        """

        Packages.writeLogFile('Entering function file_tokenizer_xml(fileName: str,funcInputs: dict) of Module: ' + __name__)
        try:
            if dict(funcInputs).get("tableHeader"):
                tableHeader = dict(funcInputs).get("tableHeader")
            else:
                tableHeader = []

            if dict(funcInputs).get("header"):
                header = dict(funcInputs).get("header")
            else:
                header = []

            if dict(funcInputs).get("fields"):
                fields = dict(funcInputs).get("fields")
            else:
                fields = []

            parentTag = Packages.getValuefromDict(funcInputs, 'parentTag')
            headerFields = Packages.getValuefromDict(funcInputs, 'headerFields')
            tableFields = Packages.getValuefromDict(funcInputs, 'tableFields')
            listRecordMarkers = []
            recordMarkerStart = True

        except ValueError as error:
            Packages.writeLogFile(repr(error))
            Packages.writeLogFile('Exiting function file_tokenizer_xml(fileName: str,funcInputs: dict) of Module: ' + __name__)
            return Packages.createReturnDict(Return_Status=500, Record_count=ReadFile.recCounter, errorMessage='Error in getting parameters for parsing XML File')
        try:
            # Changed to remove saving of Temporary file 01/01/2019 STARTS
            # file = os.path.dirname(__file__)
            # outputFileName = os.path.join(file, 'OUTPUT', 'XML',
            #                               'XML_' + datetime.now().strftime('%d_%m_%y_%H_%M_%S') + "_output.csv")
            # writeFile = open(outputFileName , mode='w')
            # Changed to remove saving of Temporary file 01/01/2019 ENDS
            patternMarker = '<' + parentTag + '[>| ].*?</' + parentTag + '>'
            currentHeaderRecord = ''
            outputStringBuffer = ''

            try:
                # creating objects of File Stream
                # Changed to remove saving of Temporary file 01/01/2019 STARTS
                # print(type(fileName))
                # file = fileName.read()
                # file = file.decode("cp1253")
                # Changed to remove saving of Temporary file 01/01/2019 ENDS

                # Changed to remove saving of Temporary file 01/01/2019 STARTS
                # tokenMatches = re.finditer(patternMarker, file, flags=re.MULTILINE | re.DOTALL)
                # Changed to remove saving of Temporary file 01/01/2019 ENDS
                tokenMatches = re.finditer(patternMarker, fileName, flags=re.MULTILINE | re.DOTALL)
                tokenMatchesHeader, tokenMatchesBody, tokenMatchesBody1 = itertools.tee(tokenMatches, 3)
                print(tokenMatchesHeader)
                print(tokenMatchesBody)
                print(tokenMatchesBody1)

            except Exception as Ex:
                Packages.writeLogFile('Error in Getting tokens')
                Packages.writeLogFile((repr(Ex)))
                Packages.writeLogFile('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
                return Packages.createReturnDict(Return_Status=500, Record_count=ReadFile.recCounter,errorMessage= 'Error in getting tokens for parsing XML file')

            for tm in tokenMatchesHeader:
                tableHeader = []
                funcInputs['tableHeader'] = tableHeader
                start, end = tm.span()
                # parsedRecord = xmltodict.parse(fileName[start:end])
                parsedRecord = xmltodict.parse(fileName[start:end])
                for k, v in parsedRecord.items():
                    if type(v) is str:
                        Packages.getHeader(k, k, funcInputs)
                    else:
                        Packages.parseHeader(k, v, funcInputs)

                tableHeader = dict(funcInputs).get('tableHeader')
                headerRecord = ','.join(strHeader for strHeader in tableHeader)

                if len(currentHeaderRecord) < len(headerRecord):
                    currentHeaderRecord = headerRecord
            outputStringBuffer = Packages.writeFile(outputStringBuffer, headerRecord)

            for tm in tokenMatchesBody:
                # Get data for the parsed file
                ReadFile.recCounter += 1
                tableHeader = []
                header = []
                fields = []

                funcInputs['tableHeader'] = tableHeader
                funcInputs['header'] = header
                funcInputs['fields'] = fields

                start, end = tm.span()
                # parsedRecord = xmltodict.parse(file[start:end])
                parsedRecord = xmltodict.parse(fileName[start:end])

                for k, v in parsedRecord.items():
                    if type(v) is str:
                        Packages.getValue(k, k, v, funcInputs)
                    else:
                        Packages.parseList(k, v, funcInputs)

                tableHeader = funcInputs.get('tableHeader')
                header = funcInputs.get('header')
                fields = funcInputs.get('fields')

                fullRecord = header + fields

                recordHeader = ','.join(strHeader for strHeader in tableHeader)

                indexHeader = 0
                indexRecord = 0
                strRecord = 0

                if len(headerRecord) == len(recordHeader):
                    strRecord = ','.join(strData for strData in fullRecord)
                else:
                    while (indexHeader < len(headerRecord.split(','))):
                        if tableHeader[indexRecord] == headerRecord.split(',')[indexHeader]:
                            if strRecord:
                                strRecord += ',' + str(fullRecord[indexRecord])
                                indexHeader += 1
                                indexRecord += 1
                            else:
                                strRecord = str(fullRecord[indexRecord])
                                indexHeader += 1
                                indexRecord += 1
                        else:
                            strRecord += ','
                            indexHeader += 1
                outputStringBuffer = Packages.writeFile(outputStringBuffer, strRecord)

            Packages.writeLogFile('Total Number of Records parsed in XML : {0} '.format(ReadFile.recCounter))

            # Changed to remove saving of Temporary file 01/01/2019 STARTS
            # writeFile.write(outputStringBuffer)
            # writeFile.close()
            # Changed to remove saving of Temporary file 01/01/2019 ENDS
        except Exception as Ex:
            Packages.writeLogFile('Error in Getting Markers for Header,Record and Table')
            Packages.writeLogFile((repr(Ex)))
            Packages.writeLogFile('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
            return Packages.createReturnDict(Return_Status=500, Record_count=ReadFile.recCounter,errorMessage= 'Error in Getting Markers for Header,Record and Table')

        Packages.writeLogFile('Exiting function file_tokenizer_xml(fileName: str,funcInputs: dict) of Module: ' + __name__)
        return Packages.createReturnDict(Return_Status=200, Parsing_Status=Packages.sv.XL_SUCCESS,Record_count=ReadFile.recCounter,outputFile=outputStringBuffer)
