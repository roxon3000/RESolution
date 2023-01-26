import objectUtil
import re

def processCID(obj, myDoc):
    if(hasattr(obj,"hasStream") and 
       obj.hasStream == True and 
       obj.unfilteredStream != None and 
       len(obj.unfilteredStream) > 7 and 
       obj.unfilteredStream[0:8] == "/CIDInit"):
            cidInitObj = objectUtil.JObj("cidinit" + obj.id)
            #add meta tags to enable object processing
            #myDoc.processObjMetaLine("<< " + obj.unfilteredStream + " >>", cidInitObj)
            #print(cidInitObj)
            bfCharObj = objectUtil.JObj('bfchar')
            bfRangeObj = objectUtil.JObj('bfrange')
            processCIDline(obj.unfilteredStream, bfCharObj, bfRangeObj)
            obj.bfCharObj = bfCharObj
            obj.bfRangeObj = bfRangeObj


                
        
    return None

def processCIDline(cidLine, bfCharObj, bfRangeObj):
    #CID line will contain a mix of meta object data and CID script
    # for simplicity in initial release, code is only focusing base font char mappings (beginbfchar/endbfchar) and base font range mappings (beginbfrange/endbfrange)

    BEGINBFCHAR = "beginbfchar"
    ENDBFCHAR = "endbfchar"
    BEGINBFRANGE = "beginbfrange"
    ENDBFRANGE = "endbfrange"
    
    bcharIndex = cidLine.find(BEGINBFCHAR)
    brangeIndex = cidLine.find(BEGINBFRANGE)
    if( bcharIndex >= 0 ):
        echarIndex = cidLine.find(ENDBFCHAR)
        bfCharWord = cidLine[bcharIndex + len(BEGINBFCHAR):echarIndex].strip()
        charList = bfCharWord.split()
        print(charList)
        if(bfCharObj != None):
            bfCharObj.charMapping = [] 
            mapObj = objectUtil.JObj('cid' + str(0))
            for i in range(0, len(charList)):

                if( i % 2 == 0):
                    mapObj.baseFontCode = charList[i]                    
                else:
                    mapObj.rearrangeFontCode = charList[i]
                    bfCharObj.charMapping.append(mapObj)
                    mapObj = objectUtil.JObj('cid' + str(i))
    if( brangeIndex >= 0):
        erangeIndex = cidLine.find(ENDBFRANGE)
        bfRangeWord = cidLine[brangeIndex + len(BEGINBFRANGE):erangeIndex].strip()
        charList = bfRangeWord.split()
        print(charList)
        if(bfRangeObj != None):
            bfRangeObj.charMapping = [] 
            mapObj = objectUtil.JObj('cid' + str(0))
            skipNext = False
            for i in range(0, len(charList)):
                if(skipNext):
                    skipNext = False
                    continue
                if( i % 3 == 0):
                    mapObj.baseRangeStart = charList[i]                    
                    mapObj.baseRangeEnd = charList[i+1] 
                    skipNext = True
                else:
                    mapObj.rearrangeFontCode = charList[i]
                    bfRangeObj.charMapping.append(mapObj)
                    mapObj = objectUtil.JObj('cid' + str(i))                

    return None

def processTextline(textLine, textObj):
    #CID line will contain a mix of meta object data and CID script
    # for simplicity in initial release, code is only focusing base font char mappings (beginbfchar/endbfchar) and base font range mappings (beginbfrange/endbfrange)

    BEGINTEXTOBJECT = "BT"
    ENDTEXTOBJECT = "ET"
    TXTARRAY = "TJ"
    TXTGROUP = "Tj"
  
    btIndex = textLine.find(BEGINTEXTOBJECT)
    if( btIndex >= 0 ):
        etIndex = textLine.find(ENDTEXTOBJECT)
        textObjWord = textLine[btIndex + len(BEGINTEXTOBJECT):etIndex].strip()
        tjArrIndex = textObjWord.find(TXTARRAY)
        if( tjArrIndex >= 0):
            tjWord = textObjWord[0:tjArrIndex + len(TXTARRAY)].strip()
            tjStart = tjWord.rfind('[')
            tjEnd = tjWord.rfind(']')
            tjArrWord = re.findAll("(?<=<)[A-Za-z0-9]+(?=>)", tjWord[tjStart:tjEnd])
            if( tjArrWord != None and len(tjArrWord) > 0):
                textObj.textArray = tjArrWord

                

    return None