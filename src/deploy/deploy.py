# pyright: reportUnusedCallResult=false
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
files.sync(
    name="Upload server directory",
    src="server",
    dest="/home/azureuser",
    user="azureuser",
    group="azureuser",
)
