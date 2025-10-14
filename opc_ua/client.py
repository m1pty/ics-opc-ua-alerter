import asyncio
from asyncua import Client

from opc_ua.logger import logger
from opc_ua.constants import OPC_UA_URL_CLIENT, OPC_UA_NAMESPACE, OPC_UA_VARIABLE_ID

class OpcUaClient:
    def __init__(self):
        self.client = Client(OPC_UA_URL_CLIENT)
        self.variable = None
        self.logger = logger.bind(class_name=self.__class__.__name__)

    async def init_client(self):
        await self.client.connect()
        namespace_index = await self.client.get_namespace_index(OPC_UA_NAMESPACE)
        self.variable = self.client.get_node(f"ns={namespace_index};i={OPC_UA_VARIABLE_ID}")
        self.logger.info("Клиент запущен, Ctrl+C чтобы выйти.")

    async def async_run(self):
        await self.init_client()
        value = 0

        try:
            while True:
                value = (value + 1) % 10
                await self.variable.set_value(value)
                self.logger.debug(f"Значение переменной изменено на {value}")
                await asyncio.sleep(1)

        except KeyboardInterrupt:
            self.logger.info("Клиент останавливается")

        finally:
            await self.client.disconnect()

    def run(self):
        asyncio.run(self.async_run())

if __name__ == "__main__":
    client = OpcUaClient()
    client.run()
