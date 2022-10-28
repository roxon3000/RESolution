

import json
from telnetlib import WONT

OBJ = "obj"
BB = "<<"
FF = ">>"
STREAM = "stream"
ENDSTREAM="endstream"
ENDOBJ = "endobj"
EMPTY = "empty"
PDF_FIRSTLINE = "pdf-firstline"
OBJ_META = "obj-meta"
UNKOWN = "unknown"

objLast = False
metaLast = False
currentLineType=PDF_FIRSTLINE
lastLineType = EMPTY

class JDoc:
    def __init__(meo, name):
        meo.name = name

    def determineLineType(self, currentLine, lastLineType):
        
        #determine if the last line type give authoritative hint on current line type
        lastlineHint = ""
        authoritative = False
        match lastLineType:
            case "obj":
                lastlineHint = OBJ_META
            case _: 
                lastlineHint = UNKOWN

        if authoritative:
            return lastlineHint

    #OBJ START RULES
        #if current line contains "obj" but not "endobj", meaning it is the start of the obj section.
        #look for obj on current line
        objIndex = currentLine.find(OBJ)
        #look for endobj on current line
        endobjIndex = currentLine.find(ENDOBJ)
        #if current line contains "obj" but not "endobj", meaning it is the start of the obj section.
        if objIndex > -1 and endobjIndex < 0 :
            return OBJ

    #OBJ META LINE RULES
        bbIndex = currentLine.find(BB)
        if (bbIndex == 0 and lastlineHint == OBJ_META):
            return OBJ_META

        return "error"
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
        
        currentObj.meta = metaObj     

    def parseMetaObject(self, metaLine, sanityCheck):
        
        #only allow 100 levels of recursivity
        if(sanityCheck > 100):
            return None

        sanityCheck = sanityCheck + 1

        newMetaObj = JObj("test")
        #find the end of the meta obj
        endOfMetaObjIndex = self.findEndOfObject(metaLine)
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

            if(propRuleInEffect == "BuildRule"):
                propRuleInEffect = "none"
                prop = propBuilder + " " + prop

            #special prop rules - eventually should externalize these
            if(prop.strip() == "Type" 
               or prop.strip() == "Filter"):
                propRuleInEffect = "BuildRule"
                propBuilder = prop

            
            if(propRuleInEffect == "none"):
                newMetaObj.mutate(prop)

        return newMetaObj

    def findEndOfObject(self, metaLine):
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

    def __setattr__(self, name, value):
        self.__dict__[name] = value

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
        
        if(len(prop) < 1):
            #ignore
            return False


        return True

        
   

myDoc = JDoc("default")
myDoc.objs = []

with open('IF107-guide.pdf', 'r', encoding="ascii", errors="surrogateescape") as tr:
    testBuff = tr.read()
tr.close()

with open('form-example.content.txt', 'w', encoding="ascii", errors="surrogateescape") as tw:
    tw.write(testBuff)
tr.close()

with open('IF107-guide.pdf','r', encoding="ascii", errors="surrogateescape" ) as f:
    currentObj= None
    for line in f:
        currentLine = str(line)
        lineType = myDoc.determineLineType(currentLine, lastLineType)
        
        match lineType:
            case "obj":
                currentObj = myDoc.processStartObjLine(currentLine)
            case "obj-meta":
                myDoc.processObjMetaLine(currentLine, currentObj)
            case _:
                pass
        lastLineType = lineType


f.close()

#et = sys.getdefaultencoding()


with open('form-example.content.json', 'w', encoding="ascii", errors="surrogateescape") as fw:
       
       fw.write(json.dumps(myDoc, default=vars))

fw.close()


