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

"""