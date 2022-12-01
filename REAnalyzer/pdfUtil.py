import jobj

def genericMapper(newObj, obj, newDoc, rawDoc):

    #check for meta (flatten)
    if(hasattr(obj, "meta") and hasattr(obj.meta, "_asdict")):
        genericObjectMapper(obj.meta, rawDoc, newDoc, newObj)
    
    genericObjectMapper(obj, rawDoc, newDoc, newObj)

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
            childObj = jobj.JObj()
            childObj.objectNumber = objr.id
            childObj.generationNumber = objr.version
            newObj.__setattr__(key, childObj)
            
            newObj.getAttr(key).update(objr, genericMapper, newDoc, rawDoc)
            return True
        else:
            newObj.__setattr__(key, key + " object was not found")
            return False

    return False

def findRawObj(rawDoc, tObject):

    for obj in rawDoc.objs:
        if(obj.id == tObject.objectNumber and obj.version == tObject.generationNumber):
            return obj

    return None

def join(delimiter, listIn):
    if(isinstance(listIn, list) and len(listIn) > 0):
        return delimiter.join(listIn)

    return listIn
    
def parseObjDef(obj):
    newObj = None

    if(isinstance(obj, list)):
        obj= join(' ', obj)

    if(isinstance(obj, str)):
        splitObj = obj.split(' ')

        if(len(splitObj) > 2 and splitObj[0].isnumeric() and splitObj[1].isnumeric() and splitObj[2] == 'R'):
            newObj = jobj.JObj()
            newObj.objectNumber = splitObj[0]
            newObj.generationNumber = splitObj[1]

    return newObj
