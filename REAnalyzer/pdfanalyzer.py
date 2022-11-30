
import jobj 
import pdfUtil
import json

class PdfAnalyzer:
    def __init__(self, jsonObject):
        self.rawDoc = jsonObject      
        self.newDoc = jobj.JObj()
    
    def findTrailerObject(self):
        rcObj = None

        for obj in self.rawDoc.objs:
            if(hasattr(obj, "meta") and hasattr(obj.meta, "Root") and hasattr(obj.meta, "Info")):
                rcObj = obj
        return rcObj

    def processTrailerHeirarchy(self):
        rawDoc = self.rawDoc
        newDoc = self.newDoc 

        trailer = None
        #check for trailer object
        if(hasattr(rawDoc, 'trailer') and hasattr(rawDoc.trailer, 'meta')):
            trailer = rawDoc.trailer.meta
        else:
            #search for trailer equivalent object
            #find obj with highest ID
            trObj = self.findTrailerObject()
            if(trObj != None):
                trailer = trObj.meta
            else:
                raise Exception("Trailer Object Not Found in PDF")

        infoObjt = pdfUtil.parseObjDef(trailer.Info)
        rootObjt = pdfUtil.parseObjDef(trailer.Root)

        #find info object
        infoObjr = pdfUtil.findRawObj(rawDoc, infoObjt)
        rootObjr = pdfUtil.findRawObj(rawDoc, rootObjt)

        newDoc.info = jobj.JObj()
        if(infoObjr != None):
            newDoc.info.update(infoObjr, pdfUtil.infoMapper, newDoc, rawDoc)
            newDoc.info.objectNumber = infoObjr.id
            newDoc.info.generationNumber = infoObjr.version
        else:
            newDoc.info.message = "Info object was not found"

        newDoc.root = jobj.JObj()
        if(rootObjr != None):
            newDoc.root.update(rootObjr.meta, pdfUtil.rootMapper, newDoc, rawDoc)
            newDoc.root.objectNumber = rootObjr.id
            newDoc.root.generationNumber = rootObjr.version
        else:
            newDoc.root.message = "Root object was not found"

        #clean objects
        #infoObjc = pdfUtil.cleanInfo(newDoc.info)

        x =1
        outputFile = "trailer.debug.json"
        with open(outputFile, 'w', encoding="ascii", errors="surrogateescape") as fw:
       
            fw.write(json.dumps(newDoc, default=vars))
            #test = vars(newDoc)
            #json.dump(test, fw)

        fw.close()



    def analyze(self):
        
        rawDoc = self.rawDoc

        #create heirarchy from trailer or equivialent
        self.processTrailerHeirarchy()

        