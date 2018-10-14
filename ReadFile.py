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

Logger = Packages.LoggerDetails()
log = Logger.setLogger()

class ReadFile:
    def __init__(self):
        pass
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

        :return: True = Success/ False = Failure
        """
        if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
            log.debug('Entering function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)

        #Extract input Variables from the dictionary: funcInputs
        try:
            recordMarkerStartText = Packages.Utilities.getValuefromDict(funcInputs, 'recordMarkerStartText', 'Y')
            recordMarkerEndText = Packages.Utilities.getValuefromDict(funcInputs, 'recordMarkerEndText', 'Y')
            tableMarkerStartText = Packages.Utilities.getValuefromDict(funcInputs, 'tableMarkerStartText', 'Y')
            tableMarkerEndText = Packages.Utilities.getValuefromDict(funcInputs, 'tableMarkerEndText', 'Y')
            headerMarkerStartText = Packages.Utilities.getValuefromDict(funcInputs, 'headerMarkerStartText', 'N')
            headerMarkerEndText = Packages.Utilities.getValuefromDict(funcInputs, 'headerMarkerEndText', 'N')
            headerFieldsSelection = Packages.Utilities.getValuefromDict(funcInputs, 'headerFieldsSelection', 'Y')
            tableFieldsSelection = Packages.Utilities.getValuefromDict(funcInputs, 'tableFieldsSelection', 'Y')
            delimiter = Packages.Utilities.getValuefromDict(funcInputs, 'delimiter', 'Y')

        except ValueError as error:
            log.error(repr(error))
            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
            return  Packages.sv.XL_FAILURE

        tableHeaderHasUnits = True
        tableSeperator = 1

        headerMarkerStart = True
        tableMarkerStart = True
        recordMarkerStart = True
        tableIndexSelected = False
        headerPrinted = False

        headerMarkers = ()
        recordMarkers = ()
        tableMarkers = ()

        listHeaderMarkers = []
        listTableMarkers = []
        listRecordMarkers = []
        tableFieldIndex = []

        headerStart = 0
        headerEnd = 0
        tableStart = 0
        tableEnd = 0
        recordStart = 0
        recordEnd = 0
        outputStringBuffer = ""
        recCounter = 0
        outputFileName= " "
        returnDict = {}
        file = os.path.dirname(__file__)
        print(file)

        #creating objects of File Stream
        InputFile1, InputFile2 = itertools.tee(fileName,2)
        outputFileName = os.path.join(file,'OUTPUT','TXT', 'TXT_' + datetime.now().strftime('%d_%m_%y_%H_%M_%S') + "_output.csv")
        print(outputFileName)
        try:
            writeFile = open(outputFileName, mode='w')
            try:
               for lineno,fileDetails_temp in enumerate(InputFile1):
                   # Get start and end markets for record
                   fileDetails = str(fileDetails_temp)
                   if recordMarkerStartText in fileDetails and recordMarkerStart:
                       recordStart = lineno
                       recordMarkerStart = False
                   if recordMarkerEndText in fileDetails:
                       recordEnd = lineno
                       recordMarkers = recordStart, recordEnd
                       listRecordMarkers.append(recordMarkers)
                       recordMarkerStart = True
                   # Get start and end markets for Table
                   if tableMarkerStartText in fileDetails and tableMarkerStart:
                       tableStart = lineno
                       tableMarkerStart = False
                   if tableMarkerEndText in fileDetails:
                       tableEnd = lineno
                       tableMarkers = tableStart, tableEnd
                       listTableMarkers.append(tableMarkers)
                       tableMarkerStart = True

                   # Get start and end markets for Header
                   if headerMarkerStartText in fileDetails and headerMarkerStart:
                       headerStart = lineno
                       headerMarkerStart = False
                   if headerMarkerEndText in fileDetails:
                       headerEnd = lineno
                       headerMarkers = headerStart, headerEnd
                       listHeaderMarkers.append(headerMarkers)
                       headerMarkerStart = True
            except Exception as Ex:
                log.debug('Error in Getting Markers for Header,Record and Table')
                log.debug((repr(Ex)))
                if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                    log.debug('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
                returnDict['Parsing_Status'] = Packages.sv.XL_FAILURE
                returnDict['Record_count'] = recCounter
                return returnDict

            # Creating header text for output File
            log.debug('Creating header text for output File')
            fileHeader = ','.join(fldList for fldList in (headerFieldsSelection+tableFieldsSelection))
            outputStringBuffer = Packages.Utilities.writeFile(writeFile, outputStringBuffer, fileHeader + '\n')

            index = 0
            recCounter = 0
            tablerecCounter = 0
            record = []
            recordTable = []
            print('len(listRecordMarkers) :',len(listRecordMarkers))
            for openFile_temp in InputFile2:
                openFile = openFile_temp.decode("cp1253").strip()
                while index < len(listRecordMarkers):
                    recCounter += 1
                    try:
                        recordStartMarker, recordEndMarker = listRecordMarkers[index]
                        record = []
                        currentLine = ""
                        try:
                            while True:
                                currentLine = (next(InputFile2)).decode("utf-8").strip()
                                if recordMarkerStartText in currentLine:
                                    record.append(currentLine)
                                    break
                        except StopIteration:
                            continue
                        #check logic to append to record
                        for _ in range(recordStartMarker,recordEndMarker):
                            record.append(next(InputFile2).decode("cp1253").strip())

                        headerStartMarker = headerEndMarker = 0
                        headerStartMarker, headerEndMarker = listHeaderMarkers[index]
                        tableStartMarker = tableEndMarker = newTableMarker = 0
                        tableStartMarker, tableEndMarker = listTableMarkers[index]
                        index += 1

                        recordHeader = record[(headerStartMarker - recordStartMarker): (headerEndMarker - recordStartMarker)]
                        recordTable = record[(tableStartMarker - recordStartMarker): (tableEndMarker - recordStartMarker)]

                    except Exception as Ex:
                        log.debug('Error in Details of Header,Record and Table')
                        log.debug((repr(Ex)))
                        if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                            log.debug(
                                'Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
                        returnDict['Parsing_Status'] = Packages.sv.XL_FAILURE
                        returnDict['Record_count'] = recCounter
                        return returnDict

                    headerText = ""
                    fileHeader = ""
                    try:
                        for headText in recordHeader:
                            for headField in headerFieldsSelection:
                                if headField in headText:
                                    # Count number of delimiters in the line. if count = 1, then get the till the end of line and then tokenize based on delimiter
                                    if headText.count(delimiter) == 1:
                                        fieldDetails = re.findall('"' + headField + '.*?', headText, flags=re.DOTALL)
                                    elif headText.count(delimiter) == 0:
                                        #log.debug('No Delimiter found in the line for header filed: {0}'.format(headField))
                                        continue
                                    else:
                                        # Split the text based on delimiter and get the second item of the text after the text is split based on tokens
                                        fieldDetails = re.findall('"' + headField + '.*' + delimiter + '*?' + delimiter,
                                                                  headText, flags=re.DOTALL)
                                    if fieldDetails:
                                        if delimiter in fieldDetails[0]:
                                            if headerText:
                                                headerText += "," + \
                                                              str(fieldDetails[0]).strip().replace('"', '').split(
                                                                  ',')[1]
                                            else:
                                                headerText = \
                                                str(fieldDetails[0]).strip().replace('"', '').split(',')[1]
                                        else:
                                            log.debug('Delimiter not found in the field Details: {0}'.format(fieldDetails))
                                    else:
                                        log.debug('Details not found in the Header: {0}'.format(headText))
                                        headerText += ','

                    except Exception as Ex:
                        log.debug('Error in Getting Markers for Header')
                        log.debug("Record index : {0}".format(index))
                        log.debug((repr(Ex)))
                        if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                            log.debug('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
                        returnDict['Parsing_Status'] = Packages.sv.XL_FAILURE
                        returnDict['Record_count'] = recCounter
                        return returnDict

                     # Calculate number of lines to table start from the start table token
                    counter = 0
                    for tableData in recordTable:
                        if tableFieldsSelection[0] in tableData:
                            break
                        else:
                            counter += 1

                    tableHeaderList = []

                    if tableHeaderHasUnits:
                        newTableMarker = counter + tableSeperator + 1
                    else:
                        newTableMarker = counter + tableSeperator

                    print(headerText)
                    try:
                        # Create a list of header items for the table
                        for tableHeader in recordTable[counter:newTableMarker]:
                            tableHeaderList.append((tableHeader).replace('"', '').split(','))


                        # Get Table Header
                        if not tableIndexSelected:
                            for tableFields in tableFieldsSelection:
                                fieldIndex = (tableHeaderList[0]).index(tableFields)
                                tableFieldIndex.append(fieldIndex)
                                tableIndexSelected = True

                        # if table has header Units then get the units
                        if tableHeaderHasUnits and not headerPrinted:
                            headerPrinted = True
                            outputStringBuffer = Packages.Utilities.writeFile(writeFile, outputStringBuffer,
                                                                        ',' * len(headerFieldsSelection)
                                                                     + ','.join(string for string in
                                                                                   operator.itemgetter(
                                                                                       *tableFieldIndex)
                                                                                   (str(','.join(
                                                                                       lstItem for lstItem
                                                                                       in tableHeaderList[
                                                                                           1])).replace('"',
                                                                                                        '').split(
                                                                                       delimiter))) + '\n')


                         # get table data
                        for tableData in recordTable[newTableMarker:len(recordTable)]:
                            if delimiter in tableData:
                                tablerecCounter += 1
                                outputStringBuffer = Packages.Utilities.writeFile(writeFile, outputStringBuffer,
                                                                         headerText + ',' + ','.join(
                                                                                string for string in
                                                                                operator.itemgetter(
                                                                                    *tableFieldIndex)(
                                                                                    str(tableData).replace(
                                                                                        '"', '').split(
                                                                                        delimiter))) + '\n')



                    except Exception as Ex:
                        log.debug('Error in Getting Parsing for Table')
                        log.debug("Record index : : {0}".format(index))
                        log.debug((repr(Ex)))
                        if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                            log.debug(
                                'Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
                        returnDict['Parsing_Status'] = Packages.sv.XL_FAILURE
                        returnDict['Record_count'] = recCounter
                        return returnDict


            writeFile.write(outputStringBuffer)
            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug('Total Number of Records parsed in TXT : {0} '.format(recCounter))
                log.debug('Total Number of Table Records in TXT : {0} '.format(tablerecCounter))
        except IOError:
            log.error('Cannot open file: {0} in read mode'.format(fileName))
            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
            returnDict['Parsing_Status'] = Packages.sv.XL_FAILURE
            returnDict['Record_count'] = recCounter
            return returnDict

        except Exception as error:
            print(repr(error))
            log.error('Exception Encountered in function: file_tokenizer_txt')
            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
            returnDict['Parsing_Status'] = Packages.sv.XL_FAILURE
            returnDict['Record_count'] = recCounter
            return returnDict
        finally:
            writeFile.close()

        if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
            log.debug('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
        returnDict['Parsing_Status'] = Packages.sv.XL_SUCCESS
        returnDict['Record_count'] = recCounter
        returnDict['outputFileName'] = outputFileName
        return returnDict

