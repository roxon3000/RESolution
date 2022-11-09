

from functools import partial
import json
from msilib.schema import BBControl
from telnetlib import WONT

import base64
import zlib 

####### Paramters
#Flag to process stream filters
unfilterStreamFlag = "Y"
inputFile = "form-example.pdf"
#inputFile = "IF107-guide.pdf"
#inputFile = "simple-pdf.pdf"
outputFile = 'form-example.content.json'
####################


OBJ = "obj"
BB = "<<"
FF = ">>"
STREAM = "stream"
ENDSTREAM="endstream"
ENDOBJ = "endobj"
EMPTY = "empty"
PDF_FIRSTLINE = "pdf-firstline"
OBJ_META = "obj-meta"
OBJ_META_CONT = "obj-meta-cont"
OBJ_STREAM = "obj-stream"
STREAM_START = "stream-start"
STREAM_END = "stream-end"

UNKOWN = "unknown"

objLast = False
metaLast = False
currentLineType=PDF_FIRSTLINE
lastLineType = EMPTY
lastLine = EMPTY

class JDoc:
    def __init__(meo, name):
        meo.name = name        

    def determineLineType(self, currentLine, lastLine, lastLineType, lastObj, lastMetaObj):
        
        if(currentLine.find(ENDSTREAM) >= 0):
            print('found u')

        #remove any extraneous LF or CR
        currentLine = currentLine.replace('\n','')
        currentLine = currentLine.replace('\r','')

        #determine if the last line type give authoritative hint on current line type
        hint = ""
        authoritative = False
        
        match lastLineType:
            case "empty":
                    hint = PDF_FIRSTLINE
                    authoritative = True
            case "obj":
                hint = OBJ_META
            case "obj-meta":
                pass
            case "obj-meta-cont":
                hint = OBJ_META
            case "stream-start":
                hint = OBJ_STREAM
                authoritative = True
            case _: 
                hint = UNKOWN

        if authoritative:
            return hint

    #ORDER OF RULES MATTER!
    #OBJ START RULES
        #if current line contains "obj" but not "endobj", meaning it is the start of the obj section.
        #look for obj on current line
        objIndex = currentLine.find(OBJ)
        #look for endobj on current line
        endobjIndex = currentLine.find(ENDOBJ)
        #if current line contains "obj" but not "endobj", meaning it is the start of the obj section.
        if objIndex > -1 and endobjIndex < 0 :
            return OBJ

    #OBJ END RULES
        if(endobjIndex >= 0):
            return ENDOBJ

    #OBJ META LINE RULES
        bbIndex = currentLine.find(BB)
        if (bbIndex == 0 and hint == OBJ_META):
            if(self.isMetaLineComplete(currentLine)):
                return OBJ_META
            else:
                return OBJ_META_CONT


    #STREAM END RULES
        if(currentLine.strip() == ENDSTREAM):
            return STREAM_END

    #IN STREAM RULES
        if(lastMetaObj and lastMetaObj.hasStream):
            #authoritative if meta object had start stream tag in its line
            return OBJ_STREAM

    #STREAM START RULES
        if(currentLine.strip() == STREAM):
            return STREAM_START


    #LINE CONTINUATION RULES
        if(currentLine.replace('\n', '').replace('\r','').isprintable()):
            lltLen = len(lastLineType)
            if(lltLen > 4 and lastLineType[lltLen-5:lltLen] == "-cont" ):
                return lastLineType
            else:
                return lastLineType + "-cont"

        return "error"

    def processFirstLine(self, currentLine):
        self.pdfVersion = currentLine[1:8]
    def processStartObjLine(self, currentLine):
        #processing the object definition line
        #split line based on spaces
        objline = currentLine.split()
        #id should be the first 
        id = objline[0]
        #version is second element
        version = objline[1]
        #add new object
        newObj = JObj(id)
        newObj.version = version
        #add empty meta section
        newObj.meta = []
        self.objs.append(newObj)
        return newObj
    def processObjMetaLine(self, currentLine, currentObj):

        #first build object tree
        #        
        metaObj = self.parseMetaObject(currentLine,  0)
        if(metaObj.hasStream):
            currentObj.hasStream = metaObj.hasStream
        currentObj.meta = metaObj   
        
        return metaObj
    def isMetaLineComplete(self, currentLine):
        bbCount = currentLine.count(BB)
        ffCount = currentLine.count(FF)

        if(bbCount == ffCount):
            return True
        else:
            return False

    def parseMetaObject(self, metaLine, sanityCheck):
        
        #only allow 100 levels of recursivity
        if(sanityCheck > 100):
            return None

        sanityCheck = sanityCheck + 1

        newMetaObj = JObj("test")
        #find the end of the meta obj
        endOfMetaObjIndex = self.findEndOfObject(metaLine)
        #identify leftover on the line after end of object. most often demarcation of stream
        leftOver = ""
        if(endOfMetaObjIndex < len(metaLine)):
            #add two for FF
            leftOver = metaLine[endOfMetaObjIndex + 2: len(metaLine)]
            #remove leftOver from metaLine. Only remove leftover if recursivivity is level 1
            if(sanityCheck < 2):
                print("Removing left over from metaLine: " + leftOver)
                metaLine = metaLine.replace(leftOver, "")
                #determine if leftover is stream demarcation since it may not have a new line
                if(leftOver.find("stream") > -1):
                    newMetaObj.hasStream = True

        #assum first 2 chars are BB
        myword = metaLine[2 : endOfMetaObjIndex]
        propLine = ""

        #check for any deeper meta's. There may be multiple trees per level, thus the While loop 
        while True:
            
            if(myword.count(BB) <= 0):
                propLine = "notset"
                break
            
            mySubObj = JObj("test")    
            #more parsing needed since it's an object
            #identify and remove subObj's key
            keyEnd = myword.find(BB)
            subObjKeyList = myword[0:keyEnd].split('/')
            #may not be first keyword, so split by '/' and take last key
            subObjKey = subObjKeyList[len(subObjKeyList)-1]
            endPropLine = myword.find(subObjKey)
            propLine = propLine + myword[0:endPropLine]

            myword = myword[keyEnd:len(myword)]
                
            mySubObj = self.parseMetaObject(myword, sanityCheck)
            newMetaObj.__setattr__(subObjKey, mySubObj)
                
            #look at rest of line
            endOfMetaObjIndex = self.findEndOfObject(myword)
            #plus two for BB
            myword = myword[endOfMetaObjIndex+2:len(myword)]

        
        #parse props
        if(propLine == "notset"):
            propLine = metaLine
        subProps = propLine.split('/')
        propRuleInEffect = "none"
        propBuilder = ""
        for prop in subProps:

            prop = prop.strip()
            if(propRuleInEffect == "BuildRule"):
                propRuleInEffect = "none"
                prop = propBuilder + " " + prop

            #special prop rules - eventually should externalize these
            #TODO: add more prop rules where they make sense.  Type=Filter for example
            if(prop == "Type" 
               or prop == "Filter"):
                propRuleInEffect = "BuildRule"
                propBuilder = prop

            
            if(propRuleInEffect == "none"):
                newMetaObj.mutate(prop)

        #print("left over in meta line: " + leftOver)
        return newMetaObj

    def findEndOfObject(self, metaLine):
        #returns most senior (outer) object end location
        testFF = -1
        endOfObjIndex = -1
        level = 0

        for i in range(0, len(metaLine)):
            
            #don't allow for two subsequent reads in case two FF's are right next to each other ">>>>". This gives a false positive on middle >>
            if(testFF >=0):
                testFF = -1
                continue

            testWord = metaLine[i:i+2]
            testFF = testWord.find(FF)
            testBB = testWord.find(BB)
            
            #if a BB is found, then encountered another sub meta object
            if(testBB >= 0):
                level = level + 1

            #if a FF is found, a pairing is complete, so take a level off
            if(testFF >= 0):
                level = level -1

            #level can be -1 since we don't count the initial BB - maybe it should. to be reviewed
            if(level <= 0):
                endOfObjIndex = i
                break;

            if(i+2 == len(metaLine)):
                break


        return endOfObjIndex


class JObj:
    def __init__(meo, id):
        meo.id = id
        meo.hasStream = False

    def __setattr__(self, name, value):
        newVal = value
        newVal = self.cleanValue(value)
        self.__dict__[name] = newVal

    def mutate(self, word):
        if(self.propRulesCheck(word)): 
            keyval = word.split(' ')
            if(len(keyval) == 2):
                self.__setattr__(keyval[0], keyval[1])
            elif(len(keyval) == 1):
                self.__setattr__(keyval[0], True)
            else:
                key = keyval[0]
                keyval.pop(0)
                self.__setattr__(key, keyval)
    def propRulesCheck(self, prop):
        
        #don't add empty properties
        if(len(prop) < 1):
            #ignore
            return False

        if(prop.strip() == BB):
            return False

        return True
    def cleanValue(self, value):
        newVal = ""
        
        if(isinstance(value, str) and len(value) > 0):
            #remove LF
            newVal = value.replace("\n", "")

            #remove FF and BB
            newVal = newVal.replace(BB,"")
            newVal = newVal.replace(FF,"")
        else:
            #don't change value if it's not a valid string
            #print("Could not set value because it's not a string")
            return value

        return newVal
    def deflateBuffer(self, buffer):
        deflatedBuffer = None
        zobj = zlib.decompressobj()
        deflatedBuffer = zobj.decompress(buffer)
                
        return deflatedBuffer
    def processStream(self, buffer):
        unfilteredStream = None
        metaObj = self.meta
        encoding = "none"

        if(hasattr(metaObj, "Filter") and metaObj.Filter == "FlateDecode"):
            
            try:
                uBuffer = self.deflateBuffer(buffer)
                #TODO: i don't like how I wrote this section in nested try/catch. will want to add more decoders later on
                try:
                    #try UTF-8. This may need to change or be configurable
                    unicodeLine = uBuffer.decode(encoding="UTF-8", errors="strict")
                    if(unicodeLine.isprintable()):
                        unfilteredStream = unicodeLine
                    else:
                        raise Exception('UTF8 Not Printable')
                    encoding="UTF-8"
                except Exception as inst:
                    print("decoding failed:  Obj ID " + self.id)
                    print(inst)
                    try:
                        #try ASCII. This may need to change or be configurable
                        asciiLine = uBuffer.decode(encoding="ascii", errors="surrogateescape")
                        if(asciiLine.isprintable()):
                            unfilteredStream = asciiLine
                        else:
                            raise Exception('ASCII Not Printable... giving up on decoding')
                        encoding="ascii"
                    except Exception as inst:
                        print("decoding failed:  Obj ID " + self.id)
                        print(inst)
                    
            except Exception as inst:
                print("Error occurred during decompression:  Obj ID " + self.id)
                print(inst)
            

        self.unfilteredStream = unfilteredStream
        self.derivedStreamEncoding = encoding
        return unfilteredStream
    
    def update(self, obj):
        self.__dict__.update(obj.__dict__.items())      
   

myDoc = JDoc("default")
myDoc.objs = []


with open(inputFile, 'rb') as tr:
    testBuff = tr.read()
tr.close()


with open('form-example.content.txt', 'wb') as tw:
    tw.write(testBuff)
tr.close()


with open(inputFile,'rb' ) as f:
    streamPersist = None
    #N
    currentObj= None
    lastObj = None 
    lastMetaObj = None
    #N-1
    prevObj = None
    #object that is in queue to have its stream populated
    streamObj = None
    isContinuation = False
    for rawline in f:

        #since reading in binary, need to account for carriage returns
        asciiLine = rawline.decode(encoding="ascii", errors="surrogateescape")
        crLines = asciiLine.splitlines(keepends=True)
        containsStreamStart = False
        containsStreamEnd = False
        containsStreamContent = False
        
        for line in crLines:
            #skip \n newlines
            if(line == "\n"):
                continue

            currentLine = str(line)
            if(isContinuation):
                currentLine = lastLine + currentLine

            lineType = myDoc.determineLineType(currentLine, lastLine, lastLineType, lastObj, lastMetaObj)

            match lineType:
                case "obj":
                    currentObj = myDoc.processStartObjLine(currentLine)
                    lastObj = currentObj
                case "endobj":
                    prevObj = currentObj
                case "obj-meta":
                    currentMetaObj = myDoc.processObjMetaLine(currentLine, currentObj)
                    if(currentMetaObj.hasStream):
                        containsStreamStart = True
                    lastMetaObj = currentMetaObj
                    isContinuation = False
                case "obj-meta-cont":
                    isContinuation = True            
                case "pdf-firstline":
                    myDoc.processFirstLine(currentLine)
                case "obj-stream":
                    #if stream processing detected, break since string processing not necessary
                    containsStreamContent = True
                case "stream-start":
                    containsStreamStart = True
                    currentMetaObj.hasStream = True
                case "stream-end":
                    #flip this so stream is only processed once
                    lastMetaObj.hasStream = False
                    containsStreamEnd = True
                case _:
                    pass
            lastLineType = lineType
            lastLine = currentLine

        #rawline processing
        if(containsStreamContent):
            #if stream processing detected, break since string processing not necessary
            
            if(streamPersist == None):
                streamPersist = rawline
            else:
                streamPersist = streamPersist + rawline

        if(containsStreamEnd):
            streamBuffer = streamPersist[0: len(streamPersist)-2]
            streamObj.stream =  base64.b64encode(streamBuffer).decode(encoding="ascii", errors="strict")
            if(unfilterStreamFlag=="Y"):
                streamObj.processStream(streamBuffer)

            streamPersist = None

        if(containsStreamStart):
            streamPersist = None
            streamObj = currentObj

f.close()

with open(outputFile, 'w', encoding="ascii", errors="surrogateescape") as fw:
       
       fw.write(json.dumps(myDoc, default=vars))

fw.close()


