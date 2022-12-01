import jobj
import re 

OBJ_REF_REGEX = '([0-9]+ [0-9]+ R)'

def genericMapper(newObj, obj, newDoc, rawDoc):

    #check for meta (flatten)
    if(hasattr(obj, "meta") and hasattr(obj.meta, "_asdict")):
        genericObjectMapper(obj.meta, rawDoc, newDoc, newObj)
    
    genericObjectMapper(obj, rawDoc, newDoc, newObj)

def genericListMapper(newList, rawList, newDoc, rawDoc):
    if(isinstance(rawList, list) == False):
        raise Exception("object must be a list in a list mapper")

    for objr in rawList:
         newObj = jobj.JObj()
         newObj.objectNumber = objr.id
         newObj.generationNumber = objr.version       
         newObj.update(objr, genericMapper, newDoc, rawDoc)
         newList.append(newObj)

def genericObjectMapper(obj, rawDoc, newDoc, newObj):
    if(hasattr(obj, "_asdict")):
        for key, val in obj._asdict().items():

            if(key == "unfilteredStream"):
                x = 1
            match key:
                case "Contents" | "Kids":
                    genericObjRefHandler(key, val, rawDoc, newDoc, newObj)
                case "meta":
                    pass
                case _:
                    newObj.__setattr__(key, val)

def infoMapper(newObj, obj, newDoc, rawDoc):

    #check for meta
    if(hasattr(obj, "meta") and hasattr(obj.meta, "_asdict")):
        obj = obj.meta

    if(hasattr(obj, "_asdict")):
        for key, val in obj._asdict().items():

            match key:
                case "Producer":
                    prodObjt = parseObjDef(val)
                    if(prodObjt != None):
                        prodObjr = findRawObj(rawDoc, prodObjt)
                        newObj.Producer = jobj.JObj()
                        newObj.Producer.update(prodObjr, genericMapper, newDoc, rawDoc)
                    else:
                        newObj.Producer = join(" ", obj.Producer)
                case "Title":
                    newObj.Title = join(" " , obj.Title)
                case "id":
                    newObj.objectNumber = val
                case "version":
                    newObj.generationNumber = val
                case _:
                    newObj.__setattr__(key, val)


def rootMapper(newObj, obj, newDoc, rawDoc):

    for key, val in obj._asdict().items():

        match key:
            case "Pages":
                genericObjRefHandler(key, val, rawDoc, newDoc, newObj)
            case "Title":
                newObj.Title = join(" " , obj.Title)
            case _:
                newObj.__setattr__(key, val)

def genericObjRefHandler(key, val, rawDoc, newDoc, newObj):
    objt = parseObjDef(val)
    if(objt != None):
        objr = findRawObj(rawDoc, objt)        
        if(objr != None):
            if(isinstance(objr, list) == False):
                childObj = jobj.JObj()
                childObj.objectNumber = objr.id
                childObj.generationNumber = objr.version       
                newObj.__setattr__(key, childObj)
                newObj.getAttr(key).update(objr, genericMapper, newDoc, rawDoc)
            else:
                newObj.__setattr__(key, [])
                genericListMapper(newObj.getAttr(key), objr, newDoc, rawDoc)
            return True
        else:
            newObj.__setattr__(key, key + " object was not found")
            return False

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
                if(len(obj) > 2 and obj[0].isnumeric() and obj[1].isnumeric() and obj[2].string() == "R"):
                    #do processing of decomposed
                    for i in range(0, len(obj), 3):
                        newObj = jobj.JObj()
                        newObj.objectNumber = obj[i]
                        newObj.generationNumber = splitObj[i + 1]
                        rcList.append(newObj)                

    if(len(rcList) > 1):
        return rcList
    elif(len(rcList) == 1):
        return rcList[0]
    else:
        return obj

    
