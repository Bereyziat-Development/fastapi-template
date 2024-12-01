Welcome to the api-template wiki!

# Setup a Linux server

### Create the server

Go to your favorite host service provider ([Ionos](https://ionos.fr), [Infomaniak](https://infomaniak.com)) and create a non managed server (Cloud, dedicated or VPS).

### Connect to the server
Configure your SSH key (public RSA key under ~/.ssh/id_rsa.pub) or save the root access credential for the first connection, then connect to the server as a root user user:
```
ssh root@<server_ip_address>
```
You probably will have to add this new server to the list of known hosts. Just type 'yes' when the command line ask you about this.

### Update the server

Update and upgrade the software on the system:

````
apt update && apt upgrade
````

### Set the hostname

Change the hostname of the server to reflect the use of your brand new server
````
hostnamectl set-hostname <new-server-name>
````

Now set up the hostname in the host file using your favorite text editor (I'm gonna go with nano to keep it simple)
````
nano /etc/hosts
````
In the open file just under the localhost line add your <server_ip_address> then hit the "Tab" key and add your <new-server-name. It should look something like this:

````
127.0.0.1               localhost
<server_ip_address>     <new-server-name>

...
````

### Add a limited user

To avoid using the root user that has unlimited privileges we will have to create a limited user to use as the main account.

````
adduser <username>
````

Now we want to add the user to the sudo group so he can run the admin commands

````
adduser <username> sudo
````

Now that this is done you can log out of the server using "exit" and login with the limited user. 

````
ssh <username>@<server_ip_address>
````
### Setup SSH key authentification

Make a .ssh/ folder and create the authorized_keys file on the server in the user's home directory.
````
mkdir .ssh
touch ~/.ssh/authorized_keys
````
Now let's go back to your local machine. If you don't have generated an ssh key yet you can run and follow the instructions.
````
ssh-keygen -t ed25519 -C "your_email@example.com"
````
Let's secure copy the ssh key on to the server
````
scp ~/.ssh/id_rsa.pub <username>@<server_ip_address>:~/.ssh/authorized_keys
````
Update the permissions of the .ssh directory

````
sudo chmod 700 ~/.ssh/
sudo chmod 600 ~/.ssh/*
````

Now the ssh connection is setup and you should be able to connect to your user on the server without any password.

Make sure that the ssh connection is working before proceeding to next step otherwise you risk to lose access to your server.

We will now deactivate the password authentication to the server
````
sudo nano /etc/ssh/sshd_config
````
And will want to deactivate to set the variables "PermitRootLogin" and "PasswordAuthentication" to "no" in this config file. To make the changes effective restart the SSH servers
````
sudo systemctl restart sshd
````
or 
````
sudo systemctl restart ssh
````

### \[Optional\] Passwordless login

**WARNING**: This is not recommended in production
To make your life easier you may want to navigate across your server without the need of a password. You are already identified by your SSH key so it should be sufficient for non-critical server like a staging server.
To do so you can run the following command:
```
sudo passwd -d <your_user>
```

### Set up a firewall
Install uncomplicated firewall or 'ufw'
````
sudo apt install ufw
````

Set up the rules (depending on your need but this should cover most of normal usages)
````
sudo ufw default allow outgoing
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
````
Apply the rules
````
sudo ufw enable
````
Verify if everything is setup the way you want
````
sudo ufw status
````

# Add your project
Create your target folder, for example:
````
sudo mkdir /var/www
cd /var/www
````

To clone your project, you can use https, in this case you will need a password but in general you will want to setup an ssh connection with your server. To do so you will have to go to the home of your user and create an ssh key. Then add the ssh key of your limited user to your GH account. Depending on your security requirements you may want to consider other approaches with limited access keys for example.



