import jobj

def genericMapper(newObj, obj, newDoc, rawDoc):

    #check for meta
    if(hasattr(obj, "meta") and hasattr(obj.meta, "_asdict")):
        obj = obj.meta

    if(hasattr(obj, "_asdict")):
        for key, val in obj._asdict().items():

            match key:
                case "meta":
                    pass
                case _:
                    newObj.__setattr__(key.lower(), val)

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
                        newObj.producer = jobj.JObj()
                        newObj.producer.update(prodObjr, genericMapper, newDoc, rawDoc)
                    else:
                        newObj.producer = join(" ", obj.Producer)
                case "Title":
                    newObj.title = join(" " , obj.Title)
                case "id":
                    newObj.objectNumber = val
                case "version":
                    newObj.generationNumber = val
                case _:
                    newObj.__setattr__(key.lower(), val)


def rootMapper(newObj, obj, newDoc, rawDoc):

    for key, val in obj._asdict().items():

        match key:
            case "Pages":
                pagesObjt = parseObjDef(val)
                if(pagesObjt != None):
                    pagesObjr = findRawObj(rawDoc, pagesObjt)
                    newObj.pages = jobj.JObj()
                    if(pagesObjr != None):
                        newObj.pages.update(pagesObjr.meta, infoMapper, newDoc, rawDoc)
                    else:
                        newObj.pages.message = "Pages object was not found"
            case "Title":
                newObj.title = join(" " , obj.Title)
            case _:
                newObj.__setattr__(key.lower(), val)

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

    splitObj = obj.split(' ')

    if( splitObj[0].isnumeric() and splitObj[1].isnumeric() and splitObj[2] == 'R'):
        newObj = jobj.JObj()
        newObj.objectNumber = splitObj[0]
        newObj.generationNumber = splitObj[1]

    return newObj
