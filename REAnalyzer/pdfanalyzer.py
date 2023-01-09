
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

    def processTextContent(self):                
        objectMap = self.treeDoc.objectMap
        for objId in  self.treeDoc.objectMap:
            obj = objectMap.get(objId)
            if(hasattr(obj, "textContent") and obj.textContent == True):
                pdfUtil.processTextline(obj.unfilteredStream, obj, self.treeDoc.toUnicode)
            else:
                continue

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
                #obj.appliedRules = []
                for rule in rulesDoc.rules:
                    result = applyRule(rule, obj)
                    if(result != None):
                        #adding applied results into the object map is overkill.. makes the files too large and is unnecessary. 
                        #  leaving uncommented for now in case I want to add it back.
                       #obj.appliedRules.append(result)                    
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

        self.processTextContent()

        self.executeRules()
        

        #write output files
        pre = self.treeDoc.id
        if(hasattr(rawDoc, "fileName") and len(rawDoc.fileName) > 0):
            pre = rawDoc.fileName
            #if file name contains folders, find and use actual file name
            if(pre.count('/') > 0 ):
                fileSplit = pre.split('/')
                pre = fileSplit[len(fileSplit)-1]

        outputFile = "./output/" + pre + ".obj.json"
        with open(outputFile, 'w', encoding="ascii", errors="surrogateescape") as fw:
                  
            fw.write(json.dumps(self.treeDoc, default=vars))
            #test = vars(treeDoc)
            #json.dump(test, fw)

            


        outputFile = "./output/" + pre + ".dat.json"
        with open(outputFile, 'w', encoding="ascii", errors="surrogateescape") as fw:        
            fw.write(json.dumps(self.rulesSummary, default=vars))
        