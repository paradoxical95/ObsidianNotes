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
7 Layers. 