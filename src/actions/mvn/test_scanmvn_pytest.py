import pytest
from actions.mvn.scanmvn import ScanMavenDocument

class TestScanMvn():

    @pytest.mark.parametrize("metadataFile", (["actions/mvn/ut/maven-metadata.xml"]))
    def test_loadMavenMetadata(self, metadataFile):
        xmlStr = None
        with open(metadataFile, 'r') as f:
            xmlStr = f.read()
        scanner = ScanMavenDocument("test-scan-mvn")
        scanner._loadMavenMetadata(xmlStr)