
import jobj 
import pdfUtil

class PdfAnalyzer:
    def __init__(self, jsonObject):
        self.rawDoc = jsonObject      
        self.newDoc = jobj.JObj()
    

    def processTrailerHeirarchy(self):
        rawDoc = self.rawDoc
        newDoc = self.newDoc 

        trailer = None
        #check for trailer object
        if(hasattr(rawDoc, 'trailer') and hasattr(rawDoc.trailer, 'meta')):
            trailer = rawDoc.trailer.meta
        else:
            #search for trailer equivalent object
            #TODO
            pass

        infoObjt = pdfUtil.parseObjDef(trailer.Info)
        rootObjt = pdfUtil.parseObjDef(trailer.Root)

        #find info object
        infoObjr = pdfUtil.findRawObj(rawDoc, infoObjt)
        rootObjr = pdfUtil.findRawObj(rawDoc, rootObjt)

        newDoc.info = jobj.JObj()
        newDoc.info.update(infoObjr, pdfUtil.infoMapper, newDoc, rawDoc)
        newDoc.info.objectNumber = infoObjr.id
        newDoc.info.generationNumber = infoObjr.version

        newDoc.root = jobj.JObj()
        newDoc.root.update(rootObjr.meta, pdfUtil.rootMapper, newDoc, rawDoc)
        newDoc.root.objectNumber = rootObjr.id
        newDoc.root.generationNumber = rootObjr.version

        #clean objects
        #infoObjc = pdfUtil.cleanInfo(newDoc.info)

        x =1


    def analyze(self):
        
        rawDoc = self.rawDoc

        #create heirarchy from trailer or equivialent
        self.processTrailerHeirarchy()

        