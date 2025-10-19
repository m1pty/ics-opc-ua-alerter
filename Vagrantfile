# -*- mode: ruby -*-
# vi: set ft=ruby :

project_dir = "/opt/opcua-demo"

install_dependencies = <<-SHELL
  set -e

  sudo apt-get update

  echo "=== Установка зависимостей ==="
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential autoconf automake libtool \
    libpcap-dev libnet1-dev libyaml-dev libjansson-dev \
    liblz4-dev libmagic-dev libpcre2-dev zlib1g-dev \
    pkg-config python3-distutils libmaxminddb-dev \
    liblua5.1-dev python3-pip python3-venv tshark jq \
    git libcap-ng-dev libcap-ng0 cargo rustc

  echo "=== Установка Rust ==="
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
  source "$HOME/.cargo/env"
  cargo install --force cbindgen
SHELL

setup_project_and_suricata = <<-SHELL
  echo "=== Настройка проекта ==="
  
  sudo mkdir -p "#{project_dir}"
  sudo chown -R vagrant:vagrant "#{project_dir}"
  cp -r /vagrant/* "#{project_dir}/"
  cd "#{project_dir}"

  if [ ! -f requirements.txt ]; then
    echo "ERROR: requirements.txt not found"
    exit 1
  fi
  if [ ! -d opcua ] || [ ! -f opcua/__init__.py ]; then
    echo "ERROR: opcua/ module is missing"
    exit 1
  fi
  if [ ! -f suricata/suricata.yaml ] || [ ! -f suricata/rules/opcua.rules ]; then
    echo "ERROR: Suricata config or rules missing"
    exit 1
  fi

  echo "=== Сборка Suricata 7.0 ==="
  cd /tmp
  git clone https://github.com/OISF/suricata.git
  cd suricata
  git checkout main-7.0.x
  git submodule update --init
  git clone https://github.com/OISF/libhtp libhtp

  ./autogen.sh

  # python3 scripts/setup-app-layer.py --detect --logger --parser OPCUA OPCUABuffer

  ./configure \
    --prefix=/usr \
    --sysconfdir=/etc \
    --localstatedir=/var \
    --enable-gccmarch-native \
    --enable-geoip

  make -j$(nproc)
  sudo make install
  sudo make install-conf
  sudo mkdir -p /var/log/suricata /var/lib/suricata/data

  # Отключаем сурикату (в будущем мб убрать)
  echo "=== Отключение Suricata ==="
  sudo systemctl stop suricata 2>/dev/null || true
  sudo systemctl disable suricata 2>/dev/null || true
SHELL

setup_python = <<-SHELL
  echo "=== Установка Python-зависимостей ==="
  cd "#{project_dir}"
  python3 -m venv .venv
  .venv/bin/pip install --quiet -r requirements.txt
  mkdir -p logs

  echo "=== Установка завершена ==="
SHELL

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  config.vm.hostname = "opcua-suricata-fromgit"

  config.vm.network "forwarded_port", guest: 4840, host: 4840, auto_correct: true
  config.vm.network "private_network", ip: "192.168.60.10"

  config.vm.provider "virtualbox" do |vb|
    vb.name = "opcua-suricata-fromgit"
    vb.memory = "4096"
    vb.cpus = 2
  end

  config.vm.provision "shell", inline: install_dependencies
  config.vm.provision "shell", inline: setup_project_and_suricata
  config.vm.provision "shell", inline: setup_python
end