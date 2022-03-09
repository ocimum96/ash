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
            s = r.status_code
            return r.text, s

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
        Create all the configured resolvers and add it in a list, to use it
        based on insertion order.
        '''
        self._logger.debug("Filling the resolver list..")        
        centralMavenRepo = MavenResolver._mavenRepository("central-maven", "repo1.maven.org/maven2")
        atlasianMavenRepo = MavenResolver._mavenRepository("atlasian-external-maven", "packages.atlassian.com/mvn/maven-atlassian-external")
        self._resolversList.append(centralMavenRepo)
        self._resolversList.append(atlasianMavenRepo)
        self._logger.debug("Done creating and appending resolvers to the list.")

    def ResolveMetadata(self) -> dict:
        '''
        Resolve the metadata xml and return it as json dict.
        '''
        urlPathToFile = self._group + '/' + self._artifact + '/' + "maven-metadata.xml"
        for mavenRepo in self._resolversList:
            self._logger.debug("Trying with repo: {}".format(mavenRepo.id))
            xmlData, s = mavenRepo.getFile(urlPathToFile)
            if s == HTTPStatus.OK:
                self._logger.debug("Got maven xml metadata: " + xmlData)
                break            

    def ResolvePOMfile(self) -> dict:
        '''
        Resolve the POM file and return as a dict
        '''
        pass






