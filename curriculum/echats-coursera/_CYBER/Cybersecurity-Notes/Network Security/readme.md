
---

## 02 - Network Security

### Network-Protocols-Security.md

```markdown
# Network Protocols Security

## 🌐 Protocol Analysis by Layer

### Layer 2 - Data Link
**Protocols:**
- **ARP**: Address Resolution Protocol
  - Security Issues: ARP spoofing, poisoning
  - Mitigation: Static ARP, ARP inspection
- **MAC Address Security**
  - MAC flooding attacks
  - Port security controls

### Layer 3 - Network
**Protocols:**
- **IP Security**
  - IP spoofing protection
  - Unicast Reverse Path Forwarding (uRPF)
- **ICMP Security**
  - ICMP flood attacks
  - Rate limiting recommendations

### Layer 4 - Transport
**Protocols:**
- **TCP Security**
  - SYN flood attacks
  - TCP sequence prediction
  - TCP hardening guidelines
- **UDP Security**
  - UDP flood attacks
  - Reflection/amplification attacks

### Layer 7 - Application
**Protocols:**
- **DNS Security**
  - DNSSEC implementation
  - DNS cache poisoning
  - DNS tunneling detection
- **HTTP/HTTPS Security**
  - TLS best practices
  - HSTS implementation
  - Certificate management

## 🔒 Secure Protocol Configuration

### SSH Hardening
```bash
# /etc/ssh/sshd_config
Protocol 2
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AllowUsers specific_user
ClientAliveInterval 300
ClientAliveCountMax 2
MaxAuthTries 3

TLS Configuration
nginx
# Nginx SSL configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
ssl_prefer_server_ciphers on;
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_stapling on;
ssl_stapling_verify on;
🛡️ Protocol Attack Mitigations
Common Attacks & Defenses
Attack	Protocol	Mitigation
SYN Flood	TCP	SYN cookies, rate limiting
DNS Amplification	DNS	Rate limiting, response size limits
ARP Poisoning	ARP	Dynamic ARP inspection, static entries
SSL Stripping	HTTPS	HSTS, certificate pinning
DHCP Starvation	DHCP	Port security, DHCP snooping
🔧 Monitoring & Detection
Wireshark Filters for Security
bash
# Detect ARP poisoning
arp.duplicate-address-detected

# Find SYN scans
tcp.flags.syn==1 and tcp.flags.ack==0

# Detect DNS tunneling
dns.qry.name.len > 50

# Find suspicious HTTP traffic
http.request.method == "POST" and http.host contains "suspicious"


### Firewalls-and-IDS-IPS.md

```markdown
# Firewalls, IDS & IPS Systems

## 🛡️ Firewall Types & Architectures

### 1. Packet Filtering Firewalls
**Operation:** Examines packet headers
**Pros:** Fast, simple
**Cons:** No state tracking
**Use Case:** Basic perimeter protection

### 2. Stateful Inspection Firewalls
**Operation:** Tracks connection states
**Pros:** Context-aware decisions
**Cons:** More resource intensive
**Use Case:** Enterprise network boundaries

### 3. Application Firewalls (WAF)
**Operation:** Layer 7 inspection
**Pros:** Deep packet inspection
**Cons:** Performance impact
**Use Case:** Web application protection

### 4. Next-Generation Firewalls (NGFW)
**Features:**
- Deep packet inspection
- Application awareness
- Integrated IPS
- SSL inspection
- User identity integration

## 🔍 Intrusion Detection Systems (IDS)

### Types of IDS
1. **Network-based (NIDS)**
   - Monitors network traffic
   - Examples: Snort, Suricata
   - Deployment: Span ports, network taps

2. **Host-based (HIDS)**
   - Monitors host activities
   - Examples: OSSEC, Wazuh
   - Deployment: Agents on endpoints

3. **Signature-based**
   - Matches known attack patterns
   - Low false positives
   - Cannot detect zero-days

4. **Anomaly-based**
   - Learns normal behavior
   - Detects deviations
   - Higher false positives

## ⚡ Intrusion Prevention Systems (IPS)

### IPS Operation Modes
1. **Inline Mode**
   - Blocks malicious traffic
   - Can cause service disruption
   - Requires careful tuning

2. **Passive Mode**
   - Alerts only (like IDS)
   - No service disruption
   - Limited protection

### IPS Deployment Strategies
```yaml
network_security:
  perimeter:
    - NGFW with IPS at internet edge
  internal:
    - Network segmentation with firewalls
    - Internal traffic inspection
  endpoints:
    - Host-based IPS on critical servers

    🔧 Configuration Examples
iptables Firewall Rules
bash
# Basic firewall rules
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH (port 22)
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Log dropped packets
iptables -A INPUT -j LOG --log-prefix "IPTABLES DROP: "
Snort IDS Rules
bash
# Alert on SQL injection attempts
alert tcp $EXTERNAL_NET any -> $HOME_NET $HTTP_PORTS \
(msg:"SQL Injection Attempt"; flow:to_server,established; \
content:"union"; nocase; content:"select"; nocase; \
pcre:"/union\s+select/i"; classtype:web-application-attack; sid:1000001;)

# Detect Nmap scans
alert tcp $EXTERNAL_NET any -> $HOME_NET any \
(msg:"Nmap Scan Detected"; flags:S,12; \
threshold:type threshold, track by_src, count 5, seconds 60; \
classtype:attempted-recon; sid:1000002;)
📊 Monitoring & Tuning
IDS/IPS Tuning Process
Initial Deployment: Detection-only mode

Baseline Establishment: 1-2 weeks of monitoring

False Positive Reduction: Adjust rules, thresholds

Optimization: Fine-tune performance settings

Prevention Enablement: Switch to blocking mode

Key Performance Metrics
Throughput: Packets per second

Detection Rate: True positives

False Positive Rate: Should be < 5%

Latency: Processing delay

Resource Utilization: CPU, memory usage


### Network-Hardening.md

```markdown
# Network Hardening Guide

## 🏗️ Network Architecture Security

### 1. Network Segmentation
**Principles:**
- **Zero Trust**: No implicit trust between segments
- **Least Privilege**: Minimum necessary access
- **Defense in Depth**: Multiple security layers

**Segmentation Models:**
```yaml
network_zones:
  untrusted:
    - Internet-facing systems
    - DMZ networks
    
  semi-trusted:
    - User workstations
    - General servers
    
  trusted:
    - Domain controllers
    - Database servers
    
  restricted:
    - Payment systems
    - Critical infrastructure

    2. VLAN Security
Best Practices:

Separate management VLAN

Isolate guest networks

Implement VLAN access controls

Disable unused VLANs

Configuration Example:

cisco
! VLAN Configuration
vlan 10
 name Management
vlan 20
 name Servers
vlan 30
 name Users
vlan 99
 name Guest

! Trunk Configuration
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,30
🔧 Device Hardening
Router/Switch Hardening Checklist
Physical Security

Secure console access

Rack security

Camera surveillance

Access Controls

Strong passwords

AAA authentication

Role-based access control (RBAC)

Service Hardening

Disable unused services

Secure management protocols

Logging and monitoring

Cisco Device Example
cisco
! Basic hardening template
service password-encryption
no ip http server
no ip http secure-server
no cdp run
no ip source-route
ip ssh version 2
ip ssh time-out 60
ip ssh authentication-retries 3

! AAA Configuration
aaa new-model
aaa authentication login default local
aaa authorization exec default local
🛡️ Wireless Network Security
WPA3 Implementation
Features:

Simultaneous Authentication of Equals (SAE)

192-bit security suite

Enhanced public key cryptography

Configuration:

bash
# hostapd configuration for WPA3
interface=wlan0
driver=nl80211
ssid=SecureNetwork
hw_mode=g
channel=6

# WPA3 Configuration
wpa=2
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
ieee80211w=2
sae_require_mfp=1
Wireless Security Best Practices
Hide SSID: Limited security value

MAC Filtering: Easily bypassed

Strong Encryption: WPA3 or WPA2 with AES

Regular Updates: Firmware patches

Rogue AP Detection: Monitor for unauthorized devices

📡 Network Monitoring & Detection
Network Traffic Analysis
Tools:

Wireshark: Deep packet inspection

tcpdump: Command-line packet capture

Zeek (Bro): Network security monitor

Suricata: IDS/IPS with network monitoring

Monitoring Script:

bash
#!/bin/bash
# Network monitoring script

# Monitor for suspicious traffic
tcpdump -i eth0 -n 'tcp[13] & 2 != 0' | grep -E '(SYN|ACK)' | head -20

# Check for ARP poisoning
arp -a | sort | uniq -d

# Monitor bandwidth usage
iftop -i eth0 -n

# Check for port scans
netstat -an | grep SYN_RECV | wc -l
Security Information and Event Management (SIEM)
Network-focused Rules:

yaml
detection_rules:
  - name: Multiple Failed SSH Attempts
    query: >
      event.category:authentication AND 
      event.action:"failed" AND 
      destination.port:22
    threshold:
      count: 5
      timeframe: 5m
      
  - name: Port Scan Detection
    query: >
      source.ip: * AND 
      destination.port: [*] AND 
      event.type:"connection" AND 
      network.transport:tcp
    threshold:
      unique_destination_ports: 100
      timeframe: 1m
🔄 Continuous Hardening Process
Hardening Assessment Checklist
markdown
## Quarterly Network Assessment

### Physical Security
- [ ] Rack access logs reviewed
- [ ] Camera footage retention verified
- [ ] Environmental controls tested

### Device Configuration
- [ ] Firmware updates applied
- [ ] Configuration backups verified
- [ ] Unused services disabled

### Access Controls
- [ ] Password policies enforced
- [ ] User access reviews completed
- [ ] Administrative accounts audited

### Monitoring
- [ ] Log collection functional
- [ ] Alert thresholds adjusted
- [ ] Incident response tested
Patch Management Schedule
Device Type	Patch Window	Testing Required	Rollback Plan
Core Routers	Monthly	Yes	Configuration backup
Switches	Quarterly	Yes	Staged rollout
Wireless APs	As needed	Yes	Firmware backup
Firewalls	Monthly	Yes	Rule backup


### VPN-Technologies.md

```markdown
# VPN Technologies & Security

## 🔐 VPN Types & Protocols

### 1. Site-to-Site VPN
**Purpose:** Connect entire networks
**Protocols:** IPsec, GRE
**Use Cases:** Branch office connectivity, cloud integration

### 2. Remote Access VPN
**Purpose:** Connect individual users
**Protocols:** SSL/TLS, IPsec, WireGuard
**Use Cases:** Remote work, mobile access

### 3. SSL/TLS VPN
**Characteristics:**
- Operates at Layer 4/5
- Uses standard HTTPS port (443)
- Clientless options available
- Examples: OpenVPN, AnyConnect

### 4. IPsec VPN
**Components:**
- **IKE** (Internet Key Exchange): Key management
- **ESP** (Encapsulating Security Payload): Data encryption
- **AH** (Authentication Header): Data integrity

## 🚀 Modern VPN Protocols

### WireGuard
**Advantages:**
- Modern cryptography (ChaCha20, Curve25519)
- Simple configuration
- High performance
- Built into Linux kernel

**Configuration Example:**
```ini
# /etc/wireguard/wg0.conf
[Interface]
Address = 10.0.0.1/24
PrivateKey = [Server Private Key]
ListenPort = 51820

[Peer]
PublicKey = [Client Public Key]
AllowedIPs = 10.0.0.2/32

OpenVPN
Features:

SSL/TLS based

Cross-platform support

Extensive configuration options

Community and commercial support

🔒 VPN Security Considerations
Encryption Standards
Protocol	Encryption	Authentication	Key Exchange
IPsec	AES-256	HMAC-SHA256	Diffie-Hellman
OpenVPN	AES-256-GCM	TLS	ECDH
WireGuard	ChaCha20	Poly1305	Curve25519
Security Best Practices
Strong Authentication

Multi-factor authentication

Certificate-based authentication

Token-based systems

Perfect Forward Secrecy

Ephemeral key exchange

Prevents compromise of past sessions

Network Segmentation

Isolate VPN traffic

Apply access controls

Monitor VPN-specific networks

🛠️ Implementation Guides
OpenVPN Server Setup
bash
# Generate certificates
easyrsa init-pki
easyrsa build-ca
easyrsa gen-req server nopass
easyrsa sign-req server server
easyrsa gen-dh

# Server configuration
port 1194
proto udp
dev tun
ca ca.crt
cert server.crt
key server.key
dh dh.pem
server 10.8.0.0 255.255.255.0
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 8.8.8.8"
keepalive 10 120
cipher AES-256-CBC
auth SHA256
VPN Security Monitoring
bash
# Monitor VPN connections
sudo wg show
sudo openvpn-status.log

# Check for unusual activity
grep "Failed password" /var/log/auth.log
netstat -tulpn | grep :1194

# Bandwidth monitoring
vnstat -l -i tun0
📊 VPN Performance Optimization
Tuning Parameters
MTU Size: Adjust for overhead (usually 1400-1500)

Compression: Use only if needed (lzo, lz4)

Cipher Selection: AES-GCM vs AES-CBC

Keepalive Settings: Balance between detection and overhead

Troubleshooting Common Issues
Issue	Possible Causes	Solutions
Slow Speeds	MTU issues, encryption overhead	Adjust MTU, change cipher
Connection Drops	Network instability, keepalive	Adjust keepalive, use TCP
Authentication Failures	Certificate issues, clock skew	Verify certificates, sync time
Routing Problems	Split tunneling misconfiguration	Check routing tables, DNS
