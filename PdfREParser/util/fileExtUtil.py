
import os

def extractEmbeddedFile(obj, parentFile):
    
    #debug
    if(obj.id == '16'):
        x = 1

    if( hasattr(obj, "meta") and hasattr(obj.meta, "Type") and obj.meta.Type == "EmbeddedFile" 
      and hasattr(obj, "unfilteredStream") and obj.unfilteredStream != None) :
        subType = ""
        if(hasattr(obj.meta, "Subtype")):
            subType = obj.meta.Subtype 

        outBuff = str.encode(obj.unfilteredStream)

        newpath = r'obj-' + obj.id 
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        fileName = newpath + "\\" + parentFile + "." + obj.id + "." + subType

        with open(fileName, 'wb') as fw:
       
            fw.write(outBuff)

        fw.close()

