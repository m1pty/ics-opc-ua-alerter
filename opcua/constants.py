import os

OPC_UA_URL_SERVER = os.getenv("OPC_UA_URL_SERVER", "opc.tcp://0.0.0.0:4840/freeopcua/server/")
OPC_UA_URL_CLIENT = os.getenv("OPC_UA_URL_CLIENT", "opc.tcp://192.168.60.10:4840/freeopcua/server/")
OPC_UA_NAMESPACE = "opcua_ns"
OPC_UA_VARIABLE_NAME = "opcua_var"
OPC_UA_VARIABLE_ID = 1