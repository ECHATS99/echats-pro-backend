
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