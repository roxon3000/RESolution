
import jobj 
import pdfUtil
import json

from objectproxy import getProxy 

class PdfAnalyzer:
    def __init__(self, jsonObject):
        self.rawDoc = jsonObject      
        self.treeDoc = jobj.JObj()
        self.treeDoc.objectMap = {}
    
    def findTrailerObject(self):
        rcObj = None

        for obj in self.rawDoc.objs:
            if(hasattr(obj, "meta") and hasattr(obj.meta, "Root") and hasattr(obj.meta, "Info")):
                rcObj = obj
        return rcObj
    def processOrphans(self):
        if(self.treeDoc != None and self.treeDoc.objectMap != None):
            for obj in self.rawDoc.objs:
                if(self.treeDoc.objectMap.get(obj.id) == None):
                    print(obj.id + " not found, is orphan")
                    newObj = jobj.JObj()
                    newObj.objectNumber = obj.id
                    newObj.generationNumber = obj.version       
                    newObj.orphan = True
                    newObj.update(obj, pdfUtil.bruteForceMapper, self.treeDoc, self.rawDoc)
                    if(self.treeDoc.objectMap.get(obj.id) == None):
                        pdfUtil.addToObjectMap(self.treeDoc, newObj)

                    

    def processTrailerHeirarchy(self):
        rawDoc = self.rawDoc
        treeDoc = self.treeDoc 

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

        #def genericObjRefHandler(key, val, rawDoc, treeDoc, newObj, mapper):

        treeTrailer = jobj.JObj()
        treeTrailer.objectNumber = 'trailer'
        treeTrailer.generationNumber = '0'
        treeDoc.treeTrailer = treeTrailer
        treeTrailer.update(trailer, pdfUtil.trailerMapper, treeDoc, rawDoc)

        #pdfUtil.genericObjRefHandler('trailer', trailer, rawDoc, treeDoc, treeTrailer, pdfUtil.genericObjectMapper)
        #pdfUtil.genericObjRefHandler('poopy', trailer.Info, rawDoc, treeDoc, treeDoc, pdfUtil.infoMapper)

        """
        infoObjt = pdfUtil.parseObjDef(trailer.Info)
        rootObjt = pdfUtil.parseObjDef(trailer.Root)

        #find info object
        infoObjr = pdfUtil.findRawObj(rawDoc, infoObjt)
        rootObjr = pdfUtil.findRawObj(rawDoc, rootObjt)

        treeDoc.info = jobj.JObj()
        if(infoObjr != None):
            treeDoc.info.update(infoObjr, pdfUtil.infoMapper, treeDoc, rawDoc)
            treeDoc.info.objectNumber = infoObjr.id
            treeDoc.info.generationNumber = infoObjr.version
        else:
            treeDoc.info.message = "Info object was not found"

        treeDoc.root = jobj.JObj()
        if(rootObjr != None):
            treeDoc.root.update(rootObjr.meta, pdfUtil.rootMapper, treeDoc, rawDoc)
            treeDoc.root.objectNumber = rootObjr.id
            treeDoc.root.generationNumber = rootObjr.version

        else:
            treeDoc.root.message = "Root object was not found"

        """
    def analyze(self):
        
        rawDoc = self.rawDoc

        #create object map
        #TODO - need to create object map first... should have done this to begin with.

        #create heirarchy from trailer or equivialent. This doc is used for object tree visualization and inspection
        #also performs some defacto validation. TODO needs error handling
        self.processTrailerHeirarchy()

        self.processOrphans()
        """
        proxy = {'$ref' : "#/objectMap/" + self.treeDoc.info.objectNumber}

        #proxy.ref = "#/objectMap/" + self.treeDoc.info.objectNumber

        testdoc =  {
            "data": ["a", "b", "c", {"id": "12"}],
            "objectMap" : 
                    {
                        "1234" : {"$ref" : "#/objectMap/14"}
                    }
                ,
            "more" : { 
                "title" : "real data",
                "producer" : getProxy("14")
                }
        }

        testdoc['objectMap'][self.treeDoc.info.objectNumber] = self.treeDoc.info

        testo = jsonref.replace_refs(testdoc)
        print(testo)
        
        
        #put object map into its own doc and clear from treeDoc
        self.objectMap = testdoc
        #self.treeDoc.objectMap = testo
        """

        #write output files
        outputFile = "objecttree.json"
        with open(outputFile, 'w', encoding="ascii", errors="surrogateescape") as fw:
                  
            fw.write(json.dumps(self.treeDoc, default=vars))
            #test = vars(treeDoc)
            #json.dump(test, fw)

        fw.close()

        """
        outputFile = "objectmap.json"
        with open(outputFile, 'w', encoding="ascii", errors="surrogateescape") as fw:
                  
            fw.write(json.dumps(self.objectMap, default=vars))
            #test = vars(treeDoc)
            #json.dump(test, fw)

        fw.close()

        """
        

        