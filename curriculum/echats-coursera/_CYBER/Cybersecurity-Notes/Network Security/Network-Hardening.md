
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