import jobj
import pdfparserconstants
import base64

class JDoc:
    def __init__(meo, name):
        meo.name = name        

    def determineLineType(self, currentLine, lastLine, lastLineType, lastObj, lastMetaObj):

        #remove any extraneous LF or CR
        currentLine = currentLine.replace('\n',' ')
        currentLine = currentLine.replace('\r',' ')

        #determine if the last line type give authoritative hint on current line type
        hint = ""
        authoritative = False
        
        match lastLineType:
            case "empty":
                    hint = pdfparserconstants.PDF_FIRSTLINE
                    authoritative = True
            case "obj":
                hint = pdfparserconstants.OBJ_META
            case "obj-meta":
                pass
            case "obj-meta-cont":
                hint = pdfparserconstants.OBJ_META
            case "stream-start":
                hint = pdfparserconstants.OBJ_STREAM
                authoritative = True
            case _: 
                hint = pdfparserconstants.UNKOWN

        if authoritative:
            return hint

    #ORDER OF RULES MATTER!
    #OBJ START RULES
        #if current line contains "obj" but not "endobj", meaning it is the start of the obj section.
        #look for obj on current line
        objIndex = currentLine.find(pdfparserconstants.OBJ)
        #look for endobj on current line
        endobjIndex = currentLine.find(pdfparserconstants.ENDOBJ)
        #if current line contains "obj" but not "endobj", meaning it is the start of the obj section.
        if objIndex > -1 and endobjIndex < 0 :
            return pdfparserconstants.OBJ

    #OBJ END RULES
        if(endobjIndex >= 0):
            return pdfparserconstants.ENDOBJ

    #OBJ META LINE RULES
        bbIndex = currentLine.find(pdfparserconstants.BB)
        if (bbIndex == 0 and hint == pdfparserconstants.OBJ_META):
            if(self.isMetaLineComplete(currentLine)):
                return pdfparserconstants.OBJ_META
            else:
                return pdfparserconstants.OBJ_META_CONT


    #STREAM END RULES
        if(currentLine.strip() == pdfparserconstants.ENDSTREAM):
            return pdfparserconstants.STREAM_END

    #IN STREAM RULES
        if(lastMetaObj and lastMetaObj.hasStream):
            #authoritative if meta object had start stream tag in its line
            return pdfparserconstants.OBJ_STREAM

    #STREAM START RULES
        if(currentLine.strip() == pdfparserconstants.STREAM):
            return pdfparserconstants.STREAM_START


    #LINE CONTINUATION RULES
        if(currentLine.replace('\n', ' ').replace('\r',' ').isprintable()):
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
        newObj = jobj.JObj(id)
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
        bbCount = currentLine.count(pdfparserconstants.BB)
        ffCount = currentLine.count(pdfparserconstants.FF)

        if(bbCount == ffCount):
            return True
        else:
            return False

    def parseMetaObject(self, metaLine, sanityCheck):
        
        #only allow 100 levels of recursivity
        if(sanityCheck > 100):
            return None

        sanityCheck = sanityCheck + 1

        newMetaObj = jobj.JObj("test")
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
            
            if(myword.count(pdfparserconstants.BB) <= 0):
                propLine = "notset"
                break
            
            mySubObj = jobj.JObj("test")    
            #more parsing needed since it's an object
            #identify and remove subObj's key
            keyEnd = myword.find(pdfparserconstants.BB)
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
            testFF = testWord.find(pdfparserconstants.FF)
            testBB = testWord.find(pdfparserconstants.BB)
            
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
    def processRawLine(self, rawline, rlState, unfilterStreamFlag):
            
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
            if(rlState.isContinuation):
                currentLine = rlState.lastLine + currentLine

            lineType = self.determineLineType(currentLine, rlState.lastLine, rlState.lastLineType, rlState.lastObj, rlState.lastMetaObj)

            match lineType:
                case "obj":
                    rlState.currentObj = self.processStartObjLine(currentLine)
                    rlState.lastObj = rlState.currentObj
                case "endobj":
                    rlState.prevObj = rlState.currentObj
                case "obj-meta":
                    rlState.currentMetaObj = self.processObjMetaLine(currentLine, rlState.currentObj)
                    if(rlState.currentMetaObj.hasStream):
                        containsStreamStart = True
                    rlState.lastMetaObj = rlState.currentMetaObj
                    rlState.isContinuation = False
                case "obj-meta-cont":
                    rlState.isContinuation = True            
                case "pdf-firstline":
                    self.processFirstLine(currentLine)
                case "obj-stream":
                    #if stream processing detected, break since string processing not necessary
                    containsStreamContent = True
                case "stream-start":
                    containsStreamStart = True
                    rlState.currentMetaObj.hasStream = True
                case "stream-end":
                    #flip this so stream is only processed once
                    rlState.lastMetaObj.hasStream = False
                    containsStreamEnd = True
                case _:
                    pass
            rlState.lastLineType = lineType
            rlState.lastLine = currentLine

        #rawline processing
        if(containsStreamContent):
            #if stream processing detected, break since string processing not necessary
            
            if(rlState.streamPersist == None):
                rlState.streamPersist = rawline
            else:
                rlState.streamPersist = rlState.streamPersist + rawline

        if(containsStreamEnd):
            streamBuffer = rlState.streamPersist[0: len(rlState.streamPersist)-2]
            rlState.streamObj.stream =  base64.b64encode(streamBuffer).decode(encoding="ascii", errors="strict")
            if(unfilterStreamFlag=="Y"):
                rlState.streamObj.processStream(streamBuffer)

            rlState.streamPersist = None

        if(containsStreamStart):
            rlState.streamPersist = None
            rlState.streamObj = rlState.currentObj
