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

Logger = Packages.LoggerDetails()
log = Logger.setLogger()

class ReadFile_XML:
    @staticmethod
    def file_tokenizer_xml(fileName: str, funcInputs: dict):
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

        :return: True = Success/ False = Failure
        """

        if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
            log.debug('Entering function file_tokenizer_xml(fileName: str,funcInputs: dict) of Module: ' + __name__)

        try:
            recCounter = 0
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

            parentTag = Packages.Utilities.getValuefromDict(funcInputs, 'parentTag')
            headerFields = Packages.Utilities.getValuefromDict(funcInputs, 'headerFields')
            tableFields = Packages.Utilities.getValuefromDict(funcInputs, 'tableFields')
            listRecordMarkers = []
            recCounter = 0
            recordMarkerStart = True

        except ValueError as error:
            log.error(repr(error))
            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug('Exiting function file_tokenizer_xml(fileName: str,funcInputs: dict) of Module: ' + __name__)
            return Packages.sv.XL_FAILURE,recCounter

        try:
            file_Name, extension = os.path.splitext(fileName)
            writeFile = open(file_Name + 'output.csv', mode='w')
            patternMarker = '<' + parentTag + '[>| ].*?</' + parentTag + '>'
            currentHeaderRecord = ''
            outputStringBuffer = ''
            recCounter = 0

            try:
                with open(fileName, mode='r') as f:
                    tokenMatches = re.finditer(patternMarker, f.read(), flags=re.MULTILINE | re.DOTALL)
                    tokenMatchesHeader,tokenMatchesBody,tokenMatchesBody1 = itertools.tee(tokenMatches,3)
                    print(tokenMatchesHeader)
                    print(tokenMatchesBody)
                    print(tokenMatchesBody1)

            except Exception as Ex:
                log.debug('Error in Getting tokens')
                log.debug((repr(Ex)))
                if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                    log.debug(
                        'Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
                return Packages.sv.XL_FAILURE, recCounter

            for tm in tokenMatchesHeader:
                with open(fileName, mode='r') as f:
                    tableHeader = []
                    funcInputs['tableHeader'] = tableHeader
                    start, end = tm.span()
                    parsedRecord = xmltodict.parse(f.read()[start:end])
                    for k, v in parsedRecord.items():
                        if type(v) is str:
                            Packages.Utilities.getHeader(k, k, funcInputs)
                        else:
                            Packages.Utilities.parseHeader(k, v, funcInputs)

                    tableHeader = dict(funcInputs).get('tableHeader')
                    headerRecord = ','.join(strHeader for strHeader in tableHeader)

                    if len(currentHeaderRecord) < len(headerRecord):
                        currentHeaderRecord = headerRecord
            outputStringBuffer = Packages.Utilities.writeFile(writeFile, outputStringBuffer, headerRecord + '\n')

            for tm in tokenMatchesBody:
                with open(fileName, mode='r') as f:
                # Get data for the parsed file
                    recCounter += 1
                    tableHeader = []
                    header = []
                    fields = []

                    funcInputs['tableHeader'] = tableHeader
                    funcInputs['header'] = header
                    funcInputs['fields'] = fields

                    start, end = tm.span()
                    parsedRecord = xmltodict.parse(f.read()[start:end])

                    for k, v in parsedRecord.items():
                        if type(v) is str:
                            Packages.Utilities.getValue(k, k, v, funcInputs)
                        else:
                            Packages.Utilities.parseList(k, v, funcInputs)

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
                    outputStringBuffer = Packages.Utilities.writeFile(writeFile, outputStringBuffer, strRecord + '\n')

            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug('Total Number of Records parsed in XML : {0} '.format(recCounter))

            writeFile.write(outputStringBuffer)
            writeFile.close()

        except Exception as Ex:
            log.debug('Error in Getting Markers for Header,Record and Table')
            log.debug((repr(Ex)))
            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
            return Packages.sv.XL_FAILURE, recCounter


        if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
            log.debug('Exiting function file_tokenizer_xml(fileName: str,funcInputs: dict) of Module: ' + __name__)
        return Packages.sv.XL_SUCCESS, recCounter
