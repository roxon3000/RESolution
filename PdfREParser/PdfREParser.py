
import json
import sys


from hashlib import md5
#from util import *
from util import pdfparserconstants
from util import docUtil
from util import fileExtUtil
from util import xrefUtil
from util import cidUtil

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
    
    myDoc = docUtil.JDoc("default")
    myDoc.objs = []
    myDoc.fileName = inputFile

    with open(inputFile, 'rb') as tr:
        testBuff = tr.read()
        print("Processing XREF...")
        xrefUtil.findXrefStart(tr, myDoc)



    with open(inputFile + '.bin' + '.txt', 'wb') as tw:
        tw.write(testBuff)



    with open(inputFile,'rb' ) as f:
        hashl = md5()
        hashl.update(f.read())
        myDoc.fileMd5 = hashl.hexdigest()


    print("Processing Objects and Raw Data Streams...")
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

        rlState = xrefUtil.RawLineState(streamPersist, currentObj, lastObj, lastMetaObj, prevObj, streamObj, isContinuation, EMPTY, EMPTY, None)
        # lines that do not need to be parsed. Should be able to use file.seek to skip most/all of the object.
        for rawline in f:
           
            rlState.rawlineCount = rlState.rawlineCount + 1
            #print('parsing raw line : ' + str(rlState.rawlineCount))
            myDoc.processRawLine(rawline, rlState, unfilterStreamFlag, f)
            



    #post parse processing of JSON
    print("Processing objects contained in compressed data streams...")
    #Process compressed objects in ObjStm objects
    for obj in myDoc.objs:
        if(hasattr(obj, "deflateFailed") and obj.deflateFailed == True):
            continue

        if(hasattr(obj, 'meta') and hasattr(obj.meta, 'Type') and obj.meta.Type == "ObjStm" and hasattr(obj, 'unfilteredStream') and obj.unfilteredStream != None
           and len(obj.unfilteredStream) > 0):
            myDoc.processObjectStreamLine(obj.unfilteredStream, int(obj.meta.First), int(obj.meta.N), obj.id)

    print("Attempting to extract text content...")
    #extract embedded files and process any CID objects and CID content streams
    for obj in myDoc.objs:
        fileExtUtil.extractEmbeddedFile(obj, inputFile)
        cidUtil.processCID(obj, myDoc)

    with open(outputFile, 'w', encoding="ascii", errors="surrogateescape") as fw:
       
            fw.write(json.dumps(myDoc, default=vars))

    

    return myDoc

if __name__ == '__main__':
    #sys.exit(main(sys.argv[1:]))
    inputFile = sys.argv[1]
    main(inputFile)


