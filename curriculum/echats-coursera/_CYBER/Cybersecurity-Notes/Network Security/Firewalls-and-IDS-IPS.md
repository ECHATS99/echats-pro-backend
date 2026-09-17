
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