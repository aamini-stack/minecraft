# Minecraft Azure Infrastructure

## Setup

1. Install Mise: https://mise.jdx.dev/getting-started.html
2. Run `mise install`
3. Run `uv sync`
4. Run `az login`

## Provision

Setup VM

```bash
cd src/infra
pulumi up
```

Save SSH key file

```bash
cd src/infra
pulumi stack output ssh_private_key --show-secrets > ~/.ssh/minecraft-key.pem
chmod 600 ~/.ssh/minecraft-key.pem
```

Add the following entry to your `~/.ssh/config` file:

```
Host aria-minecraft.eastus2.cloudapp.azure.com
    User azureuser
    IdentityFile ~/.ssh/minecraft-key.pem
```

SSH into server

```bash
ssh aria-minecraft.eastus2.cloudapp.azure.com
```

Display outputs

```bash
pulumi stack output
```

Delete resources

```bash
pulumi destroy
```

## Deploy

```bash
uv run pyinfra aria-minecraft.eastus2.cloudapp.azure.com src/deploy/deploy.py
```

## Install Fabric

https://fabricmc.net/use/server/

## Setup Crafty

1. SSH into server
2. Start Crafty: `docker compose up -d`
3. Login to Crafty:
    - url: https://aria-minecraft.eastus2.cloudapp.azure.com:8443
    - username: admin
    - password: `sudo cat config/default-creds.txt`
4. Add Server
    - Click (servers > create new server) in left sidebar
    - Fill-in 2nd box ("Import an Existing Server"):
        - Server Name: `nostalgia`
        - Server Path: `/crafty/servers/nostalgia`
        - Server Executable File: `fabric.jar`
5. Accept EULA
6. Click start

java -Xmx6G -jar fabric.jar nogui

# Screen

```bash
# Start a tmux session
tmux new -s minecraft

# Run your server
java -Xmx6G -jar fabric.jar nogui

# Detach: Press Ctrl+B, then D

# To reattach:
tmux attach -t minecraft
```
