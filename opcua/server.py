import asyncio
from asyncua import Server, ua, Node
from asyncua.tools import SubHandler

from opcua.logger import logger
from opcua.constants import OPC_UA_URL_SERVER, OPC_UA_NAMESPACE, OPC_UA_VARIABLE_NAME, OPC_UA_VARIABLE_ID

class DataChangeHandler(SubHandler):
    def __init__(self, _logger):
        self.logger = _logger

    def datachange_notification(self, node: Node, val, data):
        self.logger.info(f"Node {node.nodeid.Identifier}: Namespace {node.nodeid.NamespaceIndex}: New value - {val}")

class OpcUaServer:
    SUB_PERIOD_MS = 100

    def __init__(self):
        self.server = Server()
        self.variable = None
        self.subscription = None
        self.logger = logger.bind(class_name=self.__class__.__name__)

    async def init_server(self):
        await self.server.init()
        self.server.set_endpoint(OPC_UA_URL_SERVER)
        idx = await self.server.register_namespace(OPC_UA_NAMESPACE)
        objects = self.server.nodes.objects
        nodeid = ua.NodeId(Identifier=OPC_UA_VARIABLE_ID, NamespaceIndex=idx)
        self.variable = await objects.add_variable(nodeid, OPC_UA_VARIABLE_NAME, 0)
        await self.variable.set_writable()
        await self.server.start()

    async def create_subscription(self):
        handler = DataChangeHandler(self.logger)
        self.subscription = await self.server.create_subscription(self.SUB_PERIOD_MS, handler)
        await self.subscription.subscribe_data_change(self.variable)

    async def async_run(self):
        await self.init_server()
        await self.create_subscription()
        self.logger.info("Сервер запущен, Ctrl+C чтобы выйти.")

        try:
            while True:
                await asyncio.sleep(1)

        except KeyboardInterrupt:
            self.logger.info("Сервер останавливается")

        finally:
            await self.subscription.delete()
            await self.server.stop()

    def run(self):
        asyncio.run(self.async_run())

if __name__ == "__main__":
    server = OpcUaServer()
    server.run()