from grpc import insecure_channel
from primrose.protobuf.primrose_pb2_grpc import SbomServiceStub, MavenDocServiceStub
import primrose.protobuf.primrose_pb2 
from json import loads as jsonLoads
from common.logger import Logger
from common.application import Application

class Primrose():
    def __init__(self):
        self._logger = Logger.getLogger(__name__)
        self.channel = insecure_channel(Application.GetInstance().ConfigData["primrose"]["grpc"])
        super().__init__()
    
    def GetSbomById(self, id):
        self._logger.info("Trying RPC call SbomService:get(sbomID={})".format(id))
        stub = SbomServiceStub(self.channel)
        req = primrose.protobuf.primrose_pb2.SbomServiceGetByIdRequest(sbomID=id)
        resp = stub.Get(req) #blocking call
        self._logger.debug("Got resp SBON Json: " + resp.sbom)
        return jsonLoads(resp.sbom)
        

    def CreateMaven(self, group, artifact, version, **kwargs):        
        self._logger.info("Calling create maven API with GAV: {}, {}, {}".format(group, artifact, version))
        stub = MavenDocServiceStub(self.channel)
        req = primrose.protobuf.primrose_pb2.MavenCreateRequest(groupID=group, artifactID=artifact,
        version=version, id=None if "id" not in kwargs else kwargs["id"],
        purl=None if "purl" not in kwargs else kwargs["purl"])
        resp = None
        try:
            resp = stub.Create(req)
        except Exception as e:
            self._logger.critical("Error occured on calling RPC.")
            self._logger.debug(e)
            return False
        self._logger.info("Got status code: {}, message: {}".format(str(resp.code), resp.msg ))
        return True if resp.code == 0 else False

    def GetMavenDocById(self, id):
        self._logger.info("Calling get maven doc using id: {}".format(id))
        stub = MavenDocServiceStub(self.channel)
        req = primrose.protobuf.primrose_pb2.MavenGetRequest(id=id)
        resp = None
        try:
            resp = stub.Get(req)
            self._logger.debug("Got resp MVN Json: " + resp.doc)
        except Exception as e:
            self._logger.critical("Error occured on calling RPC.")
            self._logger.debug(e)
            return None, None
        self._logger.info("Got status code: {}, message: {}".format(str(resp.status.code), resp.status.msg ))
        return True, jsonLoads(resp.doc) if resp.code == 0 else False, None
