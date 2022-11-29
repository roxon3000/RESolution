
import jobj 

class PdfAnalyzer:
    def __init__(self, jsonObject):
        self.jDoc = jsonObject        
    

    def processTrailerHeirarchy(self):
        rawDoc = self.jDoc

        trailer = None
        #check for trailer object
        if(hasattr(rawDoc, 'trailer') and hasattr(rawDoc.trailer, 'meta')):
            trailer = rawDoc.trailer.meta
        else:
            #search for trailer equivalent object
            #TODO
            pass

        infoObj = self.parseObjDef(trailer.Info)
        rootObj = self.parseObjDef(trailer.Root)

    def parseObjDef(self, obj):
        newObj = jobj.JObj()

        newObj.objectNumber = obj[0]
        newObj.generationNumber = obj[1]

        return newObj
    def analyze(self):
        
        rawDoc = self.jDoc

        #create heirarchy from trailer or equivialent
        self.processTrailerHeirarchy()
        