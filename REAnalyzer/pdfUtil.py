import jobj
import re 
from objectproxy import getProxy
import sys 
from itertools import count
import unicodedata

OBJ_REF_REGEX = '([0-9]+ [0-9]+ R)'

def trailerMapper(newObj, obj, treeDoc, rawDoc):
    items = None
    if(hasattr(obj, "_asdict")):
        items = obj._asdict().items()
    else:
        items = obj.__dict__.items()

    if(items != None):
        for key, val in items:

            match key:
                case "Info" :
                    if(genericObjRefHandler(key, val, rawDoc, treeDoc, newObj, bruteForceMapper) == False):
                        newObj.__setattr__(key, join(" " , obj._asdict().get(key)))
                case "Root" :
                    if(genericObjRefHandler(key, val, rawDoc, treeDoc, newObj, bruteForceMapper) == False):
                        newObj.__setattr__(key, join(" " , obj._asdict().get(key)))
                case "id" | "version":
                    pass 
                case "version":
                    newObj.generationNumber = val
                case _:
                    newObj.__setattr__(key, val)

def genericMapper(newObj, obj, treeDoc, rawDoc):

    #check for meta (flatten)
    if(hasattr(obj, "meta") and hasattr(obj.meta, "_asdict")):
        genericObjectMapper(obj.meta, rawDoc, treeDoc, newObj)
    
    genericObjectMapper(obj, rawDoc, treeDoc, newObj)

def genericListMapper(newList, rawList, treeDoc, rawDoc):
    if(isinstance(rawList, list) == False):
        raise Exception("object must be a list in a list mapper")

    for objr in rawList:
         genericObjRefHandlerForListItem(objr, rawDoc, treeDoc, newList, bruteForceMapper)
         #if( genericObjRefHandler(key, val, rawDoc, treeDoc, newObj, bruteForceMapper) == False):
         #   newObj.__setattr__(key, val)
         #newObj.update(objr, bruteForceMapper, treeDoc, rawDoc)
         #newList.append(newObj)

def bruteForceMapper(newObj, obj, treeDoc, rawDoc):
    


    #check for list
    if(isinstance(obj, list)):
        print("bruteForceMapper List Count" + str(len(obj)))
        genericListMapper(newObj, obj, treeDoc, rawDoc)
    else:
        poolObj = treeDoc.objectMap.get(obj.id)
        if(poolObj != None):
            if(hasattr(poolObj, "mapped") and poolObj.mapped == True):
                #return
                pass
            else:
                poolObj.mapped = True

        #check for meta (flatten)
        print("bruteForceMapper obj.id=" + obj.id)
        if(hasattr(obj, "meta") and hasattr(obj.meta, "_asdict")):
            bruteForceObjectMapper(obj.meta, rawDoc, treeDoc, newObj)
    
        bruteForceObjectMapper(obj, rawDoc, treeDoc, newObj)

       
def processTextline(textLine, textObj, uniObj):
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
            tjArrWord = re.findall("(?<=<)[A-Za-z0-9]+(?=>)", tjWord[tjStart:tjEnd])
            translated = []
            if( tjArrWord != None and len(tjArrWord) > 0):
                for code in tjArrWord:
                    translated.append(translateUnicode(uniObj, code))
                textObj.translatedContent = "".join(translated)
                
               

    return None
def translateUnicode(uniObj, code):
    if(uniObj == None):
        return None

    if(uniObj.bfCharObj != None and uniObj.bfCharObj.charMapping != None and len(uniObj.bfCharObj.charMapping) > 0):
        charMapping = uniObj.bfCharObj.charMapping
        for mapping in charMapping:
            testm = mapping.baseFontCode.replace("<","").replace(">","")
            if(testm == code):
                outChar = mapping.rearrangeFontCode.replace("<","").replace(">","")
                return chr(int(outChar,16))

    return code

def bruteForceObjectMapper(obj, rawDoc, treeDoc, newObj):
    items = None
    if(hasattr(obj, "_asdict")):
        items = obj._asdict().items()
    else:
        items = obj.__dict__.items()

    #debug
    if(obj.id == "6"):
        x=2

    if(items != None):
        for key, val in items:
            if(str(val).isprintable()):
                #print('brute force at key=' + key + ' value=' + str(val))
                pass
            match key:
                case "id" | "version" | "meta":
                    pass 
                case "version":
                    newObj.generationNumber = val
                case "K" | "Parent" | "raw" :
                    #K is causing problems with large lists.. currently banned. Parent and raw banned to prevent recursive loops
                    newObj.__setattr__(key, val)
                case _:
                    if(hasattr(val,'_fields')):
                        subObj = jobj.JObj()
                        subObj.id = key + obj.id
                        subObj.update(val, bruteForceMapper, treeDoc, rawDoc)
                        newObj.__setattr__(key, subObj)
                    elif(isinstance(val, list) and len(val) > 0 and hasattr(val[0], '_fields')):
                        newObj.__setattr__(key, [])
                        bruteForceMapper(newObj.getAttr(key), val, treeDoc, rawDoc)
                    else:
                        if( genericObjRefHandler(key, val, rawDoc, treeDoc, newObj, bruteForceMapper) == False):
                            newObj.__setattr__(key, val)

    print("bruteForceObjectMapper obj.id=" + obj.id)
    

def genericObjectMapper(obj, rawDoc, treeDoc, newObj):
    items = None
    if(hasattr(obj, "_asdict")):
        items = obj._asdict().items()
    else:
        items = obj.__dict__.items()

    for key, val in items:
        match key:
            case "Contents" | "Kids" | "Length" | "ToUnicode" :
                genericObjRefHandler(key, val, rawDoc, treeDoc, newObj, genericMapper)
            case "Resources":
                genericObjRefHandler(key, val, rawDoc, treeDoc, newObj, bruteForceMapper)
            case "id" | "version":
                pass 
            case "version":
                newObj.generationNumber = val
            case "meta":
                pass
            case _:
                newObj.__setattr__(key, val)

def infoMapper(newObj, obj, treeDoc, rawDoc):

    #check for meta
    if(hasattr(obj, "meta") and hasattr(obj.meta, "_asdict")):
        obj = obj.meta

    items = None
    if(hasattr(obj, "_asdict")):
        items = obj._asdict().items()
    else:
        items = obj.__dict__.items()

    for key, val in items:
            match key:
                case "Creator" | "Producer" | "Title" | "Creator" | "CreationDate" | "ModDate" | "Keywords" | "AAPL_Keywords" :
                    if(genericObjRefHandler(key, val, rawDoc, treeDoc, newObj, genericMapper) == False):
                        newObj.__setattr__(key, join(" " , obj._asdict().get(key)))
                case "id" | "version":
                    pass 
                case "version":
                    newObj.generationNumber = val
                case _:
                    newObj.__setattr__(key, val)


def rootMapper(newObj, obj, treeDoc, rawDoc):
    #check for meta
    if(hasattr(obj, "meta") and hasattr(obj.meta, "_asdict")):
        obj = obj.meta

    items = None
    if(hasattr(obj, "_asdict")):
        items = obj._asdict().items()
    else:
        items = obj.__dict__.items()

    for key, val in items:

        match key:
            case "Pages":
                genericObjRefHandler(key, val, rawDoc, treeDoc, newObj,bruteForceMapper)
            case "Title":
                newObj.Title = join(" " , obj.Title)
            case "id" | "version":
                pass 
            case _:
                newObj.__setattr__(key, val)

def addToObjectMap(treeDoc, obj):
    treeDoc.objectMap[obj.objectNumber] = obj

def genericObjRefHandler(key, val, rawDoc, treeDoc, newObj, mapper):

    objt = parseObjDef(val)
    if(objt != None):
        objr = findRawObj(rawDoc, objt)        
        if(objr != None):
            if(isinstance(objr, list) == False):
                childObj = jobj.JObj()
                childObj.objectNumber = objr.id
                childObj.generationNumber = objr.version 
                if(key == "Contents"):
                    childObj.textContent = True
                if(key == "ToUnicode"):
                    childObj.toUnicode = True
                    treeDoc.toUnicode = childObj
                if ( (objr.id in treeDoc.objectMap) == False):
                    addToObjectMap(treeDoc, childObj)
                newObj.__setattr__(key, getProxy(childObj.objectNumber))
                childObj.update(objr, mapper, treeDoc, rawDoc)
            else:
                newObj.__setattr__(key, [])
                mapper(newObj.getAttr(key), objr, treeDoc, rawDoc)
            return True
        else:
            newObj.__setattr__(key, key + " object was not found")
            return False

    return False

def genericObjRefHandlerForListItem(val, rawDoc, treeDoc, newList, mapper):

    
    if(val != None):
        if(isinstance(val, list) == False):
            childObj = jobj.JObj()
            childObj.objectNumber = val.id
            #check for version, if it is not there then it's not an object ref
            if(hasattr(val, "version")):
                childObj.generationNumber = val.version       
                if ( (val.id in treeDoc.objectMap) == False):
                    addToObjectMap(treeDoc, childObj)
                newList.append(getProxy(childObj.objectNumber))
            else:
                newList.append(childObj)

            childObj.update(val, mapper, treeDoc, rawDoc)
        else:
            newList.append(val)
        return True
    else:
        return False


def findRawObj(rawDoc, tObject):

    searchList = [] 
    rcList = [] 

    if(isinstance(tObject, list) == False):
        searchList.append(tObject)
    else:
        searchList = tObject

    for searchObj in searchList:

        for obj in rawDoc.objs:
            if(obj.id == searchObj.objectNumber and obj.version == searchObj.generationNumber):
                rcList.append(obj)
                break

    if(len(rcList) > 1):
        return rcList
    elif(len(rcList) == 1):
        return rcList[0]
    else:
        return None

def join(delimiter, listIn):
    if(isinstance(listIn, list) and len(listIn) > 0):
        return delimiter.join(listIn)

    return listIn
    
def parseObjDef(obj):
    newObj = None

    rcList = []

    if(isinstance(obj, str)):
        #find all obj ref patterns. works for one to many in a string
        objRefs = re.findall(OBJ_REF_REGEX, obj)
        for ref in objRefs:
            splitObj = ref.split(' ')
            newObj = jobj.JObj()
            newObj.objectNumber = splitObj[0]
            newObj.generationNumber = splitObj[1]
            rcList.append(newObj)

    elif(isinstance(obj, list) and len(obj) > 0):
        #determine if it's a list of full ref ids, or decomposed (10,0,R,11,0,R) vs ('10 0 R','11 0 R', etc)
        if(isinstance(obj[0],str )):
            refMatch = re.search(OBJ_REF_REGEX, obj[0])
            #if found, then obj is a list of full obj refs.
            if(refMatch != None):
                #do processing of full refs
                for ref in obj:
                    splitObj = ref.split(' ')
                    newObj = jobj.JObj()
                    newObj.objectNumber = splitObj[0]
                    newObj.generationNumber = splitObj[1]
                    rcList.append(newObj)                
            else:
                if(len(obj) > 2 and obj[0].isnumeric() and obj[1].isnumeric() and obj[2].strip() == "R"):
                    #do processing of decomposed
                    for i in range(0, len(obj), 3):
                        newObj = jobj.JObj()
                        newObj.objectNumber = obj[i]
                        newObj.generationNumber = obj[i + 1]
                        rcList.append(newObj)                

    if(len(rcList) > 1):
        return rcList
    elif(len(rcList) == 1):
        return rcList[0]
    else:
        return None

    
def stack_size2a(size=2):
    """Get stack size for caller's frame.
    """
    frame = sys._getframe(size)

    for size in count(size):
        frame = frame.f_back
        if not frame:
            return size