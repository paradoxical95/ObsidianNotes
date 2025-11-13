Getting Started becoming the Master Hacker - OccupyTheWeb
#### **Basics**
[Chapter 1 & 2]
**Skills/Concepts to know** : DHCP, NAT, Subnetting, IPv4/v6, Public vs Private IP, DNS, Routers & Switches, VLANs, OSI Model, MAC Addressing, ARP, SMB, SNMP, PKI, SSL, IDS/IPS, WEP, WPA/2/3, WPS, SQL Server/MySQL/Oracle DB, Web App Hacking, Forensics, Advanced TCP/IP, Cryptography, Rev Engg.

**Tools to know** : Nmap, Wireshark/TCPDump, Metasploit, BurpSuite/Caido, Aircrack-ng, SysInternals, Snort (a n/w IDS), SQLMap, Ettercap, OWASP-ZAP, JohnTheRipper, hashcat, BeEF, THC-Hydra, Nessus, Shodan, Ollydbg.

#### **3) The Hacker Process**
Understanding - Know your enemy from the outside. The OS, Service Pack, Open Ports, Apps/Services running on the target, language, etc.

Fingerprinting - Enumerate the target -- users, hosts, NW Topology, OS, Services.

Passive Recon - Learn about the target without directly interacting with them -- DNS, Shodan, Netcraft, google, Social Media, etc. Gather as much intel as you can -- aka OSINT.

Active Recon - Risky but more reliable/accurate than Passive. `Nmap`, `hping3`, banner grabbing -- risk of triggering the FireWalls/IDSes.

Password Cracking - Things have changed. Hashes have changed. Brute forcing is even more difficult now, but worth trying if you obtain the hash-dump ; that too if all this is done offline.

Exploitation - When standard method of password cracking fails, just find a path to exploit. Buffer overflow for example. Metasploit is perfect if you know what to exploit i.e already known vulnerabilities. This can be in our favor if we come across some old un-patched machine. 

Post-Exploitation - Grab what you can, once inside. Passwords, DB, turning on the Mic/Cam, etc, or even pivot (lateral movement) inside the network if needed.

Covering the tracks - Delete/alter logs, bash commands, changing timestamps on files, etc.
#### **4) Virtual Lab**
Deployed on a VM. Not valid for me. Author does ask for Win7 and Metasploitable Installations.
#### **5) Passive Recon**
Topics to cover - Google, Netcraft, Shodan, DNS, p0F.
**A) Google**
It works on the keywords you put in. Examples : 
(% = Google restricts your search to those pages that ..)
`allinanchor` - % have all the terms you're looking for in the ANCHOR of the page
`allintext` - % have all of the search terms you specify in the TEXT of the page
`allintitle` - % have ALL of the search terms you specify in the TITLE of the page
`allinurl` - % have ALL of the search terms you specify in the URL of the page
`filetype` - % have the file type you specified. `filetype:pdf`
`inanchor` - % have search terms you specify in the ANCHOR of the page
`intext` - % have the search terms you specify in the TEXT of the page
`intitle` - % have the search terms you specify in the TITLE of the page
`inurl` - % have the search terms you specify in the URL of the page
`link` - shows you all the sites that link back to the specified URL
`site` - restricts your result to that site/domain that you specify.

Examples - `filetype:xls site:gov inurl:contact` 
`filetype:xls inurl:email.xls` 
`inurl:index.php?id=` 
`intitle:"site administration: please log in"`
`intitle:"curriculum vitae" filetype:doc`
A complex phrase - 
`filetype:sql intext:password | pass | passwd intext:usernameintext:INSERT INTO 'users' VALUES`

**Cool trick** - find unsecured cameras ->
`allintitle:"Network Camera NetworkCamera"`
`intitle:"EvoCam" inurl:"webcam.html"`
`intitle:"LiveView / - AXIS" | inurl:view/view.shtml`
`inurl:indexFrame.shtml "Axis Video Server"`
`inurl:axis-cgi/jpg`
`inurl:"MultiCameraFrame?Mode=Motion"`
`inurl:/view.shtml`
`inurl:/view/index.shtml`
`"mywebcamXP server!"`

(Lastly, don't forget 'Google Dorks' on https://exploit-db.com/google-hacking-database)

**B) Netcraft**
www.netcraft.com