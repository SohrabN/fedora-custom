# Create Custom Fedora OS

This vagrant file allows you to generate custom ISO of Fedora.

## Installation

To start make sure you have vagrant on your distro.
In addition script is deigned to run with qemu kvm so make sure you already have it installed or change the Vagrantfile to use your provider.
There are couple of vagrant plugins we require so start with running the install-plugins.sh

```bash
git clone https://github.com/SohrabN/fedora-custom.git
cd fedora-custom
bash ./install-plugins.sh
```

## Usage

Bring vagrant up.

```bash
vagrant up
```

Once all operations are over, ISO is created on the vagrant box. Now we need to copy the ISO from guest to host.

```bash
bash ./copy-iso-to-host.sh
```

