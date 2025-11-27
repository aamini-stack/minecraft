import pulumi_azure_native.compute as compute
import pulumi_azure_native.network as network
import pulumi_azure_native.resources as resources
import pulumi_tls as tls
from pulumi import Config, export

# Configuration
config = Config()
vm_size = config.get("vmSize") or "Standard_D2ps_v6"
vnet_address_space = config.get("vnetAddressSpace") or "10.0.0.0/16"
subnet_address_prefix = config.get("subnetAddressPrefix") or "10.0.1.0/24"

# Resource Group
resource_group = resources.ResourceGroup("minecraft-rg")

# Generate SSH Key
ssh_key = tls.PrivateKey(
    "minecraft-ssh-key",
    algorithm="RSA",
    rsa_bits=4096,
)

# Virtual Network
vnet = network.VirtualNetwork(
    "vnet-eastus2",
    resource_group_name=resource_group.name,
    address_space=network.AddressSpaceArgs(
        address_prefixes=[vnet_address_space],
    ),
)

# Subnet
subnet = network.Subnet(
    "snet-eastus2-1",
    subnet_name="snet-eastus2-1",
    resource_group_name=resource_group.name,
    virtual_network_name=vnet.name,
    address_prefix=subnet_address_prefix,
)

# Public IP
public_ip = network.PublicIPAddress(
    "minecraft-vm-ip",
    public_ip_address_name="minecraft-vm-ip",
    resource_group_name=resource_group.name,
    public_ip_allocation_method=network.IPAllocationMethod.STATIC,
    sku=network.PublicIPAddressSkuArgs(
        name=network.PublicIPAddressSkuName.STANDARD,
    ),
    dns_settings={"domain_name_label": "aria-minecraft"},
)

# Network Security Group
nsg = network.NetworkSecurityGroup(
    "minecraft-vm-nsg",
    network_security_group_name="minecraft-vm-nsg",
    resource_group_name=resource_group.name,
    security_rules=[
        network.SecurityRuleArgs(
            name="SSH",
            priority=1000,
            direction=network.SecurityRuleDirection.INBOUND,
            access=network.SecurityRuleAccess.ALLOW,
            protocol=network.SecurityRuleProtocol.TCP,
            source_port_range="*",
            destination_port_range="22",
            source_address_prefix="*",
            destination_address_prefix="*",
        ),
        network.SecurityRuleArgs(
            name="Minecraft",
            priority=1001,
            direction=network.SecurityRuleDirection.INBOUND,
            access=network.SecurityRuleAccess.ALLOW,
            protocol=network.SecurityRuleProtocol.TCP,
            source_port_range="*",
            destination_port_range="25565",
            source_address_prefix="*",
            destination_address_prefix="*",
        ),
        network.SecurityRuleArgs(
            name="Crafty",
            priority=1002,
            direction=network.SecurityRuleDirection.INBOUND,
            access=network.SecurityRuleAccess.ALLOW,
            protocol=network.SecurityRuleProtocol.TCP,
            source_port_range="*",
            destination_port_range="8443",
            source_address_prefix="*",
            destination_address_prefix="*",
        ),
    ],
)

# Network Interface
nic = network.NetworkInterface(
    "minecraft-vm-nic",
    network_interface_name="minecraft-vm-nic",
    resource_group_name=resource_group.name,
    network_security_group=network.NetworkSecurityGroupArgs(
        id=nsg.id,
    ),
    ip_configurations=[
        network.NetworkInterfaceIPConfigurationArgs(
            name="ipconfig1",
            subnet=network.SubnetArgs(
                id=subnet.id,
            ),
            public_ip_address=network.PublicIPAddressArgs(
                id=public_ip.id,
            ),
            private_ip_allocation_method=network.IPAllocationMethod.DYNAMIC,
        ),
    ],
    enable_accelerated_networking=True,
)

# Virtual Machine
vm = compute.VirtualMachine(
    "minecraft-vm",
    resource_group_name=resource_group.name,
    network_profile=compute.NetworkProfileArgs(
        network_interfaces=[
            compute.NetworkInterfaceReferenceArgs(
                id=nic.id,
                primary=True,
            ),
        ],
    ),
    hardware_profile=compute.HardwareProfileArgs(
        vm_size=vm_size,
    ),
    storage_profile=compute.StorageProfileArgs(
        os_disk=compute.OSDiskArgs(
            name="minecraft-vm-osdisk",
            caching=compute.CachingTypes.READ_WRITE,
            create_option=compute.DiskCreateOptionTypes.FROM_IMAGE,
            managed_disk=compute.ManagedDiskParametersArgs(
                storage_account_type=compute.StorageAccountTypes.PREMIUM_LRS,
            ),
            delete_option=compute.DiskDeleteOptionTypes.DELETE,
        ),
        image_reference=compute.ImageReferenceArgs(
            publisher="Canonical",
            offer="ubuntu-24_04-lts",
            sku="server-arm64",
            version="latest",
        ),
    ),
    os_profile=compute.OSProfileArgs(
        computer_name="minecraft-vm",
        admin_username="azureuser",
        linux_configuration=compute.LinuxConfigurationArgs(
            disable_password_authentication=True,
            ssh=compute.SshConfigurationArgs(
                public_keys=[
                    compute.SshPublicKeyArgs(
                        path="/home/azureuser/.ssh/authorized_keys",
                        key_data=ssh_key.public_key_openssh,
                    ),
                ],
            ),
        ),
    ),
    security_profile=compute.SecurityProfileArgs(
        security_type=compute.SecurityTypes.TRUSTED_LAUNCH,
        uefi_settings=compute.UefiSettingsArgs(
            secure_boot_enabled=True,
            v_tpm_enabled=True,
        ),
    ),
    diagnostics_profile=compute.DiagnosticsProfileArgs(
        boot_diagnostics=compute.BootDiagnosticsArgs(
            enabled=True,
        ),
    ),
)

# Exports
export("resource_group_name", resource_group.name)
export("vm_name", vm.name)
export("vm_id", vm.id)
export("public_ip_address", public_ip.ip_address)
export(
    "server_url",
    public_ip.dns_settings.apply(lambda dns: dns.fqdn if dns else ""),
)
export("ssh_private_key", ssh_key.private_key_pem)
