'''
Inputs: 'id' - Maven document ID to be scanned.

Fetch details from different srcs and update a mvn doc by ID.

'''

from genericpath import exists
from actions.baseaction import BaseAction
from common.logger import Logger
from primrose.wrapper import Primrose


class ScanMavenDocument(BaseAction):
    def __init__(self, name, description=None):
        self._logger = Logger.getLogger(__name__)
        self._docID = 0
        super().__init__(name, description)
    
    def exec(self, **kwargs):
        self._logger.info("Running action: {}".format(self.name))
        if "id" in kwargs:
            self._docID = kwargs["id"]
        if self._docID == 0 :
            self._logger.warning("Document id is not set. Ignoring execution.")
            return BaseAction.ERR_CODE_INVALID_PARAM
        try:
            self._scanMvnDoc()
        except Exception as e:
            self._logger.warn("Exception occured. " + str(e))
            return BaseAction.ERR_CODE_UNKNOWN_ERR
        return super().exec(**kwargs)

    def _scanMvnDoc(self):
        '''
        Scan the Maven document by id provided in self._docID and then
        fetch maven component details using the identified GAV id.
        Call Primrose to update the Maven document with the identified data.
        '''
        primroseClient = Primrose()
        _ , mvnJson = primroseClient.GetMavenDocById(self._docID)
        if mvnJson is None:
            raise Exception("Maven document is empty!")
        purl = mvnJson["purl"]
        # TODO: Should we check last updated time here?
        try:
            self._fetchData(purl)
        except Exception as e:
            self.logger.critical("Unknown exception occured.")
            self.logger.debug(str(e))
            raise e

        try:
            # Not needed to update below fields if already exists.
            if mvnJson["groupID"] is None or mvnJson["groupID"] == "" :
                groupID = self._getGroupID(purl)
                self._logger.info("GroupID identified: {}".format(groupID))
            if mvnJson["artifactID"] is None or mvnJson["artifactID"] == "" :
                artifactID = self._getArtifactID(purl)
                self._logger.info("ArtifactID identified: {}".format(artifactID))
            if mvnJson["version"] is None or mvnJson["version"] == "" :
                version = self._getVersion(purl)
                self._logger.info("version identified: {}".format(version))
            
            # Required to update below fields even if its exists.
            
        except KeyError as e:
            self._logger("Info key not present in Mvn Doc. {}".format(e))
            pass
        except Exception as e:
            self.logger.critical("Unknown exception occured.")
            self.logger.debug(str(e))
            raise e
    
    def _fetchData(self, purl):
        '''
        Fetch Mvn metadata using the resolver. Parse the metadata xml to store the data internally.
        Fetch the MVN pom file using resolver. Parse it and store the identified data.
        '''
        pass

