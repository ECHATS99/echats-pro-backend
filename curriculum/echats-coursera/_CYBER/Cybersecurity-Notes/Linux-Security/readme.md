🐧 Linux Security Hardening Guide
Last Updated: December 2024 | Version: 2.1 | Author: Nicole Dominique Montederamos

📚 Table of Contents
System Hardening Fundamentals

User & Permission Management

Service & Process Security

Filesystem Security

Network Security Configuration

Kernel & System Tuning

Auditing & Monitoring

Security Tools & Automation

Container Security

Compliance Standards

Quick Reference Cheatsheet

System Hardening Fundamentals
🔧 Initial Security Assessment
System Information Gathering:

bash
# System overview
uname -a
cat /etc/os-release
hostnamectl

# Security patch status
yum check-update      # RHEL/CentOS
apt list --upgradable # Debian/Ubuntu

# Check SELinux/AppArmor status
sestatus              # SELinux
aa-status             # AppArmor

# List installed packages
rpm -qa               # RHEL
dpkg -l               # Debian
Security Benchmark Assessment:

bash
# Using Lynis for security auditing
sudo lynis audit system --quick

# Check for common vulnerabilities
sudo apt-get install tiger
sudo tiger -e

# Basic security scan
sudo apt-get install rkhunter chkrootkit
sudo rkhunter --check
sudo chkrootkit
🏗️ Base System Hardening
Minimal Installation Principles:

bash
# For new installations, choose minimal/base install
# Remove unnecessary packages
sudo apt-get remove --purge xserver-* libreoffice-*
sudo apt-get autoremove
sudo apt-get clean

# Disable unnecessary kernel modules
echo "install bluetooth /bin/false" >> /etc/modprobe.d/disable_modules.conf
echo "install net-pf-31 /bin/false" >> /etc/modprobe.d/disable_modules.conf
echo "install dccp /bin/false" >> /etc/modprobe.d/disable_modules.conf
System Update Automation:

bash
# Configure automatic security updates
sudo apt-get install unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades

# /etc/apt/apt.conf.d/50unattended-upgrades
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
    "${distro_id}ESMApps:${distro_codename}-apps-security";
    "${distro_id}ESM:${distro_codename}-infra-security";
};
Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-Time "02:00";
User & Permission Management
👥 User Account Security
Account Policies Configuration:

bash
# /etc/login.defs configuration
PASS_MAX_DAYS   90
PASS_MIN_DAYS   1
PASS_MIN_LEN    14
PASS_WARN_AGE   7

# Install and configure pam_pwquality
sudo apt-get install libpam-pwquality
# /etc/security/pwquality.conf
minlen = 14
minclass = 4
maxrepeat = 3
maxsequence = 4
Secure Password Policies:

bash
# Configure PAM for password complexity
# /etc/pam.d/common-password
password requisite pam_pwquality.so retry=3 minlen=14 difok=3 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1

# Lock inactive accounts
sudo useradd -D -f 30  # 30 days inactive
sudo chage -I 30 -m 1 -M 90 -W 7 username
Sudo Configuration Hardening:

bash
# /etc/sudoers secure configuration
Defaults        timestamp_timeout=5
Defaults        passwd_timeout=0
Defaults        requiretty
Defaults        env_reset
Defaults        mail_always
Defaults        secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Limit sudo access
# /etc/sudoers.d/secure_admin
%admin ALL=(ALL) ALL
%sudo ALL=(ALL:ALL) ALL
User_Alias SECURITY_ADMINS = alice, bob
SECURITY_ADMINS ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart ssh
🔐 Privilege Escalation Prevention
SUID/SGID Management:

bash
# Find SUID/SGID files
find / -type f \( -perm -4000 -o -perm -2000 \) -exec ls -l {} \; 2>/dev/null

# Remove SUID from unnecessary binaries
sudo chmod u-s /usr/bin/find
sudo chmod u-s /usr/bin/nmap
sudo chmod u-s /usr/sbin/traceroute

# Common SUID files to review:
# /usr/bin/passwd, /usr/bin/sudo, /usr/bin/pkexec, /bin/su
Capabilities Management:

bash
# List capabilities
getcap -r / 2>/dev/null

# Remove dangerous capabilities
sudo setcap -r /usr/bin/ping
sudo setcap -r /usr/sbin/arping

# Example capabilities configuration
sudo setcap cap_net_raw+p /usr/bin/ping
Service & Process Security
🚀 Service Hardening
Systemd Service Security:

ini
# Example: Secure SSH service unit override
# /etc/systemd/system/ssh.service.d/security.conf
[Service]
CapabilityBoundingSet=CAP_DAC_OVERRIDE CAP_DAC_READ_SEARCH CAP_AUDIT_WRITE CAP_CHOWN CAP_NET_BIND_SERVICE CAP_SETGID CAP_SETUID CAP_SYS_CHROOT
NoNewPrivileges=yes
PrivateTmp=yes
PrivateDevices=yes
ProtectHome=yes
ProtectSystem=strict
ReadWritePaths=/var/log /var/run/sshd
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6
RestrictNamespaces=yes
RestrictRealtime=yes
SystemCallArchitectures=native
SystemCallFilter=@system-service
UMask=0077
Network Service Configuration:

bash
# SSH Hardening
# /etc/ssh/sshd_config
Protocol 2
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AllowUsers alice bob
ClientAliveInterval 300
ClientAliveCountMax 2
MaxAuthTries 3
LoginGraceTime 60
X11Forwarding no
AllowTcpForwarding no
PermitTunnel no
AllowAgentForwarding no

# Restart SSH with new config
sudo systemctl restart sshd
sudo systemctl reload sshd
Disable Unnecessary Services:

bash
# List all services
systemctl list-unit-files --type=service

# Disable unnecessary services
sudo systemctl disable bluetooth.service
sudo systemctl disable cups.service
sudo systemctl disable avahi-daemon.service
sudo systemctl disable rpcbind.service

# Mask services to prevent accidental start
sudo systemctl mask nfs-server.service
🛡️ Process Isolation
Namespace and Control Groups:

bash
# Create a secure namespace for a process
unshare --fork --pid --mount-proc --net --ipc --uts --user --map-root-user /bin/bash

# Using cgroups v2 for resource limits
sudo mkdir /sys/fs/cgroup/secure_app
echo "+cpu +memory +pids" > /sys/fs/cgroup/cgroup.subtree_control
echo "50000 100000" > /sys/fs/cgroup/secure_app/cpu.max
echo "100M" > /sys/fs/cgroup/secure_app/memory.max
Seccomp and Security Modules:

bash
# Check seccomp status for a process
grep Seccomp /proc/$$/status

# Using seccomp with systemd
[Service]
SystemCallFilter=@system-service @privileged @default
SystemCallErrorNumber=EPERM
Filesystem Security
📁 Filesystem Configuration
Secure Mount Options:

bash
# /etc/fstab secure configuration
/dev/sda1 /     ext4 defaults,noexec,nosuid,nodev 0 1
/dev/sda2 /home ext4 defaults,nosuid,nodev        0 2
/dev/sda3 /tmp  ext4 defaults,noexec,nosuid,nodev 0 2
/dev/sda4 /var  ext4 defaults,nosuid              0 2

# Special filesystems
tmpfs   /dev/shm  tmpfs defaults,noexec,nosuid,size=1G 0 0
tmpfs   /tmp      tmpfs defaults,noexec,nosuid,size=2G 0 0

# Apply changes
sudo mount -o remount /home
sudo mount -o remount /tmp
File and Directory Permissions:

bash
# Set secure permissions for system directories
sudo chmod 750 /etc/sudoers.d
sudo chmod 700 /root
sudo chmod 755 /usr/bin
sudo chmod 644 /etc/passwd
sudo chmod 600 /etc/shadow
sudo chmod 640 /etc/group

# World-writable file detection
find / -type f -perm -0002 -exec ls -l {} \; 2>/dev/null
find / -type d -perm -0002 -exec ls -ld {} \; 2>/dev/null
Access Control Lists (ACLs):

bash
# Install ACL support
sudo apt-get install acl

# Set ACL for sensitive directories
sudo setfacl -m u:alice:r-x /etc/ssl/private
sudo setfacl -m g:security:rw- /var/log/auth.log
sudo setfacl -d -m u::rwx,g::r-x,o::--- /secure/data

# View ACLs
getfacl /etc/ssl/private
🔐 Disk Encryption
LUKS Encryption Setup:

bash
# Install encryption tools
sudo apt-get install cryptsetup

# Encrypt a new device
sudo cryptsetup luksFormat /dev/sdb1
sudo cryptsetup open /dev/sdb1 secure_volume

# Create filesystem
sudo mkfs.ext4 /dev/mapper/secure_volume

# Add to /etc/crypttab
secure_volume /dev/sdb1 none luks

# Add to /etc/fstab
/dev/mapper/secure_volume /secure ext4 defaults 0 2
eCryptFS for Home Directories:

bash
# Install ecryptfs-utils
sudo apt-get install ecryptfs-utils

# Migrate user to encrypted home
sudo ecryptfs-migrate-home -u username

# Setup encrypted private directory
ecryptfs-setup-private
Network Security Configuration
🌐 Firewall Configuration
iptables/nftables Setup:

bash
# Basic iptables firewall
sudo iptables -F
sudo iptables -X
sudo iptables -Z

# Default policies
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT

# Allow loopback
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT

# Allow established connections
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow SSH
sudo iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -j ACCEPT

# Save rules
sudo iptables-save > /etc/iptables/rules.v4
nftables Modern Configuration:

bash
# /etc/nftables.conf
#!/usr/sbin/nft -f

flush ruleset

table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;
        
        # Allow loopback
        iifname "lo" accept
        
        # Allow established connections
        ct state established,related accept
        
        # Allow SSH
        tcp dport 22 ct state new accept
        
        # ICMP
        ip protocol icmp accept
        ip6 nexthdr ipv6-icmp accept
        
        # Log and reject
        log prefix "nftables-input-drop: " group 0
        reject with icmp type port-unreachable
    }
    
    chain forward {
        type filter hook forward priority 0; policy drop;
    }
    
    chain output {
        type filter hook output priority 0; policy accept;
    }
}
🛡️ Network Stack Hardening
sysctl Network Hardening:

bash
# /etc/sysctl.d/99-security.conf
# IP Spoofing protection
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# Ignore ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv6.conf.default.accept_redirects = 0

# Ignore send redirects
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0

# SYN Flood protection
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 2048
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 5

# Log martians
net.ipv4.conf.all.log_martians = 1
net.ipv4.icmp_ignore_bogus_error_responses = 1

# Apply changes
sudo sysctl -p /etc/sysctl.d/99-security.conf
TCP/IP Stack Tuning:

bash
# Additional TCP hardening
echo "net.ipv4.tcp_timestamps = 0" >> /etc/sysctl.d/99-security.conf
echo "net.ipv4.tcp_rfc1337 = 1" >> /etc/sysctl.d/99-security.conf
echo "net.ipv4.tcp_sack = 0" >> /etc/sysctl.d/99-security.conf
echo "net.ipv4.tcp_dsack = 0" >> /etc/sysctl.d/99-security.conf
echo "net.ipv4.tcp_fack = 0" >> /etc/sysctl.d/99-security.conf
Kernel & System Tuning
⚙️ Kernel Security Modules
SELinux Configuration:

bash
# Check SELinux status
sestatus
getenforce

# Set SELinux to enforcing
sudo setenforce 1
sudo sed -i 's/SELINUX=permissive/SELINUX=enforcing/g' /etc/selinux/config

# View SELinux contexts
ls -Z /etc/passwd
ps auxZ | grep ssh

# Manage SELinux policies
sudo semanage port -a -t http_port_t -p tcp 8080
sudo setsebool -P httpd_can_network_connect 1
AppArmor Configuration:

bash
# Check AppArmor status
sudo aa-status

# Install profiles
sudo apt-get install apparmor-profiles apparmor-utils

# Put a program in complain mode
sudo aa-complain /usr/sbin/nginx

# Generate new profile
sudo aa-genprof /usr/local/bin/myapp

# Enforce profile
sudo aa-enforce /usr/sbin/nginx
Kernel Module Security:

bash
# List loaded modules
lsmod

# Blacklist unnecessary modules
echo "blacklist bluetooth" >> /etc/modprobe.d/blacklist.conf
echo "blacklist firewire-core" >> /etc/modprobe.d/blacklist.conf
echo "install dccp /bin/false" >> /etc/modprobe.d/disable_modules.conf

# Secure module loading
echo "kernel.modules_disabled=1" >> /etc/sysctl.d/99-security.conf
🔒 Kernel Security Features
Kernel Self Protection:

bash
# Check kernel protection status
cat /proc/sys/kernel/kptr_restrict
cat /proc/sys/kernel/dmesg_restrict
cat /proc/sys/kernel/perf_event_paranoid

# Enable protections
echo "kernel.kptr_restrict = 2" >> /etc/sysctl.d/99-security.conf
echo "kernel.dmesg_restrict = 1" >> /etc/sysctl.d/99-security.conf
echo "kernel.perf_event_paranoid = 3" >> /etc/sysctl.d/99-security.conf
echo "kernel.yama.ptrace_scope = 2" >> /etc/sysctl.d/99-security.conf
Control Groups v2:

bash
# Enable cgroups v2
sudo sed -i 's/GRUB_CMDLINE_LINUX=""/GRUB_CMDLINE_LINUX="systemd.unified_cgroup_hierarchy=1"/g' /etc/default/grub
sudo update-grub

# Create secure cgroup
sudo mkdir /sys/fs/cgroup/secure_app
echo "+memory +pids +cpu" > /sys/fs/cgroup/cgroup.subtree_control
echo "100M" > /sys/fs/cgroup/secure_app/memory.max
echo "1000" > /sys/fs/cgroup/secure_app/pids.max
Auditing & Monitoring
🔍 System Auditing
Auditd Configuration:

bash
# Install audit framework
sudo apt-get install auditd audispd-plugins

# /etc/audit/auditd.conf configuration
max_log_file = 50
num_logs = 5
max_log_file_action = keep_logs
space_left = 75
space_left_action = email
action_mail_acct = root
admin_space_left = 50
admin_space_left_action = halt
Key Audit Rules:

bash
# /etc/audit/rules.d/audit.rules
## Monitor file access
-w /etc/passwd -p wa -k identity
-w /etc/group -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/sudoers -p wa -k identity
-w /etc/sudoers.d -p wa -k identity

## Monitor system calls
-a always,exit -F arch=b64 -S adjtimex -S settimeofday -k time-change
-a always,exit -F arch=b64 -S clock_settime -k time-change
-a always,exit -F arch=b64 -S sethostname -S setdomainname -k system-locale

## Monitor process execution
-a always,exit -F arch=b64 -S execve -k process-execution

## Monitor network configuration
-w /etc/hosts -p wa -k network-modification
-w /etc/network/ -p wa -k network-modification

# Apply rules
sudo auditctl -R /etc/audit/rules.d/audit.rules
Log Monitoring Scripts:

bash
#!/bin/bash
# security_monitor.sh

# Monitor failed login attempts
grep "Failed password" /var/log/auth.log | tail -20

# Monitor sudo usage
grep "sudo:" /var/log/auth.log | tail -10

# Check for new SUID files
find / -type f -perm -4000 -exec ls -l {} \; 2>/dev/null > /tmp/suid_files.new
diff /tmp/suid_files.old /tmp/suid_files.new

# Monitor open ports
netstat -tulpn | grep LISTEN

# Check for unusual processes
ps aux --sort=-%cpu | head -10
📊 Security Information Collection
System Health Monitoring:

bash
#!/bin/bash
# system_security_report.sh

echo "=== Security Report $(date) ==="
echo

echo "1. User Information:"
echo "-------------------"
lastlog | grep -v "Never logged in"
echo

echo "2. Failed Login Attempts:"
echo "-------------------------"
grep "Failed password" /var/log/auth.log | wc -l
echo

echo "3. Open Ports:"
echo "--------------"
ss -tulpn
echo

echo "4. Recent Auth Log:"
echo "------------------"
tail -20 /var/log/auth.log
echo

echo "5. File Integrity Check:"
echo "-----------------------"
rpm -Va 2>/dev/null | head -20 || dpkg --verify 2>/dev/null | head -20
Automated Security Scanning:

bash
# Daily security scan script
#!/bin/bash
LOGFILE="/var/log/security_scan_$(date +%Y%m%d).log"

{
    echo "=== Daily Security Scan - $(date) ==="
    echo
    
    echo "1. System Updates:"
    apt-get update && apt-get upgrade --dry-run
    
    echo "2. Rootkit Scan:"
    rkhunter --check --skip-keypress
    
    echo "3. File Integrity:"
    aide --check
    
    echo "4. Log Analysis:"
    grep -i "failed\|error\|denied" /var/log/auth.log | tail -50
    
    echo "5. Network Connections:"
    netstat -an | grep ESTABLISHED
    
} > "$LOGFILE" 2>&1
Security Tools & Automation
🛠️ Essential Security Tools
Installation and Configuration:

bash
# Security suite installation
sudo apt-get install \
    fail2ban \
    aide \
    rkhunter \
    chkrootkit \
    lynis \
    tiger \
    auditd \
    apparmor-utils \
    libpam-pwquality \
    ufw \
    unattended-upgrades
Fail2ban Configuration:

ini
# /etc/fail2ban/jail.local
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5
banaction = iptables-multiport
backend = systemd

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log

[ssh-ddos]
enabled = true
port = ssh
filter = sshd-ddos
logpath = /var/log/auth.log
maxretry = 10

[apache-auth]
enabled = true
filter = apache-auth
port = http,https
logpath = /var/log/apache2/*error.log
AIDE (Advanced Intrusion Detection Environment):

bash
# Initialize AIDE database
sudo aideinit

# Daily check configuration
# /etc/cron.daily/aide-check
#!/bin/bash
/usr/bin/aide --check > /var/log/aide/check_$(date +%Y%m%d).log 2>&1
if [ $? -ne 0 ]; then
    mail -s "AIDE Check Failed on $(hostname)" root < /var/log/aide/check_$(date +%Y%m%d).log
fi

# Update database after legitimate changes
sudo aide --update
sudo cp /var/lib/aide/aide.db.new.gz /var/lib/aide/aide.db.gz
🤖 Automation Scripts
Automated Hardening Script:

bash
#!/bin/bash
# auto_harden.sh

set -e

echo "Starting automated system hardening..."

# Update system
apt-get update && apt-get upgrade -y

# Install security tools
apt-get install -y unattended-upgrades fail2ban aide rkhunter ufw

# Configure firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw enable

# Configure automatic updates
dpkg-reconfigure -plow unattended-upgrades

# Harden SSH
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config
sed -i 's/PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config
systemctl restart sshd

# Configure auditd
systemctl enable auditd
systemctl start auditd

echo "Hardening complete!"
Security Compliance Check:

bash
#!/bin/bash
# compliance_check.sh

SCORE=0
TOTAL=20

check_command() {
    if command -v $1 &> /dev/null; then
        echo "✓ $2"
        ((SCORE++))
    else
        echo "✗ $2"
    fi
}

echo "=== Security Compliance Check ==="
echo

check_command ufw "Firewall installed"
check_command fail2ban-server "Fail2ban installed"
check_command aide "File integrity checker installed"
check_command lynis "Security auditor installed"

# Check configurations
if grep -q "PasswordAuthentication no" /etc/ssh/sshd_config; then
    echo "✓ SSH password authentication disabled"
    ((SCORE++))
fi

if grep -q "PermitRootLogin no" /etc/ssh/sshd_config; then
    echo "✓ SSH root login disabled"
    ((SCORE++))
fi

echo
echo "Compliance Score: $SCORE/$TOTAL"
Container Security
🐳 Docker Security
Docker Daemon Configuration:

json
// /etc/docker/daemon.json
{
  "icc": false,
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "live-restore": true,
  "userland-proxy": false,
  "no-new-privileges": true,
  "storage-driver": "overlay2",
  "userns-remap": "default",
  "default-ulimits": {
    "nofile": {
      "Name": "nofile",
      "Hard": 64000,
      "Soft": 64000
    }
  }
}
Secure Dockerfile Best Practices:

dockerfile
FROM alpine:latest

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Install only necessary packages
RUN apk add --no-cache python3 py3-pip \
    && pip3 install --no-cache-dir flask

# Set working directory
WORKDIR /app

# Copy application files
COPY --chown=appuser:appgroup app.py requirements.txt ./

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run application
CMD ["python3", "app.py"]
Container Runtime Security:

bash
# Run container with security options
docker run -d \
  --name secure-app \
  --read-only \
  --security-opt=no-new-privileges \
  --security-opt=seccomp=/path/to/seccomp/profile.json \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  --memory=512m \
  --cpus="1.0" \
  --pids-limit=100 \
  --ulimit nofile=1024:1024 \
  --user=1000:1000 \
  nginx:alpine

# Scan container images for vulnerabilities
docker scan nginx:alpine
🔒 Container Orchestration Security
Kubernetes Security Context:

yaml
# pod-security.yaml
apiVersion: v1
kind: Pod
metadata:
  name: security-context-demo
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: sec-ctx-demo
    image: nginx
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop:
        - ALL
      readOnlyRootFilesystem: true
      privileged: false
Pod Security Policies:

yaml
# psp-restrictive.yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  supplementalGroups:
    rule: 'MustRunAs'
    ranges:
      - min: 1
        max: 65535
  fsGroup:
    rule: 'MustRunAs'
    ranges:
      - min: 1
        max: 65535
  readOnlyRootFilesystem: false
Compliance Standards
📋 CIS Benchmarks Implementation
CIS Ubuntu 20.04 Hardening:

bash
# 1.1.1.1 Ensure mounting of cramfs filesystems is disabled
echo "install cramfs /bin/true" >> /etc/modprobe.d/cramfs.conf

# 1.1.1.2 Ensure mounting of freevxfs filesystems is disabled
echo "install freevxfs /bin/true" >> /etc/modprobe.d/freevxfs.conf

# 1.1.1.3 Ensure mounting of jffs2 filesystems is disabled
echo "install jffs2 /bin/true" >> /etc/modprobe.d/jffs2.conf

# 2.2.1.1 Ensure time synchronization is in use
apt-get install chrony
systemctl enable chrony

# 5.1.1 Ensure cron daemon is enabled
systemctl enable cron

# 5.2.1 Ensure permissions on /etc/ssh/sshd_config are configured
chown root:root /etc/ssh/sshd_config
chmod 600 /etc/ssh/sshd_config
Automated CIS Compliance Check:

bash
#!/bin/bash
# cis_compliance_check.sh

echo "=== CIS Compliance Check ==="
echo

# Check 1: Filesystem configuration
echo "1. Filesystem Configuration:"
if grep -q "/tmp.*noexec,nosuid,nodev" /etc/fstab; then
    echo "  ✓ /tmp mounted with noexec,nosuid,nodev"
else
    echo "  ✗ /tmp not properly mounted"
fi

# Check 2: SSH configuration
echo "2. SSH Configuration:"
if grep -q "^PermitRootLogin no" /etc/ssh/sshd_config; then
    echo "  ✓ Root login disabled"
else
    echo "  ✗ Root login enabled"
fi

# Check 3: Password policy
echo "3. Password Policy:"
if grep -q "minlen = 14" /etc/security/pwquality.conf; then
    echo "  ✓ Minimum password length 14"
else
    echo "  ✗ Password length insufficient"
fi

echo
echo "=== End of Compliance Check ==="
📊 Security Compliance Frameworks
ISO 27001 Controls Mapping:

bash
# A.9.2.1 User registration and de-registration
# Script to manage user lifecycle
#!/bin/bash
# user_lifecycle.sh

# Add user with proper security controls
add_user() {
    local username=$1
    local fullname=$2
    
    # Create user with secure defaults
    useradd -m -c "$fullname" -s /bin/bash "$username"
    
    # Set password policy
    chage -m 1 -M 90 -W 7 -I 30 "$username"
    
    # Add to appropriate groups
    usermod -aG users "$username"
    
    echo "User $username created with security controls"
}

# Deactivate inactive users
deactivate_inactive() {
    local days_inactive=90
    
    # Find inactive users
    inactive_users=$(lastlog -b $days_inactive | awk 'NR>1 {print $1}')
    
    for user in $inactive_users; do
        usermod -L "$user"
        chage -E0 "$user"
        echo "Deactivated inactive user: $user"
    done
}
NIST 800-53 Implementation:

bash
# AC-2 Account Management
# Automated account review script
#!/bin/bash
# account_review.sh

REPORT_FILE="/var/log/account_review_$(date +%Y%m%d).log"

{
    echo "=== Account Review Report - $(date) ==="
    echo
    
    # Check for accounts without password aging
    echo "1. Accounts without password aging:"
    awk -F: '$5 > 90 || $5 == "" {print $1}' /etc/shadow
    
    # Check for dormant accounts
    echo "2. Dormant accounts (no login in 90 days):"
    lastlog -b 90 | awk 'NR>1 {print $1}'
    
    # Check for unauthorized sudo access
    echo "3. Users with sudo access:"
    grep -Po '^[^#].*?(?=:)' /etc/sudoers /etc/sudoers.d/* 2>/dev/null
    
    # Check for shared accounts
    echo "4. Shared accounts (multiple concurrent logins):"
    who | awk '{print $1}' | sort | uniq -c | sort -nr
    
} > "$REPORT_FILE"
Quick Reference Cheatsheet
⚡ One-Minute Security Commands
Immediate Security Actions:

bash
# Lock down system quickly
sudo iptables -P INPUT DROP && sudo iptables -P FORWARD DROP
sudo fail2ban-client set sshd banip $(grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq)
sudo chmod 600 /etc/shadow /etc/gshadow
sudo chmod 644 /etc/passwd /etc/group
Quick Security Assessment:

bash
# 30-second security check
echo "Users with shell:" && grep -E ":/bin/(bash|sh|zsh)" /etc/passwd | cut -d: -f1
echo "Open ports:" && ss -tulpn | grep LISTEN
echo "SUID files:" && find / -perm -4000 -type f 2>/dev/null | wc -l
echo "Failed logins last hour:" && grep "$(date +'%b %e %H:')" /var/log/auth.log | grep "Failed password" | wc -l
🚨 Emergency Response
Incident Response Checklist:

bash
#!/bin/bash
# incident_response.sh

echo "=== Incident Response Started ==="
echo "Time: $(date)"
echo

# 1. Preserve volatile data
echo "1. Collecting volatile data..."
mkdir -p /tmp/ir-$(date +%s)
ps aux > /tmp/ir/processes.txt
netstat -tulpn > /tmp/ir/network.txt
last > /tmp/ir/logins.txt

# 2. Isolate system
echo "2. Isolating system..."
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP

# 3. Notify
echo "3. Sending notification..."
echo "Security incident detected on $(hostname) at $(date)" | mail -s "SECURITY INCIDENT" security-team@company.com

# 4. Begin investigation
echo "4. Starting investigation..."
grep -i "fail\|error\|denied\|invalid" /var/log/auth.log | tail -100 > /tmp/ir/auth_errors.txt
find / -mmin -60 -type f 2>/dev/null > /tmp/ir/recent_files.txt

echo "Incident response data saved to /tmp/ir/"
📝 Daily Security Maintenance
Daily Security Tasks:

bash
#!/bin/bash
# daily_security_tasks.sh

# 1. Check for updates
apt-get update
apt-get upgrade --dry-run

# 2. Review logs
tail -100 /var/log/auth.log | grep -i "fail\|invalid\|user"

# 3. Check for rootkits
rkhunter --check --sk

# 4. Review user accounts
awk -F: '$3 == 0 {print $1}' /etc/passwd

# 5. Check disk space
df -h | grep -E "(9[0-9]|100)%"

# 6. Review cron jobs
ls -la /etc/cron* /var/spool/cron/

# 7. Check for world-writable files
find / -xdev -type f -perm -0002 2>/dev/null

# 8. Review network connections
netstat -tulpn | grep -v "127.0.0.1"

echo "Daily security check completed at $(date)"
📚 Additional Resources
Recommended Tools
Lynis: Security auditing tool

Fail2ban: Intrusion prevention

AIDE: File integrity checker

RKHunter: Rootkit scanner

ClamAV: Antivirus engine

Snort: Network intrusion detection

OSSEC: Host intrusion detection

Wazuh: Security monitoring platform

Learning Resources
Books:

"Linux Security Cookbook" by Daniel J. Barrett

"Practical Linux Security" by Yogesh Babar

Courses:

Linux Security Essentials (Coursera)

Red Hat Security: Linux in Physical, Virtual, and Cloud (edX)

Certifications:

CompTIA Linux+

Red Hat Certified Engineer (RHCE)

GIAC Certified UNIX Security Administrator (GCUX)

Community & Support
Forums: Linux Security StackExchange, Reddit r/linuxsecurity

Mailing Lists: Security-focused Linux distributions

Conferences: Linux Security Summit, Black Hat

This guide is continuously updated. Last revision: December 2024

Remember: Security is a process, not a product. Regular maintenance, monitoring, and updates are essential for maintaining a secure Linux system.

<div align="center">
🔐 Security is a journey, not a destination. Stay vigilant! 🔐

https://img.shields.io/badge/License-MIT-yellow.svg
https://img.shields.io/badge/Maintained%253F-yes-green.svg

</div>
