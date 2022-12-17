import os
import jdoc
from util import *
import pdfparserconstants
import re 
import jobj
import sys 

# From PDF 1.7 spec
# 
# << /Type /XRef
# /Index [0 32] % This section has one subsection with 32 objects
# /W [1 2 2] % Each entry has 3 fields: 1, 2 and 2 bytes in width,
# % respectively
# /Filter /ASCIIHexDecode % For readability in this example
# /Size 32
# 
# >>
# stream
# 00 0000 FFFF % “0 65535 f” in a cross-reference table
# 
# 02 000F 0000 % The entry for object 11, the first font
# 02 000F 0001 % The entry for object 12, the font descriptor
# 02 000F 0002 % The entry for object 13, the second font
# 
# 01 BA5E 0000 % The entry for object 15, the object stream
# 
# endstream
# endobj
# startxref
# 54321 % The offset of “99 0 obj”
# %%EOF
#--------------------------------------
# simple-pdf.pdf looks lke this when formatted to 5 bytes per row, based on width W[1 2 2]
# 18 0 obj
# <<
# /Size 19
# /Root 2 0 R
# /Info 3 0 R
# /Filter /FlateDecode
# /Type /XRef
# /Length 71
# /W [ 1 2 2 ]
# /Index [ 0 19 ]
# >> 
#
# 00 0000 ffff 
# 02 0011 0000  compressed object, stored in obect 11H or 17D
# 02 0011 0001 
# 02 0011 0002 
# 02 0011 0003 
# 02 0011 0004 
# 02 0011 0005 
# 02 0011 0006 
# 02 0011 0007 
# 02 0011 0008 
# 02 0011 0009 
# 02 0011 000a 
# 01 0010 0000 
# 01 5f16 0000 
# 01 60a4 0000 
# 02 0011 000b 
# 01 6912 0000 
# 01 7034 0000 
# 01 746d 0000  
# 

"""
    based on below description, simple-pdf has 6 uncompressed objects (type 1). Then also 12 compressed objects (type 2)


0   1   The type of this entry, which must be 0. Type 0 entries define the
        linked list of free objects (corresponding to f entries in a cross-
        reference table).
    2   The object number of the next free object.
    3   The generation number to use if this object number is used again.
1   1   The type of this entry, which must be 1. Type 1 entries define
        objects that are in use but are not compressed (corresponding to n
        entries in a cross-reference table).
    2   The byte offset of the object, starting from the beginning of the
        file.
    3   The generation number of the object. Default value: 0.
2   1   The type of this entry, which must be 2. Type 2 entries define
        compressed objects.
    2   The object number of the object stream in which this object is
        stored. (The generation number of the object stream is implicitly
        0.)
    3   The index of this object within the object stream.


Direct Xref example and explanation

Example 3.5 shows a cross-reference section consisting of a single subsection
with six entries: four that are in use (objects number 1, 2, 4, and 5) and two that
are free (objects number 0 and 3). Object number 3 has been deleted, and the
next object created with that object number is given a generation number of 7.
Example 3.5
xref
0 6
0000000003 65535 f
0000000017 00000 n
0000000081 00000 n
0000000000 00007 f
0000000331 00000 n
0000000409 00000 n

"""

EMPTY = pdfparserconstants.EMPTY 

def fastForward(curOffset, xref):
    nextObjOffset = curOffset

    if(xref == None or hasattr(xref, "rows") == False or xref.rows == None) :
        return nextObjOffset

    #assume it's sorted? better be
    for row in xref.rows:
        if(row.col1 == 1 and row.col2 > curOffset):
            nextObjOffset = row.col2
            break

    return nextObjOffset

def decodeXrefObjectStream(xrefMeta, xrefBuffer):
    width = [] 
    #length = xrefMeta.Length
    #index = xrefMeta.Index

    #calc byte length of row
    rowLength = 0
    for wi in xrefMeta.W:
        rowLength = rowLength + int(wi)
        width.append(int(wi))

    numberOfRows = int(len(xrefBuffer)/rowLength)
    #if(width == [1,2,2]):
    xreftable = jobj.JObj("xreftable")
    xreftable.rows = []
    
    print('Found XREF Table in Object, printing.. ')
    for i in range(numberOfRows):
        row = xrefBuffer[i*rowLength: (i*rowLength) + rowLength ] 
        
        col1 = row[0:int(width[0])]
        col2 = row[width[0]:width[0] + width[1]]
        col3 = row[width[0] + width[1]:width[0] + width[1] + width[2]]

        row = jobj.JObj('row')
        row.rowNum = i
        row.col1 = int.from_bytes(col1,'big')
        row.col2 = int.from_bytes(col2,'big')
        row.col3 = int.from_bytes(col3,'big')
        
        xreftable.rows.append(row)
        
        print( col1.hex() + ' ' + col2.hex() + ' ' + col3.hex() )

    return xreftable

def sortXrefTable(xreftable):
    xreftable.rows.sort(key=lambda row: row.col2)

def findXrefStart(fileStream, myDoc):
    #find file length, back up.. some number of bytes and and proceed to find startxref

    fileStream.seek(-500,os.SEEK_END)
    
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
    #TODO - need to add a performance improve for large object stream processing. large object streams can have a large number of internal new
    # lines that do not need to be parsed. Should be able to use file.seek to skip most/all of the object.
    #for rawline in fileStream:
    
    xfline = fileStream.read()
    rlState.rawlineCount = rlState.rawlineCount + 1
    print('Attempting to find and parse XREF table')
    startxref = int(processFindXrefStartLine(xfline))

    print('Found XREF table at offset ' + str(startxref))

    fileStream.seek(startxref)
    firstLine = True 
    xrefType = "unknown"
    rlState.lastLineType = "xrefstub"
    rlState.mode = "xreftable"
    xrefCount = 0 #used for direct processing
    xrefCountFlag = False #used for direct processing
    xrefRowCount = 1 #used for direct processing

    for rawline in fileStream:
        if(firstLine == True):
            firstLine = False
            #determine if xref is an object reference or a direct xref table
            refObjMatch = re.search(pdfparserconstants.OBJ_ID_REGEX, str(rawline))
            if(refObjMatch == None):
                xrefType = "direct"
            else:
                xrefType = "indirect"

        if(xrefType == "indirect"):
            #parse xref object
            myDoc.processRawLine(rawline, rlState, "Y", fileStream)
            if(myDoc.xrefObj != None):
                myDoc.xrefSet = True
        else:
            #direct
            #parse xref section directly
            myDoc.processRawLine(rawline, rlState, "N", fileStream)
            if(xrefCountFlag):
                xrefCount = xrefCount + 1

            if(xrefCount >= xrefRowCount):
                myDoc.xrefSet = True

            #myDoc.xrefSet is set in jdoc processing
            if(rlState.currentObj != None and rlState.currentObj.index != None and xrefCountFlag == False):
                xrefCountFlag = True
                xrefRowCount = int(rlState.currentObj.index.end)

        if(myDoc.xrefSet == True):
            break
    
    myDoc.xrefType = xrefType
    #make sure table is sorted
    sortXrefTable(myDoc.xreftable)

def processOldXrefFixedFormatIndex(rawline, xreftable):
    
    xrefIndex = jobj.JObj('xrefindex')
    iSplit = rawline.split(' ')

    if(iSplit != None and len(iSplit) > 1):
        xrefIndex.start = str(iSplit[0]).strip()
        xrefIndex.end = str(iSplit[1]).strip()

    xreftable.index = xrefIndex


def processOldXrefFixedFormatRow(rawline, xreftable):
    newRowNum = len(xreftable.rows)
    newRow = jobj.JObj(newRowNum)
    newRow.rowNum = newRowNum 
    #conform to the standard of putting the offset in col2 
    newRow.freeChar = str(rawline[17:20]).strip()
    newRow.col1 = 1 #hard coded for direct to indicate it's not an embedded object
    newRow.col2 = int(rawline[0:10])
    newRow.col3 = int(rawline[11:16])

    xreftable.rows.append(newRow)

def processFindXrefStartLine(rawline):

    asciiLine = rawline.decode(encoding="ascii", errors="surrogateescape")
    crLines = asciiLine.splitlines(keepends=True)

    #read in reverse until startxref is found
    for i in reversed(range(len(crLines))):
        if(crLines[i].strip() == pdfparserconstants.XREFSTART):
            return crLines[i+1].strip()