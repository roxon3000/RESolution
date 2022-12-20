import unittest
import PdfREParser

class Test_test_1(unittest.TestCase):
    def test_simplepdf(self):
        results = PdfREParser.main('simple-pdf.pdf')
        
        #TODO: assert results here
        self.assertEqual(results.pdfVersion ,"PDF-1.7")
        self.assertEqual(1,1)

    def test_if107guide(self):
        results = PdfREParser.main('IF107-guide.pdf')
        
        #TODO: assert results here
        self.assertEqual(results.pdfVersion ,"PDF-1.6")
        self.assertEqual(1,1)
if __name__ == '__main__':
    unittest.main()
