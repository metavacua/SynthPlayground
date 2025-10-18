from tooling.protocol_manager import create_protocol, update_version
from tooling.protocol_oracle import get_applicable_protocols, get_rules_for_protocols
from rdflib import Graph
import os

class ProtocolAPI:
    def __init__(self, protocols_dir="protocols", knowledge_graph_path="knowledge_core/protocols.ttl"):
        self.protocols_dir = protocols_dir
        self.knowledge_graph_path = knowledge_graph_path
        self.graph = Graph()
        if os.path.exists(self.knowledge_graph_path):
            self.graph.parse(self.knowledge_graph_path, format="turtle")

    def create_protocol(self, name, directory=None):
        if directory is None:
            directory = self.protocols_dir
        create_protocol(name, directory)

    def update_protocol_version(self, protocol_id, new_version):
        update_version(protocol_id, new_version)

    def get_applicable_rules(self, context):
        applicable_protocols = get_applicable_protocols(self.graph, context)
        return get_rules_for_protocols(self.graph, applicable_protocols)
