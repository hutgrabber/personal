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

* Enumerating the FTP server 

## Exploitation