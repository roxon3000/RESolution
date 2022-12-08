
import jobj 
import pdfUtil
import json
import analyzer
from collections import namedtuple
from objectproxy import getProxy 
from rulesengine import applyRule 

class PdfAnalyzer:
    def __init__(self, jsonObject):
        self.rawDoc = jsonObject      
        self.treeDoc = jobj.JObj()
        self.treeDoc.objectMap = {}
        self.rules = None
        self.rulesSummary = jobj.JObj()
        self.rulesSummary.matchCount = 0

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
    
    def executeRules(self):
        #made decision to no run rules during heirarchy or orphan processing in order to simplify rules processing.  Decision will have a minor impact on performance.
        #load and process rules
        with open('rules/pdfrules.json', 'r') as tr:
            
            rulesDoc = json.load(tr, object_hook=analyzer.customDocDecoder)
            self.rules = rulesDoc
            objectMap = self.treeDoc.objectMap
            for objId in  self.treeDoc.objectMap:
                obj = objectMap.get(objId)
                #obj.__setattr__('appliedRules',[])
                obj.appliedRules = []
                for rule in rulesDoc.rules:
                    result = applyRule(rule, obj)
                    if(result != None):
                        obj.appliedRules.append(result)                    
                        self.recordInRuleSummary(obj, result)

        tr.close()
    
    def recordInRuleSummary(self, obj, result):
        rule = result.appliedRule
        if(result.match == True):
            self.rulesSummary.matchCount = self.rulesSummary.matchCount + 1
            if(hasattr(self.rulesSummary, rule['id']) == False):
                ruleSummaryObj = jobj.JObj()
                ruleSummaryObj.objs = []
                self.rulesSummary.__setattr__(rule['id'], ruleSummaryObj)
            self.rulesSummary.getAttr(rule['id']).objs.append(getProxy(obj.objectNumber))

    def analyze(self):
        
        rawDoc = self.rawDoc

        #create heirarchy from trailer or equivialent. This doc is used for object tree visualization and inspection
        #also performs some defacto validation. TODO needs error handling
        self.processTrailerHeirarchy()

        self.processOrphans()

        self.executeRules()
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


        outputFile = "rulessummary.json"
        with open(outputFile, 'w', encoding="ascii", errors="surrogateescape") as fw:        
            fw.write(json.dumps(self.rulesSummary, default=vars))
        fw.close()  
        