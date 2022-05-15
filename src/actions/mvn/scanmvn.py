'''
Inputs: 'id' - Maven document ID to be scanned.

Fetch details from different srcs and update a mvn doc by ID.

'''

from collections import defaultdict
from actions.baseaction import BaseAction
from common.logger import Logger
from primrose.wrapper import Primrose
from datasources.repos.mavenresolver import MavenResolver
from packageurl import PackageURL
from defusedxml import ElementTree as ET
# from xml.etree import ElementTree as ET
from defusedxml import minidom as DOM

class ScanMavenDocument(BaseAction):
    def __init__(self, name, description=None):
        self._logger = Logger.getLogger(__name__)
        self._docID = 0
        self._fetchedDataDict = defaultdict(lambda: defaultdict(list))
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
        self._logger.debug("Fetching Maven data for {}".format(purl))
        purlDict = PackageURL.from_string(purl).to_dict()
        if purlDict['type'] == 'maven' :
            g = purlDict["namespace"]
            a = purlDict["name"]
            v = purlDict["version"]
            mvnResolver = MavenResolver(g, a, v)
            dataStr = mvnResolver.ResolveMetadata()
            self._loadMavenMetadata(dataStr)
            dataStr = mvnResolver.ResolvePOMfile()
            self._loadMavenPomData(dataStr)
        else:
            self._logger.error("Wrong PURL type : {}. Expects type 'maven' here.".format(purlDict['type']))
            raise Exception("Wrong PURL type.")

    def _loadMavenMetadata(self, metadataXML):
        '''
        Parse the input mvn metadata XML str and fill in to data dict.
        '''
        self._logger.debug("Parsing Maven Metadata xml..")
        root = ET.fromstring(metadataXML)
        for child in root:            
            if child.tag == 'groupId':
                self._fetchedDataDict['groupID'] = child.text
                self._logger.debug("Created groupID {}".format(str(self._fetchedDataDict)))
            elif child.tag == 'artifactId':
                self._fetchedDataDict['artifactID'] = child.text
                self._logger.debug("Created artifactID {}".format(str(self._fetchedDataDict)))
            elif child.tag == 'versioning':
                for versionChild in child:
                    if versionChild.tag == 'latest':
                        self._fetchedDataDict['versioning']['latest'] = versionChild.text
                    elif versionChild.tag == 'release':
                        self._fetchedDataDict['versioning']['release'] = versionChild.text
                    elif versionChild.tag == 'versions':
                        for versions in versionChild:
                            if versions.tag == 'version':
                                self._fetchedDataDict['versioning']['versions'].append(versions.text)
                    elif versionChild.tag == 'lastUpdated':
                        self._fetchedDataDict['versioning']['lastUpdated'] = versionChild.text
        self._logger.debug("Created data dict: {}".format(str(self._fetchedDataDict)))

    def _loadMavenPomData(self, pomDataXML):
        '''
        Parse the i/p mvn POM file data & fill in to the data dict.
        '''
        self._logger.debug("Parsing POM XML data..")
        with DOM.parseString(pomDataXML) as doc:
            handler = ScanMavenDocument._pomXmlHandler(self._fetchedDataDict)
            handler._handleProject(doc)
        
    class _pomXmlHandler:

        def __init__(self, dataDict) -> None:
            self.dataDict = dataDict

        def _handleProject(self, document):
            pass

        def _handleBasics(self, project):
            pass

        def _handleBuildSettings(self, project):
            pass

        def _handleMiscInfo(self, project):
            pass

        def _handleEnvironmentSettings(self, project):
            pass


        

