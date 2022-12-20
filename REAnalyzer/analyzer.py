
import sys
import json
import pdfanalyzer
from collections import namedtuple

def analyze(inputFile): 

    with open(inputFile, 'r') as tr:
        jObj = json.load(tr, object_hook=customDocDecoder)

        fileType = jObj.fileType
        analyzer = None

        match fileType:
            case "PDF":
                analyzer = pdfanalyzer.PdfAnalyzer(jObj)
            case _:
                raise Exception("Unsupported File Type: " + fileType)

        results = analyzer.analyze()

    

def customDocDecoder(docDict):
    return namedtuple('ParserJson', docDict.keys())(*docDict.values())


if __name__ == '__main__':
    #sys.exit(main(sys.argv[1:]))
    inputFile = sys.argv[1]
    analyze(inputFile)