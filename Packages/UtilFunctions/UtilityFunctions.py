import collections
import operator
import re
import csv

def writeFile(fo,strBuffer: str, strInput: str):

    """
    This is a function to write data to a output file
    :param fo: File Stream to which data needs to be written
    :param strBuffer: Buffer Object that is used to collect information to write data if the length of data is more than 100 bytes
    :param strInput: Data that needs to be written to the file
    :return: strBuffer
    """
    bufferSize = 5000

    if len(strBuffer) + len ('            ') + len(strInput)  <= bufferSize :
        strBuffer += strInput + '\n'
    else:
        fo.write(strBuffer)
        strBuffer = strInput + '\n'
    return strBuffer


def writeLogFile(strInput: str):
    """
    :param strInput: String to be sent to log file
    :return: None
    """
    print(strInput)


def getValuefromDict(inputDict:dict,key:str):
    """

    :param inputDict: Input dictionary containing values
    :param key: Key for which value needs to be fetched
    :return: Value of Key in Dictionary inputDict
    """

    keyValue = inputDict.get(key)

    if not keyValue:
        writeLogFile('{0} is not provided in the input dictionary'.format(key))
        """UtilFuncs.log.error(UserException.MyError.__repr__(
            UserException.MyError('InputNotDefined', 'Value not Defined for Input: {0}'.format(key))))
        """
        raise ValueError('{0} is not provided in the input parameters'.format(key))
        writeLogFile('{0} : {1}'.format(key, keyValue))
    return keyValue


def getHeader(prnttag: str, tag: str, inputDict:dict):
    """
    This is a function used to get the header values of xml tag
    :param prnttag: Parent tag for tag
    :param tag: Current tag
    :param inputDict: Dictionary containing the input variables for parsing
    :return:
    """
    tableHeader = dict(inputDict).get('tableHeader')
    parentTag = dict(inputDict).get('parentTag')
    headerFields = dict(inputDict).get('headerFields')
    tableFields = dict(inputDict).get('tableFields')

    tg = tag[1:] if '@' in tag else tag

    if (prnttag+':'+tg in  headerFields):
        tableHeader.append(prnttag+':'+tg)
    if (prnttag+':'+tg in  tableFields):
        tableHeader.append(prnttag+':'+tg)
    inputDict['tableHeader'] = tableHeader


def parseHeader(prnttag: str, attrList, inputDict:dict):
    """
    This is a function used to get the header values of xml tag
    :param prnttag: Parent tag for tag
    :param attrList: Value of Prent tag. This value can be a string, List or Ordered Dict
    :param inputDict: Dictionary containing the input variables for parsing
    :return:
    """

    if type(attrList) is list:
        for listAttr in attrList:
            if type(listAttr) is str:
                getHeader(prnttag,prnttag,inputDict)
            else:
                parseHeader(prnttag,listAttr,inputDict)
    elif type(attrList) is collections.OrderedDict:
        for k,v in attrList.items():
            if type(v) is str:
                getHeader(prnttag,k,inputDict)
            else:
                parseHeader(k,v,inputDict)


def getValue(prnttag:str, tag: str, attr,  inputDict: dict ):
    """
    :param prnttag: Parent Tag of Current Tag
    :param tag: Current Tag
    :param attr: Value of Current tag in XML.This value can be a string, List or Ordered Dict
    :param inputDict: Dictionary containing the input variables for parsing
    :return:
    """
    tableHeader = dict(inputDict).get('tableHeader')
    parentTag = dict(inputDict).get('parentTag')
    headerFields = dict(inputDict).get('headerFields')
    tableFields = dict(inputDict).get('tableFields')
    header = dict(inputDict).get('header')
    fields = dict(inputDict).get('fields')

    tg = tag[1:] if '@' in tag else tag

    if (prnttag + ':' + tg in headerFields):
        header.append(attr)
        tableHeader.append(prnttag + ':' + tg)
    if (prnttag + ':' + tg in tableFields):
        fields.append(attr)
        tableHeader.append(prnttag + ':' + tg)


def parseList(prnttag: str, attrList, inputDict:dict):
    """
    This is a function used to get the parse dict form of input xml and extract relavant details
    :param prnttag: Parent tag for tag
    :param attrList: Value of Prent tag. This value can be a string, List or Ordered Dict
    :param inputDict: Dictionary containing the input variables for parsing
    :return:
    """

    if type(attrList) is list:
        for listAttr in attrList:
            if type(listAttr) is str:
                getValue(prnttag,prnttag,listAttr,inputDict)
            else:
                parseList(prnttag,listAttr,inputDict)
    elif type(attrList) is collections.OrderedDict:
        for k,v in attrList.items():
            if type(v) is str:
                getValue(prnttag,k,v,inputDict)
            else:
                parseList(k,v,inputDict)


def getValuefromDict(funcInputs:dict,key:str,Mandatory:str = None):
    """
    :param funcInputs: Dictionary from which Values need to to retreived
    :param key: Key for which value needs to be retrieved
    :param Mandatory: Indicator to identify value as Mandatory/Optional
    :return: keyValue of the Key in the dictionary: funcInputs
    """
    keyValue = dict(funcInputs).get(key)
    if Mandatory and str(Mandatory).upper() == 'Y':
        if not keyValue:
            writeLogFile('{0} is not provided in the input dictionary'.format(key))
            writeLogFile('InputNotDefined'+('Value not Defined for Input: {0}'.format(key)))
            raise ValueError('{0} is not provided in the input dictionary'.format(key))
            writeLogFile('{0} : {1}'.format(key,keyValue))
    return keyValue

def createReturnDict(Return_Status:int,Parsing_Status:bool = False, Record_count:int = 0,outputFileName:str = None,errorMessage:str = None):
    """
    :param Return_Status:
    :param Parsing_Status:
    :param Record_count:
    :param outputFileName:
    :return:
    """
    returnDict = {}
    returnDict['Return_Status'] = Return_Status
    returnDict['Parsing_Status'] = Parsing_Status
    returnDict['Record_count'] = Record_count
    if outputFileName:
        returnDict['outputFileName'] = outputFileName
    if errorMessage:
        returnDict['errorMessage'] = errorMessage
    return returnDict


def getRecordRegex(file_content: str, startMarker: str, endMarker: str):
    """
    Function to break content into tokens based on start and end markers

    :param file_content: Content Which need to be tokenized
    :param startMarker: StartMarker of Parsing
    :param endMarker: End Marker of Parsing
    :return: records lazily
    """
    recordDetail = re.findall(startMarker + '.*?' + endMarker, file_content, flags=re.DOTALL)
    yield from parsed_data_iter(recordDetail)


def parsed_data_iter(data_iter):
    """
    Function to lazily return a iterator
    :param data_iter: Any Iterator
    :return: contents of iterator in a lazy way
    """
    for data in data_iter:
        yield data


def itersplit(text, sep=None):
    """
    split the text based on seperator
    :param text: Text which needs to be split
    :param sep: Seperator
    :return:
    """
    exp = re.compile(r'\s' if sep is None else re.escape(sep))
    pos = 0
    while True:
        m = exp.search(text, pos)
        if not m:
            if pos < len(text) or sep is not None:
                yield text[pos:]
            break
        if pos < m.start() or sep is not None:
            yield text[pos:m.start()]
        pos = m.end()


def getTableDetails(tableText, tableFieldsSelection, tableMarkerEndText, tableHeaderHasUnits=False, tableSeperator=1,
                    tableRecSeperator='-'):
    """
    Parse table and return details of parsing in as a ist
    :param tableText: text of table
    :param tableFieldsSelection: Fields required from the table
    :param tableMarkerEndText: End text of Table provided parsing
    :param tableHeaderHasUnits: Flag to indicate if the header of table has units
    :param tableSeperator: Integer value to indicate the number of rows between the table header and start of data
    :param tableRecSeperator: Text to identify the seperator of header and data in table
    :return:
    """

    tableHeader = []
    tableDataList = []
    tableFieldIndex = []
    while True:
        TableHeader = next(tableText)
        if tableFieldsSelection[0] in TableHeader:
            tableHeaderList = TableHeader.replace('"', '').split(',')
            break

    for tableFields in tableFieldsSelection:
        fieldIndex = (tableHeaderList).index(tableFields)
        tableFieldIndex.append(fieldIndex)

    if tableHeaderHasUnits:
        tableHeaderListUnits = operator.itemgetter(*tableFieldIndex)(next(tableText).replace('"', '').split(','))
        tableDataList.append(tableHeaderListUnits)

    counter = 0
    while counter < tableSeperator:
        next(tableText)
        counter += 1

    for tableData in tableText:
        if tableData and tableData != '\r':
            tableData = tableData
            if (10 * tableRecSeperator) in tableData:
                continue
            if tableMarkerEndText in tableData:
                continue
            tablerow = operator.itemgetter(*tableFieldIndex)(tableData.replace('"', '').split(','))
            tableDataList.append(tablerow)
    yield from parsed_data_iter(tableDataList)

def csv_parser(fname, *, delimiter=',', quotechar='"', include_header=False):
    """
    Function to parse a csv file
    :param fname: name of file
    :param delimiter:
    :param quotechar:
    :param include_header:
    :return:
    """
    with open(fname) as f:
        reader = csv.reader(f, delimiter=delimiter, quotechar=quotechar)
        if not include_header:
            next(f)
        yield from reader

def extract_field_names(fname,delimiter=',', quotechar='"'):
    reader = csv_parser(fname, delimiter=delimiter, quotechar=quotechar,include_header=True)
    return next(reader)

def Extract_data(fname, delimiter=',', quotechar='"'):
    reader = csv_parser(fname, delimiter=delimiter, quotechar=quotechar, include_header=False)
    yield from parsed_data_iter(reader)