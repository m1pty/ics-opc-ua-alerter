import asyncio
from asyncua import Client

from opcua.logger import logger
from opcua.constants import OPC_UA_URL_CLIENT, OPC_UA_NAMESPACE, OPC_UA_VARIABLE_ID

class OpcUaClient:
    def __init__(self):
        self.client = Client(OPC_UA_URL_CLIENT)
        self.variable = None
        self.logger = logger.bind(class_name=self.__class__.__name__)

    async def init_client(self):
        max_retries = 10
        retry_delay = 2  # секунды

        for attempt in range(1, max_retries + 1):
            try:
                await self.client.connect()
                namespace_index = await self.client.get_namespace_index(OPC_UA_NAMESPACE)
                self.variable = self.client.get_node(f"ns={namespace_index};i={OPC_UA_VARIABLE_ID}")
                self.logger.info("Клиент успешно подключён к серверу.")
                return
            except Exception as e:
                self.logger.warning(f"Попытка {attempt}/{max_retries} подключения не удалась: {e}")
                if attempt < max_retries:
                    await asyncio.sleep(retry_delay)
                else:
                    self.logger.error("Не удалось подключиться к OPC UA серверу после всех попыток.")
                    raise

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