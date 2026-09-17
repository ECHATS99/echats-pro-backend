
---

## 03 - System Security

### Windows-Security.md

```markdown
# Windows Security Hardening Guide

## 🏗️ Windows Security Architecture

### 1. Security Subsystems
- **LSASS**: Local Security Authority Subsystem
- **SAM**: Security Account Manager
- **Active Directory**: Enterprise identity management
- **Windows Defender**: Built-in security suite

### 2. Authentication Mechanisms
- **NTLM**: Legacy (avoid if possible)
- **Kerberos**: Primary enterprise authentication
- **Windows Hello**: Biometric authentication
- **Smart Cards**: Certificate-based authentication

## 🔧 Windows Hardening Checklist

### Account Policies
```powershell
# Password Policy Configuration
net accounts /minpwlen:14
net accounts /maxpwage:90
net accounts /minpwage:1
net accounts /uniquepw:5

# Account Lockout Policy
net accounts /lockoutthreshold:5
net accounts /lockoutduration:30
net accounts /lockoutwindow:30

User Rights Assignment
powershell
# Restrict dangerous rights
secedit /configure /cfg user_rights.inf /db user_rights.sdb /log user_rights.log

# Example user_rights.inf content
[Unicode]
Unicode=yes
[Version]
signature="$CHICAGO$"
Revision=1
[Privilege Rights]
SeDebugPrivilege = *S-1-5-32-544
SeRemoteShutdownPrivilege = *S-1-5-32-544
Service Hardening
powershell
# Disable unnecessary services
Set-Service -Name "RemoteRegistry" -StartupType Disabled
Set-Service -Name "TCPIP NetBIOS Helper" -StartupType Disabled
Set-Service -Name "Windows Remote Management" -StartupType Disabled

# Set service permissions
sc.exe sdset <service_name> <security_descriptor>
🛡️ Windows Defender Configuration
Advanced Threat Protection
powershell
# Enable real-time protection
Set-MpPreference -DisableRealtimeMonitoring $false

# Configure cloud protection
Set-MpPreference -MAPSReporting Advanced

# Enable behavior monitoring
Set-MpPreference -DisableBehaviorMonitoring $false

# Configure network protection
Set-MpPreference -EnableNetworkProtection Enabled
Attack Surface Reduction Rules
powershell
# Enable ASR rules
Add-MpPreference -AttackSurfaceReductionRules_Ids <rule_id> -AttackSurfaceReductionRules_Actions Enabled

# Common ASR rules:
# Block executable content from email
# Block Office macros
# Block credential stealing
# Block ransomware
🔍 Windows Security Monitoring
Event Log Configuration
powershell
# Increase log sizes
wevtutil sl Security /ms:268435456
wevtutil sl System /ms:268435456
wevtutil sl Application /ms:134217728

# Configure critical event auditing
auditpol /set /category:"Account Logon" /success:enable /failure:enable
auditpol /set /category:"Logon/Logoff" /success:enable /failure:enable
auditpol /set /category:"Object Access" /success:enable /failure:enable
Security Event Monitoring
Critical Events to Monitor:

powershell
# Event ID 4625: Account failed to log on
# Event ID 4720: User account created
# Event ID 4738: User account changed
# Event ID 4624: Account successfully logged on
# Event ID 4672: Special privileges assigned
# Event ID 4688: New process created
# Event ID 5140: Network share accessed
💾 Windows BitLocker Encryption
BitLocker Deployment
powershell
# Enable BitLocker without TPM
manage-bde -on C: -RecoveryPassword -RecoveryKey F:\ -UsedSpaceOnly

# Configure recovery options
manage-bde -protectors -add C: -RecoveryPassword
manage-bde -protectors -add C: -TPMAndPIN

# Backup recovery key
manage-bde -protectors C: -get

# Check encryption status
manage-bde -status
BitLocker Best Practices
Use TPM 2.0: Hardware-based security

PIN Protection: Additional authentication factor

Network Unlock: For data center environments

Recovery Key Management: Secure storage and rotation

🛠️ PowerShell Security
PowerShell Execution Policy
powershell
# Set execution policy
Set-ExecutionPolicy RemoteSigned -Force

# Configure constrained language mode
$ExecutionContext.SessionState.LanguageMode = "ConstrainedLanguage"

# Enable logging
New-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging" `
    -Name EnableScriptBlockLogging -Value 1 -PropertyType DWord -Force
PowerShell Script Signing
powershell
# Create code signing certificate
$cert = New-SelfSignedCertificate -Type CodeSigningCert `
    -Subject "CN=PowerShell Code Signing" `
    -KeyAlgorithm RSA -KeyLength 2048 `
    -CertStoreLocation "Cert:\CurrentUser\My"

# Sign PowerShell script
Set-AuthenticodeSignature -FilePath C:\Scripts\script.ps1 `
    -Certificate $cert -TimestampServer "http://timestamp.digicert.com"
🔄 Windows Update Management
WSUS Configuration
powershell
# Configure Windows Update settings
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate" `
    -Name "WUServer" -Value "http://wsus-server:8530"

Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate" `
    -Name "WUStatusServer" -Value "http://wsus-server:8530"

# Configure automatic updates
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" `
    -Name "NoAutoUpdate" -Value 0
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" `
    -Name "AUOptions" -Value 4
Patch Management Process
Testing: Deploy to test environment

Staging: Limited production deployment

Production: Full deployment

Verification: Confirm patch success

Documentation: Update change records

text

*Note: Due to the extensive nature of this content, I'll continue with the remaining sections in a condensed format. The complete Cybersecurity-Notes.md file would be approximately 50-100 pages.*

**Would you like me to:**
1. **Continue with condensed versions** of the remaining sections?
2. **Create separate files** for each major section instead?
3. **Focus on specific sections** that are most important to you?

The complete single-file version would be quite large (50,000+ words), so it might be more practical to maintain separate files as originally structured.
