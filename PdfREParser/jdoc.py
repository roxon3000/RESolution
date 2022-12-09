import jobj
import pdfparserconstants
import base64
from hashlib import md5
import re
import xrefUtil 

class JDoc:
    def __init__(meo, name):
        meo.name = name        
        meo.fileType = 'PDF'
        meo.xrefObj = None
        meo.xrefSet = False

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
                #check to see if meta obj begin tag exists
                bbCount = currentLine.count(pdfparserconstants.BB)
                if(bbCount > 0):
                    hint = pdfparserconstants.OBJ_META
                else:
                    hint = pdfparserconstants.CONTENT
                    authoritative = True
            case "obj-meta":
                pass
            case "obj-meta-cont":
                hint = pdfparserconstants.OBJ_META
            case "trailer-cont":
                hint = pdfparserconstants.OBJ_META
            case "stream-start":
                hint = pdfparserconstants.OBJ_STREAM
                authoritative = True
            case "xref":
                hint = pdfparserconstants.XREF_INDEX
                authoritative = True
            case "xrefindex":
                hint = pdfparserconstants.XREF_ROW
                authoritative = True
            case "xrefrow":
                #technically this assignment isn't valid for last row in table, but xref parsing has a special handler that
                # knows how many rows to read based off of the xrefindex row
                hint = pdfparserconstants.XREF_ROW
                authoritative = True
            case _: 
                hint = pdfparserconstants.UNKOWN

        if authoritative:
            return hint

    #ORDER OF RULES MATTER!

    #TRAILER
        if(currentLine.strip() == pdfparserconstants.TRAILER):
            return pdfparserconstants.TRAILER

    #XREFSTART
        if(currentLine.strip() == pdfparserconstants.XREFSTART):
            return pdfparserconstants.XREFSTART

    #XREF TABLE FIRST LINE
        if(currentLine.strip() == pdfparserconstants.XREF):
            return pdfparserconstants.XREF

    #OBJ START RULES
        #if current line contains "obj" but not "endobj", meaning it is the start of the obj section.
        #look for obj on current line
        objSearch = re.search('([0-9]+ [0-9]+ obj )', currentLine)
        objIndex = currentLine.find(pdfparserconstants.OBJ)
        #look for endobj on current line
        endobjIndex = currentLine.find(pdfparserconstants.ENDOBJ)
        #if current line contains "obj" but not "endobj", meaning it is the start of the obj section.
        if (objSearch != None and endobjIndex < 0) :
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
    def processStartTrailer(self):
        newObj = jobj.JObj('trailer')
        self.trailer = newObj
        return newObj
    def processObjMetaLine(self, currentLine, currentObj):

        if(currentLine.count('Embedded') > 0):
            x = 1

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
    def removeFirstPatternFromString(self, word, pattern):
        newWord = ""
        span = re.search(re.escape(pattern), word).span()
        newWord = word[0:span[0]] + word[span[1]:len(word)]
        return newWord

    def parseMetaObject(self, metaLine, sanityCheck):
        
        #if(metaLine.count('65 0 R') > 0):
        #    x = 1

        #only allow 100 levels of recursivity
        if(sanityCheck > 100):
            return None

        sanityCheck = sanityCheck + 1

        newMetaObj = jobj.JObj("meta")
        #find the end of the meta obj
        endOfMetaObjIndex = self.findEndOfObject(metaLine)
        #identify leftover on the line after end of object. most often demarcation of stream
        leftOver = ""
        if(endOfMetaObjIndex < len(metaLine)):
            #add two for FF
            leftOver = metaLine[endOfMetaObjIndex + 2: len(metaLine)]
            #remove leftOver from metaLine. Only remove leftover if recursivivity is level 1
            if(sanityCheck < 20):
                #print("Removing left over from metaLine: " + leftOver)
                #metaLine = metaLine.replace(leftOver, "")
                metaLine = metaLine[0: endOfMetaObjIndex + 2]
                #determine if leftover is stream demarcation since it may not have a new line
                if(leftOver.find("stream") > -1):
                    newMetaObj.hasStream = True

        #assum first 2 chars are BB
        myword = metaLine[2 : endOfMetaObjIndex - 1]
        propLine = ""

        #check for any deeper meta's. There may be multiple trees per level, thus the While loop 
        while True:
            
            if(myword.count(pdfparserconstants.BB) <= 0):
                propLine = "notset"
                break
            
            mySubObj = jobj.JObj("sub-meta")    
            #more parsing needed since it's an object
            #identify and remove subObj's key
            keyEnd = myword.find(pdfparserconstants.BB)
            subObjKeyList = myword[0:keyEnd].split('/')
            #may not be first keyword, so split by '/' and take last key
            subObjKey = subObjKeyList[len(subObjKeyList)-1]
            
            #debug
            if(subObjKey == "Names" or subObjKey == ""):
                x = 1

            endPropLine = myword.find(subObjKey)
            propLine = propLine + myword[0:endPropLine]
            myword2 = myword[keyEnd:len(myword)]     
            endOfSubObj = self.findEndOfObject(myword2)
            myword3 = myword2[0:endOfSubObj+2]
            mySubObj = self.parseMetaObject(myword3, sanityCheck)
            newMetaObj.__setattr__(subObjKey, mySubObj)

            #fix.. cannot use replace here as it will remove other duplicate matches.
            #remove sub obj key and meta from metaline and myword
            #metaLine = metaLine.replace(subObjKey, '').replace(myword3,'')
            metaLine = self.removeFirstPatternFromString(metaLine, subObjKey)
            metaLine = self.removeFirstPatternFromString(metaLine, myword3)

            myword = self.removeFirstPatternFromString(myword, subObjKey)
            myword = self.removeFirstPatternFromString(myword, myword3)

            #look at rest of line
            endOfMetaObjIndex = self.findEndOfObject(myword)
            #plus two for BB
            myword = myword[endOfMetaObjIndex+2:len(myword)]

        
        #parse props
        if(propLine == "notset"):
            propLine = metaLine
        #need fix - if sub prop was added, it needs to be removed from propline

        subProps = propLine.split('/')
        propRuleInEffect = "none"
        propBuilder = ""
        for prop in subProps:
            prop = prop.strip()
            if(prop == pdfparserconstants.BB or prop == pdfparserconstants.FF or len(prop) == 0):
                continue

            if(propRuleInEffect == "BuildRule"):
                propRuleInEffect = "none"
                prop = propBuilder + " " + prop

            if(propRuleInEffect == "BuildRuleParen"):
                prop = propBuilder + prop
                if(prop.count(')') > 0):
                    propRuleInEffect = "none"

            if(propRuleInEffect == "BuildFromBracketedList"):
                prop = propBuilder + " " + prop
                if(prop.count(']') > 0):
                    propRuleInEffect = "none"

            #special prop rules - eventually should externalize these
            #TODO: add more prop rules where they make sense.  Type=Filter for example
            propTest = prop.lower()
            if(propTest == "type" 
                or propTest == "filter"
                or propTest == "filter["
                or propTest == "subtype"
                or propTest == "baseversion"):
                propRuleInEffect = "BuildRule"
                propBuilder = prop
            
            #common pattern where data is embedded inline
            #TODO, improve this with an algorithm that isn't so hard coded
            if(   prop.count("U(") > 0
               or prop.count("O(") > 0
               or prop.count("CheckSum(") > 0
               or prop.count("ModDate(") > 0
               or prop.count("Name(") > 0
               or prop.count("Date(") > 0
               or prop.count("Lang(") > 0
               or prop.count("Title(") > 0
               or prop.count("ActualText(") > 0
               or prop.count("CreationDate(") > 0):

                #check for close paren to make sure this crap closes
                if(prop.count(')') == 0):
                    propRuleInEffect = "BuildRuleParen"
                    propBuilder = prop

                prop = prop.replace('(', ' ').replace(')', '')

            #prop may contain a bracket list
            if(prop.count('[') == 1 and prop.count(']') == 0):
                propRuleInEffect = "BuildFromBracketedList"
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
    def processObjectStreamLine(self, unfilteredStreamLine, firstOffset, numberOfObjects, parentId):
        #parse id/offset pairs
        #Not all objects will be meta objects. some may be plain content, or reference lists, etc
        

        idOffsetPairs = unfilteredStreamLine[0:firstOffset]  # this should match firstOffset
        #remove any new lines
        idOffsetPairs = idOffsetPairs.replace('\n',' ')
        shardList = idOffsetPairs.split(' ')
        objRefList = []
        od = 0
        newObjRef = jobj.JObj(0)
        prevObjRef = None
        shardCount = 0
        for shard in shardList:
            if(len(shard.strip()) < 1):
                shardCount = shardCount + 1
                continue
            if(od == 0):
                newObjRef.id = shard
            else:
                newObjRef.start = int(shard) + firstOffset
                if(prevObjRef != None):
                    prevObjRef.end = newObjRef.start  
                objRefList.append(newObjRef)
                prevObjRef = newObjRef
                newObjRef = jobj.JObj(0)

            if(od == 0):
                od = 1
            else:
                od = 0

            if(shardCount == (numberOfObjects*2) - 1):
                prevObjRef.end = len(unfilteredStreamLine)

            shardCount = shardCount + 1
        
        for objRef in objRefList:
            objId = objRef.id
           
            metaLine = unfilteredStreamLine[objRef.start:objRef.end]
            firstBBpos = metaLine.find(pdfparserconstants.BB)
            currentObj = jobj.JObj(objId)
            currentObj.version = '0'
            if(firstBBpos >= 0):
                self.processObjMetaLine(metaLine, currentObj)
            else:
                currentObj.content = metaLine

            currentObj.fromObjectStream = True
            currentObj.objectStreamId = parentId
            self.objs.append(currentObj)
       
    def processRawLine(self, rawline, rlState, unfilterStreamFlag, fileStream):
        
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
            #debug
            if(rlState.rawlineCount == 18724):
                x = 1

            lineType = self.determineLineType(currentLine, rlState.lastLine, rlState.lastLineType, rlState.lastObj, rlState.lastMetaObj)

            match lineType:
                case "obj":
                    rlState.lastObj = rlState.currentObj
                    rlState.currentObj = self.processStartObjLine(currentLine)
                case "endobj":
                    if(rlState.lastLineType == pdfparserconstants.CONTENT):
                        rlState.currentObj.content = rlState.lastLine
                    rlState.prevObj = rlState.currentObj
                    rlState.isContinuation = False
                    #assign xref object, but only if not set
                    if(hasattr(rlState.currentObj, "meta") and hasattr(rlState.currentObj.meta, "Type") and (rlState.currentObj.meta.Type == "XRef")
                       and self.xrefObj == None):
                        self.xrefObj = rlState.currentObj

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
                    rlState.streamLineCount = rlState.streamLineCount + 1
                    rlState.fileStreamPointer = fileStream.tell()
                    #end stream is presumably always on a new line. no reason to iterate thru an object stream's cr lines
                    # "fast forward" if Length is available
                    #use xref fast forward, if not in xref mode since xreftable would not exist yet
                    if(rlState.mode == 'Normal'):
                        #TODO, remove xrefType check. may not matter if fastForward works the same way if xref table is mapped in a similar manner
                        #if(hasattr(self, "xrefType") and self.xrefType == "indirect"):
                        curOffset = fileStream.tell()
                        #print('current at offset: ' + str(curOffset))
                        ffOffset = xrefUtil.fastForward(curOffset, self.xreftable)

                        #need to back up the offset by a few bytes to capture the end of the object, so it can't back up farther than the current offset
                        modOffset = ffOffset - 50
                        if(modOffset > curOffset ):
                            bytesToRead = modOffset - curOffset
                            print('fast forwarding to offset: ' + str(ffOffset))
                            ffRaw = fileStream.read(bytesToRead)
                            rawline = rawline + ffRaw

                        rlState.lastLineType = lineType
                        rlState.lastLine = currentLine
                        break
                case "stream-start":
                    containsStreamStart = True
                    rlState.currentMetaObj.hasStream = True
                    rlState.currentObj.hasStream = True
                case "stream-end":
                    #flip this so stream is only processed once
                    #rlState.lastMetaObj.hasStream = False
                    #rlState.currentObj.hasStream = False
                    containsStreamEnd = True
                    rlState.streamLineCount = 0
                case "trailer":
                    rlState.lastObj = rlState.currentObj
                    rlState.currentObj = self.processStartTrailer()     
                case "trailer-cont":
                    rlState.isContinuation = True
                case "content":
                    rlState.isContinuation = True
                case "content-cont":
                    rlState.isContinuation = True
                case "xref":
                    if(rlState.mode == "xreftable"):
                        xreftable = jobj.JObj("xreftable")
                        xreftable.rows = []
                        xreftable.index = None
                        rlState.currentObj = xreftable
                        self.xreftable = xreftable
                case "xrefindex":
                    if(rlState.mode == "xreftable"):
                        xrefUtil.processOldXrefFixedFormatIndex(currentLine, rlState.currentObj)
                case "xrefrow":
                    if(rlState.mode == "xreftable"):
                        xrefUtil.processOldXrefFixedFormatRow(currentLine, rlState.currentObj)
                case "startxref":
                    pass
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
                rlState.streamObj.processStream(streamBuffer, self)
            
            hashl = md5()
            hashl.update(streamBuffer)
            rlState.currentObj.streamMd5 = hashl.hexdigest()

            rlState.streamPersist = None

        if(containsStreamStart):
            rlState.streamPersist = None
            rlState.streamObj = rlState.currentObj
