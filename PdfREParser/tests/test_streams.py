
import unittest
import PdfREParser
import jdoc
import jobj 
import base64

class Test_test_1(unittest.TestCase):
    def test_decode_stream(self):
        encodedStream = "eJxdUstugzAQvPMVPqaHCMwjTSSElJBG4tCHSvsBYC+ppWIs4xz4+5pdSKRaAjTrmfEs67CszpVWjoUfdhA1ONYpLS2Mw80KYC1clQ54zKQSbkH4Fn1jgtCL62l00Fe6G4I8Zyz89LujsxPbHOXQwlMQvlsJVukr23yXtcf1zZhf6EE7FgVFwSR03um1MW9NDyxE2baSfl+5aes1D8bXZIDFiDmlEYOE0TQCbKOvEOSRXwXLL34VAWj5bz8jVduJn8YiO/HsKIqjAlFGKEYUp4hSTuhM6IgoIV0W4SmL32F1f4Q5IS0qyXdPp1wQcU7FEoucDDklSCgP31PxQMWMguxWM8yTUPGy6rBIngkxk2fKSsw0XSnzZ0fNpS9EWYqnpSvqY/6N87jvMxI3a/148E7gXOaJKA33a2MGM6vm5w/Sjag="
        myDoc = jdoc.JDoc("streams")
        byteStream = base64.b64decode(encodedStream)
        streamObj = jobj.JObj('streams')
        streamObj.meta = jobj.JObj('meta')
        streamObj.processStream(byteStream)
        print("Stream Test")
        print(streamObj.unfilteredStream)
        self.assertEqual(1,1)


if __name__ == '__main__':
    unittest.main()
