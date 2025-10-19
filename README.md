<<<<<<< HEAD
# ics-opc-ua-alerter
=======
# Анализ промышленного протокола OPC UA

#### Для запуска проекта через `Vagrant`:

```bash
# Запуск Vagrant и подключение к ВМ
vagrant up
vagrant ssh
```

```bash
# Запуск сервера и клиента
cd /opt/opcua-demo/
.venv/bin/python3 -m opcua.server
.venv/bin/python3 -m opcua.client
```

```bash
# Для захвата трафика через tshark
sudo tshark -i lo -f "tcp port 4840"
```

```bash
# Запуск сурикаты и проверка (также из /opt/opcua-demo)
# После разархивирования suricata лежит в /tmp
sudo suricata -c ./suricata/suricata.yaml -i lo -v
tail -f ./logs/eve.json | jq 'select(.event_type == "alert")'
```

#### Для локального запуска:

##### Через Poetry:

1. Установка poetry:

    ```bash
    pip install poetry
    ```

2. Создайте виртуальное окружение и установите зависимости:

   ```bash
   poetry config virtualenvs.in-project true --local
   poetry install
   ```

3. Запуск сервера и клиента:

    ```bash
    poetry run python -m opcua.server
    poetry run python -m opcua.client
    ```

##### Через venv:

1. Создайте виртуальное окружение:

   ```bash
   python -m venv .venv
   ```

2. Активируйте и установите зависимости:

   ```bash
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Запуск сервера и клиента:

   ```bash
   python -m opcua.server
   python -m opcua.client
   ```
>>>>>>> f56b048 (Initial commit: OPC UA client/server + Suricata rules + Vagrant setup)
