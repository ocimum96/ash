'''
Helper class to resolve maven details from different available repos, based on resoultion order.

'''

from http import HTTPStatus
import requests
from common.logger import Logger
import urllib

class MavenResolver:

    class _mavenRepository:

        def __init__(self, id, url, user=None, password=None ) -> None:
            self.id = id
            self._url = url
            self._user = user
            self._password = password

        def getFile(self, httpUrlPathtoFile): #-> Tuple[str, int]: TODO:requires Py39
            '''
            Fetch the file from maven repo.
            Implement using basic http call to get the file.
            Override this fn if require to fetch the file in a different way.
            '''            
            l = Logger.getLogger(__name__)
            l.debug("Fetching the file with path: {}".format(httpUrlPathtoFile))

            # (scm, netloc, path, params, query, fragment)
            urlTuple = ('https', self._url, httpUrlPathtoFile, None, None, None)
            finalUrl = urllib.parse.urlunparse(urlTuple)
            l.debug("Calling GET on {}".format(finalUrl))
            r = requests.get(finalUrl, timeout=10)        
            return r.text, r.reason, r.status_code

    def __init__(self, group, artifact, version) -> None:
        self._logger = Logger.getLogger(__name__)
        self._resolversList = list()
        self._group = group
        self._artifact = artifact
        self._version = version
        self._fillTheResolverList()

    # def _getNextResolver(self) -> _mavenRepository:
    #     '''
    #     Pop the next resolver from the queue.
    #     '''
    #     pass

    def _fillTheResolverList(self):
        '''
        Create all the configured/known resolvers and add it in a list, to use it
        based on insertion order.
        '''
        
        self._logger.debug("Filling the resolver list..")        

        #TODO: Read the Repo details from config file, so that user can config custom mvn repos.
        centralMavenRepo = MavenResolver._mavenRepository("central-maven", "repo1.maven.org/maven2")
        atlasianMavenRepo = MavenResolver._mavenRepository("atlasian-external-maven", "packages.atlassian.com/mvn/maven-atlassian-external")
        self._resolversList.append(centralMavenRepo)
        self._resolversList.append(atlasianMavenRepo)

        self._logger.debug("Done creating and appending resolvers to the list.")

    def ResolveMetadata(self) -> str:
        '''
        Resolve the metadata xml and return it as xml str.
        '''
        urlPathToFile = self._group + '/' + self._artifact + '/' + "maven-metadata.xml"
        xmlData = self._resolveFile(urlPathToFile)    
        if xmlData is None:
            raise MavenResolver.FileNotResolvedException("Not able to resolve metadata for {}.{}"
            .format(self._group, self._artifact))     
        else:                   
            self._logger.debug("Got maven xml metadata: " + xmlData)
            return xmlData     

    def ResolvePOMfile(self) -> str:
        '''
        Resolve the POM file and return as a str
        '''
        urlPathToFile = self._group + '/' + self._artifact + '/' + self._version + '/' + self._artifact + '-' + self._version + ".pom"
        xmlData = self._resolveFile(urlPathToFile)   
        if xmlData is None:
            raise MavenResolver.FileNotResolvedException("Not able to resolve POM file for {}.{}.{}"
            .format(self._group, self._artifact, self._version))
        else:             
            self._logger.debug("Got maven pom data: " + xmlData)
            return xmlData    
        
    def _resolveFile(self, urlPathToFile) -> str:
        '''
        A helper file to fetch a file from the MVN repos and return as text.
        '''        
        text = None
        for mavenRepo in self._resolversList:
            self._logger.debug("Trying with repo: {}".format(mavenRepo.id))
            text, reason, status_code = mavenRepo.getFile(urlPathToFile)
            if status_code == HTTPStatus.OK:   
                self._logger.debug("The file is resolved.")             
                break       
            else:
                self._logger.debug("File not resolved. Got reason : {}".format(reason))
                text = None # some Maven repo returns error texts, discard that.
        return text     

    class FileNotResolvedException(BaseException):
        """Raised when all repos are tried and file not resolved"""
        def __init__(self, *args: object) -> None:
            super().__init__(*args)






