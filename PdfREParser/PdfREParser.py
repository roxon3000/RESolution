
import json
import sys
import pdfparserconstants
import jdoc
from hashlib import md5
from util import *





def main(arg1):
    #TODO: add support for Linearized PDF files
    #TODO: improve stream output handling. Streams should be output to separate files for improved performance and ease of use with big files and streams.
    #TODO: Extract Embedded files, similar to what needs to be done for streams 


    ####### Parameters
    #Flag to process stream filters
    unfilterStreamFlag = "Y" #TODO: add this as an argument
    inputFile = arg1
    outputFile = inputFile + '.json' 
    ####################
    EMPTY = pdfparserconstants.EMPTY
    
    myDoc = jdoc.JDoc("default")
    myDoc.objs = []


    with open(inputFile, 'rb') as tr:
        testBuff = tr.read()
        findXrefStart(tr, myDoc)



    with open(inputFile + '.bin' + '.txt', 'wb') as tw:
        tw.write(testBuff)



    with open(inputFile,'rb' ) as f:
        hashl = md5()
        hashl.update(f.read())
        myDoc.fileMd5 = hashl.hexdigest()


    with open(inputFile,'rb' ) as f:
        streamPersist = None
        #N
        currentObj= None
        lastObj = None 
        lastMetaObj = None
        #N-1
        prevObj = None
        #object that is in queue to have its stream populated
        streamObj = None
        isContinuation = False
        lastLine = EMPTY
        lastLineType = EMPTY

        rlState = RawLineState(streamPersist, currentObj, lastObj, lastMetaObj, prevObj, streamObj, isContinuation, EMPTY, EMPTY, None)
        # lines that do not need to be parsed. Should be able to use file.seek to skip most/all of the object.
        for rawline in f:
           
            rlState.rawlineCount = rlState.rawlineCount + 1
            #print('parsing raw line : ' + str(rlState.rawlineCount))
            myDoc.processRawLine(rawline, rlState, unfilterStreamFlag, f)
            



    #post parse processing of JSON
    
    #Process compressed objects in ObjStm objects
    for obj in myDoc.objs:
        if(hasattr(obj, 'meta') and hasattr(obj.meta, 'Type') and obj.meta.Type == "ObjStm" and hasattr(obj, 'unfilteredStream') and obj.unfilteredStream != None
           and len(obj.unfilteredStream) > 0):
            myDoc.processObjectStreamLine(obj.unfilteredStream, int(obj.meta.First), int(obj.meta.N), obj.id)

    #extract embedded files
    for obj in myDoc.objs:
        extractEmbeddedFile(obj, inputFile)


    with open(outputFile, 'w', encoding="ascii", errors="surrogateescape") as fw:
       
            fw.write(json.dumps(myDoc, default=vars))

    fw.close()

    return myDoc

if __name__ == '__main__':
    #sys.exit(main(sys.argv[1:]))
    inputFile = sys.argv[1]
    main(inputFile)


