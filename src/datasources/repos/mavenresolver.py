'''
Helper class to resolve maven details from different available repos, based on resoultion order.

'''

from collections import deque
import string

class abstractMavenResolver:
    def __init__(self, id, url, user, password ) -> None:
        self.id = id
        self.url = url
        self.user = user
        self.password = password
    def getFile(self, name) -> string:
        '''
        Fetch the file from maven repo.
        '''

class MavenResolver:
    def __init__(self, group, artifact, version) -> None:
        self._resolversQueue = deque(maxlen=5)
        self._group = group
        self._artifact = artifact
        self._version = version

    def _getNextResolver(self) -> abstractMavenResolver:
        '''
        Pop the next resolver from the queue.
        '''
        pass

    def _fillTheResolverQueue(self):
        '''
        Create all the configured resolvers and add it in queue based on order.
        '''
        pass

    def ResolveMetadata(self) -> dict:
        '''
        Resolve the metadata xml and return it as json dict.
        '''
        pass

    def ResolvePOMfile(self) -> dict:
        '''
        Resolve the POM file and return as a dict
        '''
        pass

class centralMavenResolver(abstractMavenResolver):
    '''
    Extends the abstractMavenResolver, to provide functionaliy to resolve
    any files from central maven repo.
    '''





