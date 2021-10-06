from grpc import insecure_channel
from primrose.protobuf.primrose_pb2_grpc import SbomServiceStub
from primrose.protobuf.primrose_pb2 import SbomServiceGetByIdRequest
from json import loads as jsonLoads
from common.logger import Logger
from common.application import Application

class Primrose():
    def __init__(self):
        self.channel = insecure_channel(Application.GetInstance().ConfigData["primrose"]["grpc"])
        super().__init__()
    
    def GetSbomById(self, id):
        l = Logger.getLogger(__name__)
        l.info("Trying RPC call SbomService:get(sbomID={})".format(id))
        stub = SbomServiceStub(self.channel)
        req = SbomServiceGetByIdRequest(sbomID=id)
        resp = stub.Get(req) #blocking call
        l.debug("Got resp SBON Json: " + resp.sbom)
        return jsonLoads(resp.sbom)
        

    def CreateMaven(self, group, artifact, version, **kwargs):
        l = Logger.getLogger(__name__)
        l.info("Calling create maven API with GAV: {}, {}, {}".format(group, artifact, version))
        return "dummy-maven-doc-id"
