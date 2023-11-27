Vagrant.configure("2") do |config|
  config.vm.box = "fedora/38-cloud-base"
  config.vm.provider "libvirt" do |libvirt|
    libvirt.memory = 4096   # Set VM memory to 4096 MB (4 GB)
    libvirt.cpus = 4        # Set the number of CPU cores to 4
  end
  # Provisioning steps
  config.vm.provision "shell", inline: <<-SHELL
    # Install mock
    sudo dnf install -y mock

    # Add user to mock group
    sudo usermod -aG mock vagrant

    # Initialize the build environment
    mock -r /et    # Add user to mock group
    sudo usermod -aG mock vagrantc/mock/fedora-38-x86_64.cfg --init

    # Install necessary packages inside mock
    mock -r fedora-38-x86_64 --install lorax anaconda git pykickstart vim

    mock -r fedora-38-x86_64 --copyin /vagrant/vscode-extensions /vscode-extensions

    mock -r fedora-38-x86_64 --shell --isolation=simple --enable-network <<-MOCK  
     
    # Clone Fedora kickstart files
    sed -i '/\[main\]/a diskspacecheck=0' /etc/dnf/dnf.conf
    git clone https://pagure.io/fedora-kickstarts -b f38
    cd fedora-kickstarts
    cat << EOF > fedora-repo-not-rawhide.ks
repo --name=fedora --mirrorlist=https://mirrors.fedoraproject.org/mirrorlist?repo=fedora-38&arch=x86_64
repo --name=updates --mirrorlist=https://mirrors.fedoraproject.org/mirrorlist?repo=updates-released-f38&arch=x86_64
repo --name=code --baseurl=https://packages.microsoft.com/yumrepos/vscode
repo --name=rpmfusion-free --baseurl=http://download1.rpmfusion.org/free/fedora/releases/38/Everything/x86_64/os/
repo --name=copr:copr.fedorainfracloud.org:taw:joplin --baseurl=https://download.copr.fedorainfracloud.org/results/taw/joplin/fedora-38-x86_64/

url --mirrorlist=https://mirrors.fedoraproject.org/mirrorlist?repo=fedora-38&arch=x86_64
EOF
    cat <<EOF > fedora-live-minimal-workstation.ks
%include fedora-live-workstation.ks

%packages
@core
@standard
@hardware-support
@base-x
@firefox
@fonts
@printing
@multimedia
@development-tools
@networkmanager-submodules
vim
tcpdump
ansible
calc
git-review
readline-devel
libX11-devel
libXt-devel
zlib-devel
bzip2-devel
xz-devel
pcre2-devel
libcurl-devel
python3-virtualenvwrapper
python3-devel
gcc-c++
transmission-gtk
libffi-devel
jq
ristretto
xrandr
tmux
bash-color-prompt
bash-completion
nmap
netcat
sshuttle
arp-scan
hping3
wireshark
socat
python3
pipenv
python3-requests
bettercap
pipx
podman
remmina
golang
htop
jetbrains-mono-fonts
neovim
rust
realmd
git
vlc
ffmpeg
ruby-devel
libreoffice
gnome-tweaks
dnsmasq
code
joplin
# Package groups excluded from @workstation-product-environment
-@guest-desktop-agents
-@multimedia
# Packages excluded from @workstation-product
-rhythmbox
-unoconv
# Packages excluded from @gnome-desktop
-gnome-boxes
-gnome-backgrounds
-gnome-connections
-gnome-text-editor
-baobab
-cheese
-gnome-clocks
-gnome-logs
-gnome-maps
-gnome-photos
-gnome-remote-desktop
-gnome-weather
-orca
-rygel
-totem
%end

# %post
# mkdir -p /root/vscode/
# cat <<'PYSCRIPT' > /root/vscode/download-vscode-extension.py
# import argparse
# import requests
# import os
# import re

# headers = {
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
#     'Accept-Language': 'en-US,en;q=0.5',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Connection': 'keep-alive',
#     'Referer': 'https://marketplace.visualstudio.com/items?itemName=ms-python.python',
#     'Upgrade-Insecure-Requests': '1',
#     'Sec-Fetch-Dest': 'document',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'same-origin',
#     'Sec-Fetch-User': '?1',
#     'TE': 'trailers'
# }

# # Updated cookies
# cookies = {
#     'VstsSession': '%7B%22PersistentSessionId%22%3A%224550fe5a-845e-4701-904a-abc628dc754a%22%2C%22PendingAuthenticationSessionId%22%3A%2200000000-0000-0000-0000-000000000000%22%2C%22CurrentAuthenticationSessionId%22%3A%2200000000-0000-0000-0000-000000000000%22%2C%22SignInState%22%3A%7B%7D%7D',
#     'Gallery-Service-UserIdentifier': '9e61b919-76d5-404a-abb7-4f9a7266d379',
#     'Market_SelectedTab': 'vscode'
# }
# def get_latest_version(extension_id):
#     url = f"https://marketplace.visualstudio.com/items?itemName={extension_id}"
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         # Use regex to find the version number in the page content
#         match = re.search(r'"version":"([\\d.]+)"', response.text)
#         if match:
#             return match.group(1)
#     return None

# def download_extension(extension_id, save_path):
#     # Fetch the latest version number for the extension
#     version = get_latest_version(extension_id)
#     if not version:
#         print(f"Could not find version for {extension_id}")
#         return

#     # Extract publisher and extension name from the ID
#     publisher, extension_name = extension_id.split('.')

#     # Construct download URL for the .vsix file
#     download_url = f"https://marketplace.visualstudio.com/_apis/public/gallery/publishers/{publisher}/vsextensions/{extension_name}/{version}/vspackage"
    
#     print("Download URL: "+download_url)
#     # Download the extension
#     vsix_response = requests.get(download_url, headers=headers, cookies=cookies)
#     print("VSIX Responde: "+str(vsix_response.status_code))
#     if vsix_response.status_code == 200:
#         with open(os.path.join(save_path, f"{extension_id}-{version}.vsix"), 'wb') as file:
#             file.write(vsix_response.content)
#         print(f"Downloaded {extension_id} version {version}")
#     else:
#         print(f"Failed to download {extension_id} version {version}")

# def main():
#     parser = argparse.ArgumentParser(description='Download VSCode extensions.')
#     parser.add_argument('--extension', help='Extension ID to download')
#     parser.add_argument('--file', help='File containing list of extensions')
#     args = parser.parse_args()
    
#     save_path = './vscode-extensions'

#     # Check if the directory exists, if not, create it
#     if not os.path.exists(save_path):
#         os.makedirs(save_path)

#     if args.extension:
#         download_extension(args.extension, save_path)
#     elif args.file:
#         with open(args.file, 'r') as file:
#             for line in file:
#                 extension_id = line.strip()
#                 download_extension(extension_id, save_path)

# if __name__ == "__main__":
#     main()


# PYSCRIPT

# cat <<'EXTFILE' > /root/vscode/extension-list.txt
# 4ops.packer
# 4ops.terraform
# kosz78.nim
# ms-azuretools.vscode-docker
# ms-python.python
# ms-python.vscode-pylance
# ms-vscode-remote.remote-containers
# ms-vscode-remote.remote-ssh
# ms-vscode-remote.remote-ssh-edit
# ms-vscode.cmake-tools
# ms-vscode.cpptools
# ms-vscode.cpptools-extension-pack
# ms-vscode.cpptools-themes
# ms-vscode.remote-explorer
# redhat.ansible
# redhat.vscode-yaml
# twxs.cmake
# EXTFILE

# cd /root/vscode/
# python3 download-vscode-extension.py --file extension-list.txt
# cat <<'INSTALLFILE' > /root/vscode/install-ext.sh
# extension_folder="./vscode-extensions/"
# for vsix_file in "$extension_folder"*.vsix; do
#   if [ -f "$vsix_file" ]; then
#     code --install-extension "$vsix_file"
#     echo "Installed: $vsix_file"
#   fi
# done
# INSTALLFILE
# %end


EOF

    # Flatten kickstart file
    ksflatten -c fedora-live-minimal-workstation.ks -o ks.cfg

    # Create custom live image  
    livemedia-creator --ks ks.cfg --no-virt --resultdir /var/lmc \
                      --project Fedora-minimal-workstation-Live --make-iso \
                      --volid Fedora-minimal-workstation-Live --iso-only \
                      --iso-name Fedora-minimal-workstation-Live.iso --releasever 38 --macboot --image-size 10000

  MOCK
    exit
  SHELL
end

