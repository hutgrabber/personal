### Solution

1. performed an NMAP scan and one IP (192.168.192.8) had the port 25 open.
2. interacted with it using `nc -nv $IP 25` and sent the `VRFY root` command to see if I got a reply. 
3. The reply was `255` which means user exists.
