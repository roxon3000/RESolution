

def getProxy(id, pool="objectMap"):
    return {"$ref" : "#/" + pool + "/" + id, "id" : id}

