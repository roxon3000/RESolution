
import json
import base64
import zlib 
import sys
import pdfparserconstants
import jdoc

class RawLineState:
    def __init__(self, streamPersist, currentObj, lastObj, lastMetaObj, prevObj, streamObj, isContinuation, lastLine, lastLineType, currentMetaObj):
        self.streamPersist = streamPersist
        self.currentObj = currentObj
        self.lastObj = lastObj
        self.lastMetaObj = lastMetaObj
        self.prevObj = prevObj
        self.streamObj = streamObj
        self.isContinuation = isContinuation
        self.lastLine = lastLine
        self.lastLineType = lastLineType
        self.currentMetaObj = currentMetaObj


def main(arg1):
    
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
    tr.close()


    with open(inputFile + '.bin' + '.txt', 'wb') as tw:
        tw.write(testBuff)
    tr.close()


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

        for rawline in f:
            myDoc.processRawLine(rawline, rlState, unfilterStreamFlag)
            

    f.close()

    #post parse processing of JSON

    #TODO heirarchical relationships and cmap processing


    with open(outputFile, 'w', encoding="ascii", errors="surrogateescape") as fw:
       
            fw.write(json.dumps(myDoc, default=vars))

    fw.close()

    return myDoc

if __name__ == '__main__':
    #sys.exit(main(sys.argv[1:]))
    inputFile = sys.argv[1]
    main(inputFile)


