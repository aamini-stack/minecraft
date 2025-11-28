# pyright: reportUnusedCallResult=false
import io

from pyinfra.operations import apt, files, server, systemd

# 1. Install JDK 21 (Adoptium)
apt.packages(
    name="Install prerequisites",
    packages=["wget", "apt-transport-https", "gpg", "curl"],
    _sudo=True,
)

apt.key(
    name="Add Adoptium GPG key",
    src="https://packages.adoptium.net/artifactory/api/gpg/key/public",
    _sudo=True,
)

apt.repo(
    name="Add Adoptium repository",
    src="deb https://packages.adoptium.net/artifactory/deb noble main",
    _sudo=True,
)

apt.update(
    name="Update apt cache",
    _sudo=True,
)

apt.packages(
    name="Install JDK 21",
    packages=["temurin-21-jdk"],
    _sudo=True,
)

apt.packages(
    name="Install podman",
    packages=["podman-docker"],
    _sudo=True,
)

# 2. Install Podman
server.shell(
    name="Enable linger for current user",
    commands=["sudo loginctl enable-linger $(whoami)"],
)

systemd.service(
    name="Enable podman user service",
    service="podman",
    enabled=True,
    user_mode=True,
)

# 3. Upload Server Files
server_files = files.sync(
    name="Upload server directory",
    src="server",
    dest="/home/azureuser/server",
    user="azureuser",
    group="azureuser",
)

# 4. Setup Systemd Service
SERVICE_FILE = """
[Unit]
Description=Minecraft Server
After=network.target

[Service]
User=azureuser
WorkingDirectory=/home/azureuser/server
ExecStart=/usr/bin/java -Xmx6G -Xms2G -jar fabric.jar nogui
Restart=on-failure

[Install]
WantedBy=multi-user.target
"""

service_file = files.put(
    name="Create minecraft service file",
    src=io.StringIO(SERVICE_FILE),
    dest="/etc/systemd/system/minecraft.service",
    _sudo=True,
)

systemd.service(
    name="Enable and start minecraft service",
    service="minecraft",
    running=True,
    enabled=True,
    _sudo=True,
)

# 5. Optional Restart
if server_files.changed or service_file.changed:
    should_restart = input(
        "Server files or service configuration changed. Restart minecraft service? (y/n): "
    )
    if should_restart.lower() == "y":
        systemd.service(
            name="Restart minecraft service",
            service="minecraft",
            restarted=True,
            _sudo=True,
        )
