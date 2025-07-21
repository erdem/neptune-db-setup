import os
from dotenv import load_dotenv
from gremlin_python.driver import client
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.driver.aiohttp.transport import AiohttpTransport
from gremlin_python.process.anonymous_traversal import traversal

load_dotenv()

class NeptuneConfig:
    def __init__(self):
        self.endpoint = os.getenv('NEPTUNE_ENDPOINT')
        self.port = os.getenv('NEPTUNE_PORT', '8182')
        self.region = os.getenv('AWS_REGION', 'us-east-1')
        self.local_endpoint = os.getenv('LOCAL_GREMLIN_ENDPOINT', 'ws://localhost:8182/gremlin')
        
    def get_connection(self, use_local=True):
        """Get Gremlin connection - use local by default for demo"""
        if use_local:
            connection_string = self.local_endpoint
        else:
            connection_string = f"wss://{self.endpoint}:{self.port}/gremlin"
            
        print(f"Connecting to: {connection_string}")
        
        try:
            # Use aiohttp transport for local connections
            transport_factory = lambda: AiohttpTransport()
            connection = DriverRemoteConnection(
                connection_string, 
                'g',
                transport_factory=transport_factory
            )
            g = traversal().withRemote(connection)
            return g, connection
        except Exception as e:
            print(f"Failed to connect: {e}")
            return None, None
            
    def get_client(self, use_local=True):
        """Get Gremlin client for raw queries"""
        if use_local:
            connection_string = self.local_endpoint
        else:
            connection_string = f"wss://{self.endpoint}:{self.port}/gremlin"
            
        transport_factory = lambda: AiohttpTransport()
        return client.Client(
            connection_string, 
            'g',
            transport_factory=transport_factory
        )