from base64 import b85decode
from cmath import isnan
import pdfparserconstants
import zlib
import base64
import xrefUtil

class JObj:
    def __init__(meo, id):
        meo.id = id
        meo.hasStream = False
        

    def __setattr__(self, name, value):
        newVal = value

        name = self.cleanValue(name, 'key')

        #don't clean streams
        if(name == 'unfilteredStream' or name == 'stream'):
            pass
        else:
            newVal = self.cleanValue(value, 'val')
            
        self.__dict__[name] = newVal

    def mutate(self, word):
        word = self.parseBracketedList(word)
        if(self.propRulesCheck(word)): 
            #replace \n \r \r\n with ' '
            word = word.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ').replace('[','').replace(']', '').replace(pdfparserconstants.FF, '').replace(pdfparserconstants.BB, '')
            keyval = word.split(' ')
            key = self.cleanValue(keyval[0], 'key')
            if(len(keyval) == 2):
                val = self.cleanValue(keyval[1], 'val')                   
                self.__setattr__(key, val)
            elif(len(keyval) == 1):
                self.__setattr__(key, True)
            else:
                keyval.pop(0)
                keyval = self.cleanValue(keyval, 'val')
                #check to see if value is a single obj ref. if so, join to one value.  If list, join to one value per element
                keyval = self.objectReferenceCheck(keyval)
                self.__setattr__(key, keyval)
    def objectReferenceCheck(self, valList):
        newList = valList
        #check for pattern that matches obj ref "<num> <num> R"
        if(isinstance(valList, list) and len(valList) > 2):
            if( valList[0].isnumeric() and valList[1].isnumeric() and valList[2] == 'R'):
                newList = " ".join(valList).split('R')
                #pop last element
                newList.pop(len(newList)-1)
                #add back the R for fun and jic
                for i in range(len(newList)):
                    newList[i] = newList[i].lstrip() + "R"

        return newList

    def propRulesCheck(self, prop):
        
        #don't add empty properties
        if(len(prop) < 1):
            #ignore
            return False

        if(prop.strip() == pdfparserconstants.BB):
            return False

        return True
    def parseBracketedList(self,word):
        #ensure there is a space before open bracket
        #find open bracked
        bracketIndex = word.find('[')
        if(bracketIndex > 0 and word[bracketIndex-1:bracketIndex] != ' '):
            #TODO: this will break if there are sublists
            bsplit = word.split('[')
            newVal = bsplit[0] + ' ' + bsplit[1]
            newVal = newVal.replace(']','')
            word = newVal                
        return word
    def cleanValue(self, value, source):
        newVal = ""

        if(isinstance(value, str) and len(value) > 0):
            #remove LF
            newVal = value.replace('\n', ' ')

            #remove FF, BB ] [
            newVal = newVal.replace(pdfparserconstants.BB,'')
            newVal = newVal.replace(pdfparserconstants.FF,'')
            newVal = newVal.replace('[','')
            newVal = newVal.replace(']','')

            if(source == "key"):
                #fix int attrs to make compliant
                if(newVal[0:1].isnumeric()):
                    newVal = 'n' + newVal

                #remove plus/minus sign
                newVal = newVal.replace('+', '_')
                newVal = newVal.replace('-', '_')
                #remove parens, colon, period, hash
                newVal = newVal.replace('(', '_')
                newVal = newVal.replace(')', '_')
                newVal = newVal.replace(':', '_')
                newVal = newVal.replace('.', '_')
                newVal = newVal.replace('#', '_')

                #first char cannot be an undercore
                if(newVal[0:1] == '_'):
                    newVal = 'x' + newVal

                newVal = newVal.strip()


  
        else:
            cleanValList = []
            #check to see if it's a list
            if(isinstance(value, list)):
                for i in range(0, len(value)):
                    checkVal = self.cleanValue(value[i], 'val')
                    if(checkVal != ''):
                        cleanValList.append(checkVal)
                if(len(cleanValList) == 1):
                    value = cleanValList[0]
                else:
                    value = cleanValList
            return value

        return newVal
    def deflateBuffer(self, buffer):
        deflatedBuffer = None
        zobj = zlib.decompressobj()
        deflatedBuffer = zobj.decompress(buffer)
                
        return deflatedBuffer
    def processStream(self, buffer, myDoc):
        unfilteredStream = None
        metaObj = self.meta
        encoding = "none"
        uBuffer = None
        decodeBuffer = buffer 
        skipBruteForce = False 

        if(hasattr(metaObj, "Filter") and metaObj.Filter == "FlateDecode"):
            
            try:
                uBuffer = self.deflateBuffer(buffer)
                #TODO: i don't like how I wrote this section in nested try/catch. will want to add more decoders later on
                decodeBuffer = uBuffer            
                if(hasattr(metaObj, "Type") and hasattr(metaObj, "Subtype") and metaObj.Type == "XObject" and metaObj.Subtype == "Image"):
                    #set unfiltered stream to be the decompressed data in base64
                    unfilteredStream  = base64.b64encode(uBuffer).decode(encoding="ascii", errors="strict")
                    skipBruteForce = True
                    encoding = "base64"
                if(hasattr(metaObj, "Type")  and metaObj.Type == "XRef"):
                    #do xref stream processing and set xreftable
                    myDoc.xreftable = xrefUtil.decodeXrefObjectStream(metaObj, uBuffer)
                    skipBruteForce = True

            except Exception as inst:
                print("Error occurred during decompression:  Obj ID " + self.id)
                print(inst)
                
        #TODO reorg code, probably to a switch statement


            

        
        #attempt decoding, even if there is no filter or deflate was successful
        if(skipBruteForce == False):
            try:
                #try UTF-8. This may need to change or be configurable
                unicodeLine = decodeBuffer.decode(encoding="UTF-8", errors="strict")
                #remove these common unprintable characters for testing whether decode was a success
                testLine = unicodeLine.replace('\n','').replace('\r','')
                if(testLine.isprintable()):
                    unfilteredStream = unicodeLine
                else:
                    raise Exception('UTF8 Not Printable')
                encoding="UTF-8"
            except Exception as inst:
                print("decoding failed:  Obj ID " + self.id)
                print(inst)
                try:
                    #try ASCII. This may need to change or be configurable
                    asciiLine = decodeBuffer.decode(encoding="ascii", errors="surrogateescape")
                    testLine = asciiLine.replace('\n','').replace('\r','')
                    if(asciiLine.isascii or testLine.isprintable()):
                        unfilteredStream = asciiLine
                    else:
                        raise Exception('ASCII Not Printable... giving up on decoding')
                    encoding="ascii"
                except Exception as inst:
                    print("decoding failed:  Obj ID " + self.id)
                    print(inst)

        self.unfilteredStream = unfilteredStream
        self.derivedStreamEncoding = encoding
        return unfilteredStream
    
    def update(self, obj):
        self.__dict__.update(obj.__dict__.items())      
   
