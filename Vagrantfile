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
    mock -r /etc/mock/fedora-38-x86_64.cfg --init

    # Install necessary packages inside mock
    mock -r fedora-38-x86_64 --install lorax anaconda git pykickstart vim

    # Enter chroot environment and execute further commands
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
url --mirrorlist=https://mirrors.fedoraproject.org/mirrorlist?repo=fedora-38&arch=x86_64
EOF
    cat <<EOF > fedora-live-minimal-workstation.ks
%include fedora-live-workstation.ks

%packages
@hardware-support
@base-x
@firefox
@fonts
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
@libreoffice
gnome-tweaks
dnsmasq
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
EOF

    # Flatten kickstart file
    ksflatten -c fedora-live-minimal-workstation.ks -o ks.cfg

    # Create custom live image
    livemedia-creator --ks ks.cfg --no-virt --resultdir /var/lmc \
                      --project Fedora-minimal-workstation-Live --make-iso \
                      --volid Fedora-minimal-workstation-Live --iso-only \
                      --iso-name Fedora-minimal-workstation-Live.iso --releasever 38 --macboot

  MOCK
    exit

    original_ip=$(ip addr show eth0 | grep "inet " | awk '{print $2}' | cut -d/ -f1)
    modified_ip=$(echo $original_ip | sed 's/\.[0-9]*$/\.1/')
    scp Fedora-minimal-workstation-Live.iso user@${modified_ip}:.
    # Clean the build environment
    mock -r fedora-38-x86_64 --clean
  SHELL
end

