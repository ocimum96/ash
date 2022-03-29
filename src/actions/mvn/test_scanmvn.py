from unittest import TestCase, main, expectedFailure
from actions.mvn.scanmvn import ScanMavenDocument

class TestScanMvn(TestCase):

    def _loadMavenMetadataFromFile(self, metadataFile):
        xmlStr = None
        with open(metadataFile, 'r') as f:
            xmlStr = f.read()
        scanner = ScanMavenDocument("test-scan-mvn")
        scanner._loadMavenMetadata(xmlStr)
    
    def test_loadMavenMetadata(self):
        self._loadMavenMetadataFromFile("src/actions/mvn/ut/maven-metadata.xml")
        pass
        
    def test_loadMavenMetadata_bad_xml(self):
        self._loadMavenMetadataFromFile("src/actions/mvn/ut/maven-metadata-wrong.xml")

    @expectedFailure
    def test_loadMavenMetadata_non_xml(self):
        scanner = ScanMavenDocument("test-scan-mvn")
        scanner._loadMavenMetadata("{}") # TODO: Should expect an exception to throw here

if __name__=='__main__':
    main()        