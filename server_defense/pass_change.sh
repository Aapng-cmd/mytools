# on home

# ssh-keygen -t ed25519 -C "your_email@example.com"

# ssh-copy-id username@server_ip_address

# on server

apt update && apt full-upgrade
apt install rsyslog git nano -y
nano /etc/ssh/sshd_config
# PasswordAuthentication no
# ChallengeResponseAuthentication no
# PubkeyAuthentication yes
# Port <smth>
# LogLevel VERBOSE
systemctl restart sshd
systemctl restart rsyslog

apt install libssh-dev libjson-c-dev libpcap-dev libssl-dev -y
git clone https://github.com/droberson/ssh-honeypot.git
cd ssh-honeypot
make
ssh-keygen -t rsa -f ./ssh-honeypot.rsa -N "" # with no pass
# you also can add version of ssh, and then
#make install
#systemctl enable --now ssh-honeypot

