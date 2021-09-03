'''
Inputs: doc-ID - SBOM doc ID.

SBOM doc scanning, to create docs for its deps and components.
'''

from actions.baseaction import BaseAction
from common.logger import Logger
from primrose.wrapper import Primrose
from packageurl import PackageURL

class ScanSBOM(BaseAction):
    def __init__(self, name, description):
        self.docId = 0
        super().__init__(name, description=description)
    
    def exec(self, **kwargs):
        self.logger = Logger.getLogger(__name__)
        self.logger.info("Running action: {}".format(self.name))
        if "id" in kwargs:
            self.docId = kwargs["id"]
        if self.docId == 0 :
            self.logger.warning("doc id is not set. Ignoring execution.")
            return 0
        self._scanSbomDoc()
        return super().exec()

    def _scanSbomDoc(self):
        '''
        Scan the SBOM by id provided in self.docId.
        Identify the components and create appropriate documents with available details.
        '''
        primroseClient = Primrose()
        sbomJson = primroseClient.GetSbomById(self.docId)
        if sbomJson is not dict:
            raise Exception("Document not correct. Got: {}".format(sbomJson))
        for component in sbomJson["components"]:
            purl = component["purl"]
            purlDict = PackageURL.from_string(purl).to_dict()
            if purlDict['type'] == 'maven' :
                g = component["group"]
                a = component["name"]
                v = component["version"]
                idCreated = primroseClient.CreateMaven(g, a, v, purl=purl)
                self.logger.info("Primrose create-maven-doc API returned id {} ".format(idCreated))
            else:
                self.logger.warning("Component type {} is unknown.".format(purlDict['type']))

