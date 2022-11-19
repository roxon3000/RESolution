import pdfparserconstants
import zlib

class JObj:
    def __init__(meo, id):
        meo.id = id
        meo.hasStream = False

    def __setattr__(self, name, value):
        newVal = value

        #don't clean streams
        if(name == 'unfilteredStream' or name == 'stream'):
            pass
        else:
            newVal = self.cleanValue(value)
            
        self.__dict__[name] = newVal

    def mutate(self, word):
        word = self.parseBracketedList(word)
        if(self.propRulesCheck(word)): 
            keyval = word.split(' ')
            key = self.cleanValue(keyval[0])
            if(len(keyval) == 2):
                val = self.cleanValue(keyval[1])                   
                self.__setattr__(key, val)
            elif(len(keyval) == 1):
                self.__setattr__(key, True)
            else:
                keyval.pop(0)
                self.__setattr__(key, keyval)
    def propRulesCheck(self, prop):
        
        #don't add empty properties
        if(len(prop) < 1):
            #ignore
            return False

        if(prop.strip() == pdfparserconstants.BB):
            return False

        return True
    def parseBracketedList(self,word):
        #find open bracked
        bracketIndex = word.find('[')
        if(bracketIndex > 0 and word[bracketIndex-1:bracketIndex] != ' '):
            #TODO: this will break if there are sublists
            bsplit = word.split('[')
            newVal = bsplit[0] + ' ' + bsplit[1]
            newVal = newVal.replace(']','')
            word = newVal                
        return word
    def cleanValue(self, value):
        newVal = ""
        
        if(isinstance(value, str) and len(value) > 0):
            #remove LF
            newVal = value.replace('\n', '')

            #remove FF, BB ] [
            newVal = newVal.replace(pdfparserconstants.BB,'')
            newVal = newVal.replace(pdfparserconstants.FF,'')
            newVal = newVal.replace('[','')
            newVal = newVal.replace(']','')
  
        else:
            cleanValList = []
            #check to see if it's a list
            if(isinstance(value, list)):
                for i in range(0, len(value)):
                    checkVal = self.cleanValue(value[i])
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
    def processStream(self, buffer):
        unfilteredStream = None
        metaObj = self.meta
        encoding = "none"

        if(hasattr(metaObj, "Filter") and metaObj.Filter == "FlateDecode"):
            
            try:
                uBuffer = self.deflateBuffer(buffer)
                #TODO: i don't like how I wrote this section in nested try/catch. will want to add more decoders later on
                try:
                    #try UTF-8. This may need to change or be configurable
                    unicodeLine = uBuffer.decode(encoding="UTF-8", errors="strict")
                    if(unicodeLine.isprintable()):
                        unfilteredStream = unicodeLine
                    else:
                        raise Exception('UTF8 Not Printable')
                    encoding="UTF-8"
                except Exception as inst:
                    print("decoding failed:  Obj ID " + self.id)
                    print(inst)
                    try:
                        #try ASCII. This may need to change or be configurable
                        asciiLine = uBuffer.decode(encoding="ascii", errors="surrogateescape")
                        if(asciiLine.isprintable()):
                            unfilteredStream = asciiLine
                        else:
                            raise Exception('ASCII Not Printable... giving up on decoding')
                        encoding="ascii"
                    except Exception as inst:
                        print("decoding failed:  Obj ID " + self.id)
                        print(inst)
                    
            except Exception as inst:
                print("Error occurred during decompression:  Obj ID " + self.id)
                print(inst)
            

        self.unfilteredStream = unfilteredStream
        self.derivedStreamEncoding = encoding
        return unfilteredStream
    
    def update(self, obj):
        self.__dict__.update(obj.__dict__.items())      
   
