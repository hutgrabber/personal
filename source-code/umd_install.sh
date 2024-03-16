#!/bin/bash

# This script builds the midterm VM for ENPM685 on a
# deb package-based system.  

# The general aim is that this will work on multiple Linux distributions
# that use .deb packages, though more testing is needed.

# Please contact kts@umd.edu if you have any updates
# on errors or compatibility issues found.

# Before starting, test sudo with
#	sudo whoami
# If you get an error that you're not allowed to run under sudo, log in as 
# root and edit /etc/group .  Scroll down to the "wheel:..." line and add your 
# username to the end of it (if there are already account names there, put
# a comma between the last name and your account.  Save, log out, log back in
# as yourself, and rerun.

# Tested on: Ubuntu 20.04

install_tools_version="1.1"


fail() {
	# Something failed, exit.
	echo "$@, exiting." >&2
	exit 1
}


require_sudo () {
    # Stops the script if the user does not have root privs and cannot sudo
    # Additionally, sets $SUDO to "sudo" and $SUDO_E to "sudo -E" if needed.

    if [ "$EUID" -eq 0 ]; then
        SUDO=""
        SUDO_E=""
        return 0
    fi

    if sudo -v; then
        SUDO="sudo"
        SUDO_E="sudo -E"
        return 0
    fi
    fail 'Missing administrator privileges. Please run with an account with sudo privileges.'
}


tmp_dir () {
	mkdir -p "$HOME/tmp/"
	tdirname=`mktemp -d -q "$HOME/tmp/install-tools.XXXXXXXX" </dev/null`
	if [ ! -d "$tdirname" ]; then
		fail "Unable to create temporary directory."
	fi
	echo "$tdirname"
}



install_tool() {
	# Install a program.  
	# $1 holds the name of the executable we need
	# $2 is one or more packages that can supply that executable 
	# (put preferred package names early in the list).


	binary="$1"
	echo "Installing package that contains $binary" >&2
	potential_packages="$2"

	if type -path "$binary" >/dev/null ; then
		echo "$binary executable is installed." >&2
	else
		if [ -x /usr/bin/apt-get -a -x /usr/bin/dpkg-query ]; then
			for one_package in $potential_packages ; do
				if ! type -path "$binary" >/dev/null ; then		#if a previous package was successfully able to install, don't try again.
					$SUDO apt-get -q -y install $one_package
				fi
			done
		elif [ -x /usr/bin/yum -a -x /bin/rpm ]; then
			#Yum takes care of the lock loop for us
			for one_package in $potential_packages ; do
				if ! type -path "$binary" >/dev/null ; then		#if a previous package was successfully able to install, don't try again.
					$SUDO yum -y -q -e 0 install $one_package
				fi
			done
		else
			fail "Neither (apt-get and dpkg-query) nor (yum, rpm, and yum-config-manager) is installed on the system"
		fi
	fi

	if type -path "$binary" >/dev/null ; then
		return 0
	else
		echo "WARNING: Unable to install $binary from a system package" >&2
		return 1
	fi
}


# start with an update of apt repos
sudo apt-get update

echo "install_tools version $install_tools_version" >&2

echo "Checking sudo" >&2
require_sudo

install_tool openssh-server "openssh-server"
install_tool realpath "coreutils realpath"
install_tool git "git"
install_tool make "make"
install_tool nc "netcat nc nmap-ncat"
install_tool wget "wget"
install_tool curl "curl"
install_tool apache2 "apache2"
install_tool mysql-server "mysql-server"
install_tool php "php"
install_tool libapache2-mod-php "libapache2-mod-php"
install_tool php-mysql "php-mysql"

echo "====================================" >&2
echo "ENPM685 Midterm VM Setup in Progress" >&2
echo "====================================" >&2

# create mysql users
wget -q --no-check-certificate https://terpconnect.umd.edu/~kts/enpm685/midterm/enpm685_users.sql -O /tmp/enpm685_users.sql
sudo mysql -u root < /tmp/enpm685_users.sql
sudo rm /tmp/enpm685_users.sql
# import mysql content
wget  -q --no-check-certificate https://terpconnect.umd.edu/~kts/enpm685/midterm/n.sql -O /tmp/n.sql
sudo mysql -u root flag3_is_inside < /tmp/n.sql
sudo rm /tmp/n.sql
wget  -q --no-check-certificate https://terpconnect.umd.edu/~kts/enpm685/midterm/m.sql -O /tmp/m.sql
sudo mysql -u root movies < /tmp/m.sql
sudo rm /tmp/m.sql

# download web content
wget -q --no-check-certificate https://terpconnect.umd.edu/~kts/enpm685/midterm/site.tar.gz -O /tmp/site.tar.gz
sudo tar zxf /tmp/site.tar.gz --directory=/ 
sudo chown root:root /var/www/html/*
# remove index.html
sudo rm /var/www/html/index.html
sudo rm /var/www/html/admin-ssh-key.txt
sudo wget -q --no-check-certificate https://terpconnect.umd.edu/~kts/enpm685/midterm/movies.php -O /var/www/html/movies.php

# configure to allow .htaccess to work
sudo wget -q --no-check-certificate https://terpconnect.umd.edu/~kts/enpm685/midterm/apache2.conf -O /etc/apache2/apache2.conf
sudo wget -q --no-check-certificate https://terpconnect.umd.edu/~kts/enpm685/midterm/ports.conf -O /etc/apache2/ports.conf
sudo mkdir /var/www/admin
sudo wget -q --no-check-certificate https://terpconnect.umd.edu/~kts/enpm685/midterm/admin.conf -O /etc/apache2/sites-available/admin.conf
sudo ln -s /etc/apache2/sites-available/admin.conf /etc/apache2/sites-enabled/
sudo wget -q --no-check-certificate https://terpconnect.umd.edu/~kts/enpm685/midterm/admin/index.html -O /var/www/admin/index.html
sudo wget -q --no-check-certificate https://terpconnect.umd.edu/~kts/enpm685/midterm/admin/admin-ssh-key.txt -O /var/www/admin/admin-ssh-key.txt
sudo wget -q --no-check-certificate https://terpconnect.umd.edu/~kts/enpm685/midterm/admin/htaccess -O  /var/www/admin/.htaccess
sudo wget -q --no-check-certificate https://terpconnect.umd.edu/~kts/enpm685/midterm/admin/htpasswd -O  /var/www/admin/.htpasswd


# for good measure
sudo systemctl restart apache2.service

echo "==========================================" >&2
echo "ENPM685 Midterm VM Setup Still in Progress" >&2
echo "==========================================" >&2

sudo echo "admin:x:5002:5002:Adminy McAdminyface,,,:/home/admin:/bin/bash" >> /etc/passwd
sudo echo "bobdobbs:x:5003:5003:Bob Dobbs,,,:/home/bobdobbs:/bin/bash" >> /etc/passwd
sudo echo "crackme:x:5004:5004:Crack My Password For A Flag,,,:/home/crackme:/bin/bash" >> /etc/passwd

sudo echo "admin:\$6\$wbtYxSoc$/0/H4i8EjiQRJ1aN.miaLmNZIWWLeIvqFs5LLt1HmuX2bwI9KaSlqMI/RVZS1vwI5dI8fZfUMsmtQuySiWPDh.:19008:0:99999:7:::" >> /etc/shadow
sudo echo "bobdobbs:\$6\$cM8wEBuo$/eMCFr6HYgaRkWwuZ5A4Q9m88DL1eIj9M5Hr1QnHXf.z9rfMmi/VVWqEf2a8Pz9I8Omo1Te5VuiUsY1pL3wgn1:19008:0:99999:7:::" >> /etc/shadow
sudo echo "crackme:\$6\$Q6c0LZzR\$6OD2scXTTLWqDpdUhTdGRbTAc.gKBDspGnu5KPS6oeFq80XQFCFTZOU3L1mn.VhLsPoCz0veoCoq6uI1Zgzvr.:19039:0:99999:7:::" >> /etc/shadow


sudo echo "admin:x:5002:" >> /etc/group
sudo echo "bobdobbs:x:5003:" >> /etc/group
sudo echo "crackme:x:5004:" >> /etc/group

sudo mkdir /home/admin
sudo chown admin:admin /home/admin
sudo chmod 700 /home/admin
sudo mkdir /home/bobdobbs
sudo chown bobdobbs:bobdobbs /home/bobdobbs
sudo chmod 700 /home/bobdobbs
sudo mkdir /home/crackme
sudo chown crackme:crackme /home/crackme

sudo usermod -aG sudo admin
sudo usermod -aG adm admin

sudo wget -q --no-check-certificate https://terpconnect.umd.edu/~kts/enpm685/midterm/flag1-is-inside.zip -O /home/bobdobbs/flag1-is-inside.zip 
sudo chown bobdobbs:bobdobbs /home/bobdobbs/flag1-is-inside.zip
sudo wget -q --no-check-certificate https://terpconnect.umd.edu/~kts/enpm685/midterm/readme.txt -O /home/bobdobbs/readme.txt 
sudo chown bobdobbs:bobdobbs /home/bobdobbs/readme.txt
sudo wget -q --no-check-certificate https://terpconnect.umd.edu/~kts/enpm685/midterm/flag6-is-inside.zip -O /home/admin/flag6-is-inside.zip 
sudo chown admin:admin /home/admin/flag6-is-inside.zip
sudo wget -q --no-check-certificate https://terpconnect.umd.edu/~kts/enpm685/ssh-key.tar -O /tmp/ssh-key.tar
sudo tar xf /tmp/ssh-key.tar --directory=/home/admin
sudo rm /tmp/ssh-key.tar
sudo chown -R admin:admin /home/admin/.ssh
sudo chmod go-w /home/admin 
sudo chmod 700 /home/admin/.ssh
sudo chmod 600 /home/admin/.ssh/authorized_keys

sudo cp /etc/passwd /home/admin/passwd.bak
sudo cp /etc/shadow /home/admin/shadow.bak
sudo chown admin:admin /home/admin/passwd.bak
sudo chown admin:admin /home/admin/shadow.bak



echo "==========================================" >&2
echo "ENPM685 Midterm VM Configuration Complete!" >&2
echo "==========================================" >&2

rm install.sh
