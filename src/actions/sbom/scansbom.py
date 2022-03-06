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
            return BaseAction.ERR_CODE_INVALID_PARAM
        try:
            self._scanSbomDoc()
        except Exception as e:
            self.logger.warn("Exception occured. " + str(e))
            return BaseAction.ERR_CODE_UNKNOWN_ERR
        return super().exec()

    def _scanSbomDoc(self):
        '''
        Scan the SBOM by id provided in self.docId.
        Identify the components and create appropriate documents with available details.
        '''
        primroseClient = Primrose()
        sbomJson = primroseClient.GetSbomById(self.docId)
        if sbomJson is None:
            raise Exception("Document not correct.")
        
        for component in sbomJson["components"]:
            try:
                if component["type"] == "library": #Continue only if its a library
                    purl = component["purl"] #TODO: What if PURL not available for the component?
                    purlDict = PackageURL.from_string(purl).to_dict()
                    if purlDict['type'] == 'maven' :
                        g = component["group"]
                        a = component["name"]
                        v = component["version"]
                        res = primroseClient.CreateMaven(g, a, v, purl=purl) # TODO: Need to make purl as the only required param. 
                        if res:
                            self.logger.info("Primrose New Maven-doc created.")
                        else:
                            self.logger.critical("Primrose new Maven doc create call failed. Quiting the action.")
                            break #Other calls are also likely to fail.
                    else:
                        self.logger.warning("Component type {} is unknown.".format(purlDict['type']))
            except KeyError as e:
                self.logger.warning("Key error while parsing SBOM.")
                self.logger.warn("Key not found {}".format(e))
                continue
            except Exception as e:
                self.logger.critical("Unknown exception occured.")
                self.logger.debug(str(e))
                break

