import collections
from Packages import sv,LoggerDetails
import Packages

class UtilFuncs:
    Logger = LoggerDetails()
    log = Logger.setLogger()


    @staticmethod
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
            strBuffer += strInput
        else:
            fo.write(strBuffer)
            strBuffer = strInput
        return strBuffer


    @staticmethod
    def getValuefromDict(inputDict:dict,key:str):
        """

        :param inputDict: Input dictionary containing values
        :param key: Key for which value needs to be fetched
        :return: Value of Key in Dictionary inputDict
        """

        keyValue = inputDict.get(key)

        if not keyValue:
            UtilFuncs.log.error('{0} is not provided in the input dictionary'.format(key))
            """UtilFuncs.log.error(UserException.MyError.__repr__(
                UserException.MyError('InputNotDefined', 'Value not Defined for Input: {0}'.format(key))))
            """
            raise ValueError('{0} is not provided in the input parameters'.format(key))
        if UtilFuncs.log.getEffectiveLevel() == sv.XL_DEBUG:
            UtilFuncs.log.debug('{0} : {1}'.format(key,keyValue))
        return keyValue


    @staticmethod
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


    @staticmethod
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
                    UtilFuncs.getHeader(prnttag,prnttag,inputDict)
                else:
                    UtilFuncs.parseHeader(prnttag,listAttr,inputDict)
        elif type(attrList) is collections.OrderedDict:
            for k,v in attrList.items():
                if type(v) is str:
                    UtilFuncs.getHeader(prnttag,k,inputDict)
                else:
                    UtilFuncs.parseHeader(k,v,inputDict)


    @staticmethod
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


    @staticmethod
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
                    UtilFuncs.getValue(prnttag,prnttag,listAttr,inputDict)
                else:
                    UtilFuncs.parseList(prnttag,listAttr,inputDict)
        elif type(attrList) is collections.OrderedDict:
            for k,v in attrList.items():
                if type(v) is str:
                    UtilFuncs.getValue(prnttag,k,v,inputDict)
                else:
                    UtilFuncs.parseList(k,v,inputDict)


    @staticmethod
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
                UtilFuncs.log.error('{0} is not provided in the input dictionary'.format(key))
                UtilFuncs.log.error('InputNotDefined'+('Value not Defined for Input: {0}'.format(key)))
                raise ValueError('{0} is not provided in the input dictionary'.format(key))
        if UtilFuncs.log.getEffectiveLevel() == sv.XL_DEBUG:
            UtilFuncs.log.debug('{0} : {1}'.format(key,keyValue))
        return keyValue