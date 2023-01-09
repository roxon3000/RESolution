
#
#   Examples.
#
#   this defines a font cid to unicode charcode. 0003=0020 or "T", etc.
#   beginbfchar 
#       <0003> <0020> 
#       <0012> <0043> 
#       <003E> <004C> 
#       <0064> <0054> 
#       <0102> <0061> 
#       <010F> <0062> 
#       <0110> <0063> 
#       <011E> <0065> 
#       <015A> <0068> 
#       <015D> <0069> 
#       <016C> <006B> 
#       <016F> <006C> 
#       <0176> <006E> 
#       <0190> <0073> 
#
#   endbfchar
#
#  Content stream: [<0064>-0.304688<015A>5.000000<015D>-0.492188<0190>-9.000000<0003>6.000000<015D>-0.492188<0190>-0.113281<0003>-0.074219<0102>-0.003906<0003>-0.074219<0012>-7.000000<016F>-0.492188<015D>9.000000<0110>-0.851563<016C>-0.589844<0102>-0.003906<010F>5.000000<016F>-0.492188<011E>-0.558594<0003>6.000000<003E>-10.000000<015D>9.000000<0176>-0.390625<016C>-0.589844] TJ
#  <0064>=<0054>=T, <015D>=<0069>=h, etc.
# BT = Begin Text Object
# ET = End Text Object
# Tr = text rendering Mode. 
# Tf = Text Font
# Td = position on page where text prints
# Tj = paints the string of chars with no rearrangement. (Some Text) Tj
# w = line width : 2 w
# Tc Character spacing
# Tw Word spacing
# Th Horizontal scaling
# Tl Leading
# Tf Text font
# Tfs Text font size
# Tmode Text rendering mode
# Trise Text rise
# Tk Text knockout
# Tm Text Matrix
# 
#  For simplicity, only look at TJ or Tj. TJ is an array []. Tj is a string group ()
'''
TJ = Show one or more text strings, allowing individual glyph positioning (see imple-
mentation note 58 in Appendix H). Each element of array can be a string or a
number. If the element is a string, this operator shows the string. If it is a num-
ber, the operator adjusts the text position by that amount; that is, it translates the
text matrix, Tm . The number is expressed in thousandths of a unit of text space
(see Section 5.3.3, “Text Space Details,” and implementation note 59 in Appen-
dix H). This amount is subtracted from the current horizontal or vertical coordi-
nate, depending on the writing mode. In the default coordinate system, a
positive adjustment has the effect of moving the next glyph painted either to the
left or down by the given amount. Figure 5.11 shows an example of the effect of
passing offsets to TJ.
'''

# The remaining four range substitutions complete the Roman character substi-
# tution. The first and second elements in each line are the beginning and
# ending valid input codes for the template font; the third element is the begin-
# ning character code for the range of proportional Roman characters being
# assigned to that template input range.
# Example 20 Ranges of base fonts
# 4 beginbfrange
# <00> <26> <00>
# <28> <5b> <28>
# <5d> <5f> <5d>
# <61> <7d> <61>
# endbfrange



#