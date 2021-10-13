from unittest import TestCase, main
from unittest.mock import patch
from json import loads as jsonLoad
from actions.sbom.scansbom import ScanSBOM

class TestScanSbomDoc(TestCase):
    def test_simple_maven_test(self):
        class PrimroseMock:
            @staticmethod
            def GetSbomById():
                mockData = ""
                with open("actions/sbom/ut/mockDepsMvn.json", 'r') as mockFile:
                    mockData = jsonLoad(mockFile.read())
                return mockData
            
            @staticmethod
            def CreateMaven():
                return "mocked-sbom-doc-id"

        with patch('actions.sbom.scansbom.Primrose', autospec=False) as primroseMocked:
            primroseMocked.return_value.GetSbomById.return_value = PrimroseMock.GetSbomById()
            primroseMocked.return_value.CreateMaven.return_value = PrimroseMock.CreateMaven()
            ScanSBOM(name="simple-scan-sbom", description="for ut").exec(id=1)
            primroseMocked.return_value.GetSbomById.assert_called()
            primroseMocked.return_value.CreateMaven.assert_called()


if __name__ == '__main__':
    main()