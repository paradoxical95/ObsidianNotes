##### **Windows Fundamentals**
`msconfig` - Systems Config Util - handles General (startup), Boot, Services, Startup (now handled by `taskmgr`) & Tools (to launch some specific service).

`control.exe` opens the control panel.

`UserAccountControlSettings.exe` is the UAC manager.

Some apps that are attached to ControlPanel may have a different extension. Example : `wscui.cpl` -> which opens up the Security & Maintenance section of ControlPanel.

Other things, can be attributed as `.msc` - which are the services running via Management console. One such service - `compmgmt.msc` -- which can handle a lot of tasks and contains a lot of services/link to them. `Win+R>compmgmt.msc` or `Win+X>Comp Management`
`compmgmt.msc` can make tasks + bind them. It also contains `lusrmgr.msc` and even `perfmon`
WMI and WMI-CLI (Windows Mgmt Instrumentation) was deprecated and superseded by Powershell.
`msinfo32.exe` is capable of gathering all HW info along with SW Components. 
There's also `resmon.exe` - Resource Manager which taskmgr but on steroids. 
`regedit.exe` - reg editor

CMD Commands : `hostname`, `whomai`, `ipconfig`, `/?` (used as 'man' command in linux, although some commands would want `'help'` instead), `cls`, `netstat`, `net` (manage n/w resources) [net is used for user-management as well]
VSS or Volume Shadow Copy Service handles the restore point and all.

##### **Active Directory Basics** 
**Windows Domain** is a group of users & computers under the administration of some business. The centralised repo of all those machines is called **Active Directory** & the server that runs this AD is called **Domain Controller** (DC).
This way, you can centralise ID mgmt and have a unified method of managing security policies.
Examples - the university/school network that gave you one user ID/pw and you can login on any machine and still have your stuff synced + restrictions (like control panel) still in place.
DS is domain service i.e the catalogue storing info about who all are in the AD (users, groups, PC, printers, etc.)
**Users :** also called *'Security Principals'*, they basically can act upon the resources on the network. People (humans) and Services (IIS or MySQL) both fall under this. 
**Machines :** also considered Security Principals, but they are an object created for any and every computer that joins the network. They do have an account this way but very limited. No one else is supposed to log in to one machine's account but ofc they can. Naming scheme is simple. It uses the computer's name followed by a $ -> `AdminPC` would have a machine name as `AdminPC$`.
**Security Groups :** Basically like User Groups - having rights to file/folders with respective permissions. Also 'Security Principals'. 
Examples of some domains present in a group ->
Domain Admins - admin priv over the entire domain. Can administer anything.
Server Ops - Can administer DC but cannot change any admin group memberships.
Backup Ops - To perform data backups on computers. Can ignore any file permissions.
Account Ops - Create/modify other users in the domain.
Domain Users - All existing user accounts in the domain.
Domain Computers - All existing computers in the domain.
Domain Controllers - All DCs on the domain

Windows already has the "Active Directory Users & Computers" tool to handle all this. In this we have Organizational Units (OU) which are just container objects that allow us to classify users & machines. 1 User can only be in 1 OU, and each OU can have totally difft+separate permissions (Sales, IT, Marketing, etc).
Ofc there are default containers too (BuiltIn, Computers, DC, Users, Managed Service Accounts).
Basically, quoting THM directly :
- **OUs** are handy for **applying policies** to users and computers, which include specific configurations that pertain to sets of users depending on their particular role in the enterprise. Remember, a user can only be a member of a single OU at a time, as it wouldn't make sense to try to apply two different sets of policies to a single user.
- **Security Groups**, on the other hand, are used to **grant permissions over resources**. For example, you will use groups if you want to allow some users to access a shared folder or network printer. A user can be a part of many groups, which is needed to grant access to multiple resources.

***Managing users in AD***
Deleting OUs or Users :
By default, OUs are protected against accidental deletion. To fix this, enable Advanced Features in the view menu, then Rt-click the OU you want to delete > properties > object & un-check the "Protect object from accidental deletion"

Delegation :
Allowing some users have control over some OUs is delegation. Example : IT being given the priv to reset other low-level user's passwords. For this, Rt-click on the OU you want to hand over the control of, then fill in the user name of that person (IT guy in our case) followed by the tasks selection for delegation.
In such cases, we can RDP to this IT member who can run a powershell script to remotely change the password of any of the users and optionally prompt a password reset on logon.
`PS > Set-ADAccountPassword sophie -Reset -NewPassword (Read-Host -AsSecureString 'New Password')`

***Managing computers in AD***
By default, all machines that join a domain (except for the DCs) will be put in the container called "Computers". The entries might have their own naming convention like 'LPT-SOPHIE' or 'PC-MARK'.

***Group Policies***
The main idea of organizing users and computers into separate OUs is to have customized Group Policies for each of them. Situated inside the "Group Policy Management" tool, we have the GPO or Group Policy Objects -- they simply are the collection of settings that can be applied to OUs. They can be used to apply settings/rules to computers.
(Policies are created under the GPO section but linked in the general section). Examples like Default Domain Policy or RDP Policy, etc.
GPOs are distributed to the network via a network share called `SYSVOL`, which is stored in the DC. All users in a domain should typically have access to this share over the network to sync their GPOs periodically. The SYSVOL share points by default to the `C:\Windows\SYSVOL\sysvol\` directory on each of the DCs in our network.

***Authentication Methods***
On Windows domains, credentials are stored with the DC -- as these are now Domain Credentials -- so the service talks to the DC for auth via any of the 2 protocols :

**Kerberos** -> default protocol in any recent domain + used by recent versions of Windows.
Standard behavior is to assign tickets at log in -- tickets act as a proof of prev auth. 
Basically it involves the username + timestamp in the requst, encrypted with a key. The Key Distribution Center (KDC) will send back to the usrer, a TGT - ticket granting ticket - and a session key. Then the client, while connecting to a service, asks for a TGS - ticket granting service, which are service specific - which is done when the user sends their username+timestamp encrypted using the Session key + send the TGT and SPN (service principal name). In return, the KDC sends us a TGS along with a service session key in the response. Now the user re-encrypts the TGS with service-owner hash and finally connects to the service

**NetNTLM** - legacy, mainly for compatibility. Client sends an auth req -> server generates a random number & sends it as a challenge to the client -> Client then combines NTLM password hash with the challenge to generate a resp to the challenge & sends it back to the server for verification. The server forwards the challenge & the response to the DC for verification. The DC uses the challenge to recalculate the response and compares it to the original response sent by the client. If they both match, client is auth-cated & server forwards the auth result to the client.

***Trees, Forests & Trusts***
**Tree** can be formed with a sub-domain like AD network. Example : `thm.local` is our main AD network, and `uk.thm.local` and `eu.thm.local` will be the sub-domains. 
**Forest** is when 2 or more trees are union-ized as one big network. So all trees will be filled with their respective sub-domains in it.
For this, a new security group is introduced - **Enterprise Admins**.
**Trust Relationships** are required when different trees need to access files stored on each other. Example : UK THM needs to access something in MHT Asia or EU. So we need a one-way trust relationship. Trust is one direction, access is the other. Two way is also possible. Does not mean everyone is now family, you still need per-user auth. 

##### **Bash Basics**
(Most is covered elsewhere)
In bash, you can debug by writing `set +` and `set -` inside your code making a block, then on the terminal run `$ > bash +x ./script.sh`. This will show a '+' for the lines that worked perfectly and '-' for the ones that failed.
`$1`, `$2` etc are all parameters that can be sent when calling the script. Inside the script they can be used like normal variables. Input is still handled by `read`. However, `$0` is used to fetch the script name itself i.e 0 parameter.
`$#` is used to get the number of args supplied while calling the script.
**_Arrays_**
`transport=('car' 'train' 'bike' 'bus')`
To use : `echo "${transport[@]}"`  -- @ is for all elements, can be replaced by numeric digits.
To unset/delete an element -- `use unset transport[1]`. 
To set any element to something else, the same syntax follows -- `transport[1]='truck'`
**_Conditionals_**
`if [condition compare condition]`
`then`
  `body_of_if`
`else`
  `body_of_else`
`fi`
Conditionals like `-eq , -ne , -gt , -lt , -ge`
Example code :
`#! /bin/bash`
`filename=$1`
`if [ -f  "$filename" ] && [ -w  "$filename" ]`
`then`
  `echo "hello" > "$filename"`
`else`
  `touch "$filename"`
  `echo "hello" > "$filename"`
`fi`
//Here, `-f` checks if the file exists & `-w` checks if its writable. `-r` for readable and `-d` to see if it's a directory. 

(Part of Network Fundamentals Module)
##### **LAN Basics**
*Subnetting* :
We know, IP Addrs are split into 4 octets, ranging from 0-255. Subnet is just a sub-category, also ranging from 0-255, 4 bytes(32 bits). Subnets use IP Addr in 3 different ways -> ID the network addr, ID the host addr & ID the default gateway.
Examples ->
N/W Addr - Identifies the actual start of the N/W and its existence. Device with 192.168.1.100 will be on the N/w identified by 192.168.1.0
Host Addr - Used to identify a device on the subnet. A device will have the N/W Addr of 192.168.1.1
Default Gateway - A special addr assigned to a device on the N/W that is capable of sending info to another network. Any data that needs to go to a device that isn't on the same network (168.1.0) will be sent to this device. These devices can use any host addr but usually use either the first or the last addr in the network (.1 or .254)

ARP is the link b/w the MAC Addr & IP Addr of any device on the network. ARP Req (packet) is sent -- a message is broadcasted on the N/w asking the MAC of the IP in question. Only the valid party is allowed to respond via the ARP Reply (packet).

DHCP is responsible for assigning the IP Addresses. When not manually assigned, a new device sends out a `DHCP Discover` req to get any DHCP servers on the N/w. DHCP Server then replies back with an IP Addr via the `DHCP Offer` reply. Then device gets it, sends back a confirmation via `DHCP Request` to the server. Lastly, the DHCP server sends the reply acknowledging via `DHCP ACK`. Device only sends 2 messages - Discover & Request. Server has the other 2, OFFER & ACK.

##### **OSI Model**
Open Systems Interconnection. 
7 Layers. From 7 to 1 -> **Application, Presentation, Session, Transport, Network, Data Link & Physical**. In OSI, devices can have different functions & designs on a network while communicating with other devices. This model provides a framework dictating how all networked devices will send, receive & interpret data. Encapsulation - pieces of info get added to data. 
Observing all layers ->
1. Physical : Ethernet cables for example. 
2. Data Link : focuses on physical addressing of the transmission. It receives a packet from the network layer (including the IP) and adds the MAC addr of the receiving endpoint. NIC handles this MAC thing. Remember, MAC cannot be changed but can be spoofed. This layer presents the data in a suitable format for transmission.
3. Network : Routing & re-assembly of data. Optimal path via OSPF (Optimal shortest path first) & RIP (routing info protocol) -- shortest (least devices to hop), reliable (minimal packet loss) & faster physical connection (fibre vs copper). Everything is dealt via IP Addrs & devices here (router etc) are called Layer-3 devices.
4. Transport : Actual transmission. Methods - always 2 there are - TCP & UDP. 
	A. TCP -> Reserves  a constant connection b/w the 2 devices for the amount of time it takes for data to be sent & received + incorporates error checking (helps session layer). It guarantees the accuracy of data but requires a reliable connection b/w the 2 devices (a small chunk missing can render the entire chunk useless). It can handle device-sync to prevent flooding, but any slow connection will bottleneck the other device as the connection will be reserved on the receiving end. Slower than UDP bcz devices work a lot harder here. USE CASES : file sharing, browsing, email. 
	B. UDP -> Not as advanced as TCP. It doesn't care if the data is received. Leaves the Application Layer (user end) to decide if there's any control over how quickly the packets are sent. It is flexible to SDEs. Does not reserve a continuous connection on a device as TCP. Unstable connection here results in a terrible experience for the user. USE CASES : ARP, DHCP, small pieces of data being sent, large video streaming.
5. Session : When data is formatted/translated from Layer-6, Layer-5 i.e Session layer will begin to create & maintain the connection to the computer for which the data is destined. Connection established -> session created. This layer is also responsible for closing the connection on a timeout or error. Can also create checkpoints -- saves bandwidth. Unique in nature -- data cannot travel over different sessions.
6. Presentation : The translator. Here, standardization takes place. Back-and-forth with Layer-7. Example - email client varies but we still get the same thing, thanks to Presentation layer. HTTPS occurs at this layer. 
7. Application : User-facing. Here, protocols & rules are in place to determine how the user should interact with data sent/received. USE CASES : Everything like email clients, browsers, file browing (FileZilla), DNS, etc.
Order -> Phy-DL-NW-TR-SS-PRS-APP (Physical-D-NTS-PA)

##### **Packets & Frames**
###### *What are they?*
Both are small pieces of data. ==Packet== is under layer-3 i.e Network -- containing IP header & payload. ==Frame== is under layer-2 i.e Data Link -- encapsulates the packet & adds additional info such as the MAC Addr.
Analogy - Mailing a letter through post. Envelope is the frame, here used to move the letter i.e packet. Once the recipient opens the envelope, the can see the letter itself. This process is called 'encapsulation'.
Packets are efficient at communication across networked devices. Small pieces hence less chance of bottle-necking. Eg : Loading an image, instead of the whole image, small pieces are sent and then reconstructed on your local machine. The structure of a packet may vary depending upon the type.
Some notable headers ->
`Time to live` : lifespan/expiry timer of the packet
`Checksum` : integrity checking for TCP/IP. Notifies of tampering.
`Source Addr` : IP of where it was sent from, so that data knows where to return to.
`Dest Addr` : IP of where it's being sent to, so that data knows where to travel next.

###### *TCP/IP (3-way handshake)*
TCP/IP consists of 4 layers of its own-> Application, Transport, Internet & Network Interface.
(A.T.I.Ni). TCP uses these 4 layers to ensure that data is received at destination. TCP is connection-based -- i.e a connection needs to be established first. Each layer embeds some info in the packet.
A TCP packet has various sections called headers :
`Source Port (0-65535)` , `Destination Port`, `Source IP`, `Destination IP`, `Sequence Number` (every piece is given a random number), `Ack Number` (Seq No. + 1), `Checksum` (integrity hash), `Data` (where are the bytes stored), `Flag` (behavior - how it should be handled).
TCP has this special 3-way handshake. In total we have 6 messages ->
`SYN` - initial packet sent by the client. Used to initiate the connection + sync the devices.
`SYN/ACK` - receiving device sends it to acknowledge sync attempt.
`ACK` - can be used by either party to ack that a series of messages/packets have been rec'd.
`DATA` - actual bytes of data sent via this message
`FIN` - cleanly close the connection after completion
`RST` - abruptly ends all communications -- last resort & indicates a problem.

Process : 2 Devices A & B -> A sends `SYN` to B, B sends `SYN/ACK` back to A and then A sends `ACK` to B. Any sent data is given a Random Number seq & is reconstructed using this number sequence. Both devices must agree with the same number sequence for the data to be sent in the correct order. The order is agreed upon in the above 3 steps of the handshake. Basically,
`SYN` - Client : Here is my initial seq number (INS) to SYNchronise with (0)
`SYN/ACK` - Server : here's my INS to SNYchronise with (5000) & I ACKnowledge your INS (0)
`ACK` - Client : I ACKnowledge your INS (5000), here is some data which is INS+1 (0+1)
//This way, Client INS is going 0,1,2,3... and FNS will be 1,2,3...

Closing a connection ->
TCP closes the connection when the rec'r says it has rec'd all the data. TCP inherently reserves system resources, so closing it ASAP is best. To initiate the closure, device will send a "FIN" packet. Here, 
A sends a `FIN` packet to B, then B sends `FIN` & `ACK` packets, then A replies with `ACK` and then the connection is closed.
###### *UDP/IP*
UDP is state-less protocol (no ACK system) + no need for a constant connection. No 3-way handshake. UDP can tolerate data loss + does  not reserve a continuous connection on a device as TCP -- hence no safeguards such as data integrity. 
*UDP Headers :* `TTL` (time to live), `Source IP`, `Dest IP`, `Source Port`, `Dest Port`, `Data`.
It feels one sided. Request sent from B to A and then A keeps on sending Response.

**Ports**
Ports are the point of exchange. Very specific. Like harbour, ships & ports. Ships line up and connect to a port at the harbour. A cruiser liner cannot dock at a port made for  a fishing vessel & vice versa. Compatibility is defined by the ports. It if ain't compatible it can't park here. Ranging from 0 to 65535 but few apps have a fixed port.
`FTP - 21`, `SSH - 22`, `HTTP - 80`, `HTTPS - 443`, `SMB - 445`, `RDP - 3389`, etc.
Eg : `$ > nc  8.8.8.8   443`

##### **Extending your Network**
*Port Forwarding*
Configured at the router level, it is the most crucial step. Without it, everything is limited to its own network i.e Intranet. Example - a webserver running something on `Port 80` inside a network having `192.168.1.10` will not be public by default. For that it needs an IP ofc but also the services being port forwarded via that IP. So now this server will have a Public IP of `82.62.51.70`.

*Firewall*
Responsible for what traffic is allowed to enter/exit. Like border security. Can be configured by admin to permit/deny any traffic. It performs packet inspection to ask these questions -> `Coming from where? ; 
`Going to where? ;
`For which port? ; 
& `What protocol is being used by this traffic?.`
Operates at Layer 3 & 4 i.e Network & Transport layer. 
2 Types - Hardware (Fortinet) & software (Snort). 
2 Categories ->
a) **Stateful** : Uses the *entire info from a connection* rather than inspecting individual packets. This will determine the behavior of a device *based upon the entire connection.* More resource-intensive but has dynamic decision making. 
Eg : FW could allow the first parts of a TCP handshake that would later fail. If a connection from a host is bad, it will block the entire device.
b) **Stateless** : Uses *static set of rules to determine whether individual packets are acceptable or not.* Less resource-intensive, but also dumber. Great for tackling huge data like DDOS.
Eg : Device sending a bad packet will not necessarily mean that the entire device is blocked. These ones are only effective as the rules that are defined withing them. If a rule is not exactly matched, it is effectively useless.

*VPN Basics*
VPN works on the fundamental principle of making a secured end-to-end comms line via tunneling b/w two devices.
For instance - 2 offices can connect securely and directly via a VPN. Like individually, you can still be a part of your network but also be a part of that VPN to communicate.
VPN allows Networks in different geo-locations to be connected (best for multiple office branches) ; It also offers privacy via encryption & Offers anonymity (blocks your ISP from viewing your traffic).
Tech : 
PPP - used by PPTP, used for auth + encryption. On it's own cannot leave a network (non-routable)
PPTP - Point-to-point Tunneling Protocol - allows data from PPP to travel & leave the network. Easy to set-up + supported by most devices BUT is weakly encrypted.
IPSec - encrypts data using existing IP framework. Difficult to set-up BUT boasts a strong encryption + supported on many devices.

*LAN NW'ing Devices*
a) Router : Connect networks & pass data between them. Done by 'routing'. Operate on Layer-3 i.e Network layer. When many routers are present, the data takes optimal path automatically albeit governed by existing routing protocols.
b) Switch : Dedicated device meant for connecting many devices (3 to 63) via ethernet cables. Operate on both Layer-2 & 3 altho exclusive i.e Layer-2 switch won't operate at Layer-3.
Example -> Layer 2 is very simple. Layer-3 acts as a router as well. How? It segments via VLAN (`VLAN1` via `192.168.1.1` & `VLAN2` via `192.168.2.1`). This still treats them separate and they can still get the actual internet via the router -- altho this N/w segmentation will determine the comms rule for all devices.

Sample Simulation :
2 Machines. PC1 connected to Switch1 which is connected to Router. PC3 connected to Switch2 also connected to Router. 
Sending a packet from PC1 to PC3. First a handshake packet is sent, followed by a SYN packet from PC1 to PC3. PC1 tells ROUTING (Switch1) that PC3 is not on his network, so ROUTING sends an ARP REQ to the router to first identify itself as the Router and then tell where PC3 is. Router tells him that and PC3 receives the SYN packet from PC1, sends back a SYN/ACK packet to PC1. PC1 recevies it and sendds back an ACK packet to PC3. PC3 recevies it from PC1 & handshake is complete. Post which, the TCP packet safely & directly travels from PC1 to PC3. After receiving the packet, PC3 sends an ACK to PC1. For that, another handshake is started b/w PC1 & PC3 -- SYN sent from PC1 to PC3. PC3 receives it and sends SYN/ACK to PC1, who then receives/acknowledges it and sends ACK to PC3. PC3 receives it.

##### **DNS in Detail**
Domain Name System. Converting IP Addr numbers into read-able websites.

*Domain Heirarchy*
Root Domain > Top Level Domain > Second-Level Domain -- Subdomains
TLD : Also 2 sub-types. gTLD (generic = .com, .org, .edu, .online, .club, .biz) & ccTLD (Country code = .ca, .co.uk, .in, .us).
SLD : The domain preceding the TLD is called SLD. Eg : tryhackme.com has TLD as .com and SLD as tryhackme. SLD is limited to 63 chars + TLD can only use a-z 0-9 and hyphens. 
// Sub-domains have the same character limit, but no limit on the number of sub-domains that can be made.

*Record Types*
Many types of DNS records exist. 
`A Record` : For IPv4 : 104.26.10.229
`AAAA Record` : For IPv6
`CNAME Record` : These resolve to another domain name. Example - 'store.tryhackme.com' returns a CNAME record 'shops.shopify.com' which further requires another DNS req for the IP Addr.
`MX Record` : Resolve to addr of the servers that handle the email for the domain you're querying. These records come with a priority flag -- telling the client in which order to try the servers (perfect for switching to backups)
`TXT Record` : Free text fields where any text-based data can be stored. Can have multiple uses but most common is to list servers that have the auth-y to send an email on behalf of the domain, or even verify the ownership of the domain.

*Making a DNS Request*
5 Steps :
1) When you req a domain name, your PC first checks its local cache to see if you've previously looked up the addr recently. False ? A req to your recursive DNS server will be made.
2) A Recursive DNS server is usually provided by your ISP. This also has a local cache of recently looked up domains. If a result is found locally, then sent it back to your PC & your request ends. Else, move on to the Root DNS Server for an answer.
3) The Root servers act as the DNS backbone of the internet -- their job is to redirect you to the correct TLD server (by identifying the parts correctly).
4) TLD Server holds records for where to find the authoritative server (aka NameServer) to answer the DNS req. Eg: NS for tryhackme.com is kip.ns.cloudflare.com. Many NS exists as backups too.
5) Autho-DNS is responsible for storing all DNS records for a particular domain name & is also where any updates to your DNS records would be made. Depending upon the record type, the DNS record is then sent back to the Recursive DNS server, where a local copy will be cached for future requests & then relayed back to the original client that made the request. DNS records come with a TTL value (time to live - unit : seconds) representing how long a response be saved locally before having to look it up again -- caching saves time.

##### **HTTP in Detail**
Set of rules used for communicating with webservers for transmitting webpage data (HTML, images,videos, etc).

*Requests & Responses*
URL is needed first. Has many parts like scheme (http/s), port, fragment, query string, etc.
A req is made via "GET" >  `GET / HTTP/1.1` -- Req Method & Protocol version.
Req has many fields. Firstly the Method (GET), then the 'Host', 'User-Agent', 'Referrer', etc.
Resp would include Protocol version & the Status Code ('200 OK'), also includes Server, Date, Content-Type, Content-Length and then the information requested, which is usually the body.

*HTTP Methods*
GET : getting info from the web-server
POST : submitting data to it -- creating new records
PUT : submitting data to it -- updating some info
DELETE : delete any info/records

*HTTP Status Codes*
(visit https://http.cat for more info)
Range -
100-199 : Info -> not common anymore
200-299 - Success
300-399 - Redirection
400-499 - Client Errors
500-599 - Server side errors
Common Codes -
200 - OK
201 - Created
301 - Permanently moved
302 - Found
400 - Bad Req
401 - Not Authorised (username pw needed)
403 - Forbidden (not allowed, no matter logged in or not)
404 - Not Found
405 - Method not allowed
500 - Internal service error
503 - Service unavailable

*Headers*
Common Req Headers ->
Host, User-Agent, Content-Length, Accept-Encoding, Cookie.
Common Resp Headers ->
Set-Cookie, Cache-Control, Content-Type, Content-Encoding

*Cookies*
Saved when you receive a 'Set-cookie' header. HTTP is stateless, cookies can be used to remind the web-server who you are (+/ your settings). Those settings are sent in the Set-Cookie header with proper key-value. Then from now on, all req will be come back with this cookie data. In case of passwords, they are usually a hashed token.

##### **How Websites Work**
2 parts -> Front-end (the way our browser renders the site)
& Back-end (server that processes the req & returns a resp)

*HTML*
Websites are made using HTML, CSS & JS.
HTML is tags and attribute based.
*JavaScript*
Implemented inside the `<script>` tag usually, this is the dynamic code on a webpage. 
Example : `<script src="/location/of/javascript_file.js"></script>`
OR
`<button onclick='document.getElementById("demo").innerHTML = "Button Clicked";'>Click me!</button>`
//Sensitive Data Exposure happens when a website forgets to remove clear-text sensitive info in the source code -- which is accessible to anyone.

*HTML Injection*
Happens when websites fail to filter any malicious text that a user might input into a website. This way, the attacker can inject malicious HTML code onto the site -- a client side thing.
Input Sanitisation is a necessary practice in this case. 

##### **Web-Stuff Put Together**
The flow : Req website in your browser -> Find web server IP addr with DNS -> Connect to that web-server -> view website.
*Other Components*
1) Load Balancers : A traffic handler when the main web-server is over-loaded. It sits in front of all the web-servers. It ensures high traffic websites can handle the load & providing a failover if server becomes unresponsive. It uses algos like round-robin (sent to each in turn) or weighted (find the least busy one). They can also perform health-checks on all servers.
2) CDNs : Content Delivery Network, useful for cutting down traffic to a busy website. It allows you to host static files from your website (JS, CSS, Img, MP4,..) & host them across many servers all over the world. When a user requests a file, the CDN finds the nearest server & sends the request there instead of anywhere else.
3) Databases : Webservers can communicate with DB to store & recall data from them. DB can range from simple plain-text files to complex clusters. Eg: MySQL, MSSQL, MongoDB, etc.
4) WAF : Web-Application Firewall -- sits b/w the web request & the websever. Its primary purpose is to protect the webserver from any hacking/DDoS attempt. It analyses the web-requests for common attack techniques (bot or real user) + checks for excessive requests by using 'rate-limiting' (certain amount of IPs per second). Sus req are dropped.
*How Web-servers work*
A web-server listens for incoming connections & then utilises HTTP to deliver web-contents to its clients. Common examples include Apache, Nginx, IIS & NodeJS. A web-server always returns the content placed in its root directory. Nginx/Apache use `/var/www/html` in Linux and IIS uses `C:\inetpub\wwwroot` for Windows.

Virtual Hosts : WS can host multiple websites with difft domain names -- so they use VH for this. VH are just text based config files. Example : one.com being mapped to `/var/www/website_one` & two.com being mapped to `/var/www/website_two`.

Static vs Dynamic Content : Static never changes i.e pictures, javascript, CSS, but can also include HTML that never changes. Files are directly served from WS with no changes made.
Dynamic is the opposite. Latest entries, updates on a frequency, search query on a blog, etc. Changes done in the Backend but ofc reflected onto the Frontend.

Scripting & Backend Language : PHP, Python, Ruby, NodeJS, Perl, etc. Superb languages. 

*An example of a full rundown of the steps involved :*
Request website in your browser -> Check local DNS cache for IP Addr -> Check your recursive DNS Server for Addr -> Query root server to find authoritative DNS server -> Authoritative DNS server advises the IP Addr for the website -> Req passes through a WAF -> then req passes through a load balancer -> Connect to the WS on port 80 or 443 -> WS receives a GET req -> Web App talks to the DB -> Finally, your browser renders the HTML into a viewable website.

____________________________________________________________________
____________________________________________________________________
### **Cybersecurity 101** Modules

##### **Windows Command Line**
