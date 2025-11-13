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

##### **Active Directory**
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
The main idea of organizing users and computers into separate OUs is to have customized Group Policies for each of them. Situated inside the "Group Policy Management" tool, we have the GPO or Group Policy Objects -- they simply are the collection of settings that can be applied to OUs. 
(Policies are created under the GPO section but linked in the general section)