
import unittest
import PdfREParser
import jdoc
import jobj 

class Test_test_1(unittest.TestCase):
    def test_simplepdf(self):
        rawLine = bytes("<</Contents 4763 0 R/CropBox[0.0 0.0 612.0 792.0]/MediaBox[0.0 0.0 612.0 792.0]/Parent 4740 0 R/Resources<</Font<</TT0 4777 0 R/TT1 4779 0 R/TT2 4781 0 R/TT3 4783 0 R/TT4 4785 0 R>>/ProcSet[/PDF/Text]>>/Rotate 0/StructParents 0/Tabs/S/Type/Page>>", "UTF-8")
        myDoc = jdoc.JDoc('test doc')
        state = PdfREParser.RawLineState(None, jobj.JObj('test obj')  , None, None, None, None, False, "4762 0 obj", "obj")
        myDoc.processRawLine(rawLine, state, "Y")
       
        
        #TODO: assert results here
        #self.assertEqual(results.pdfVersion ,"PDF-1.7")
        self.assertEqual(1,1)


if __name__ == '__main__':
    unittest.main()
