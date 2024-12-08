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


# Deploy your stack
This is an example of how to quickly deploy your project. Keep in mind to challenge this configuration bases on your project scale and requirements.

## Setup your project

Set the hostname of your server
````
export USE_HOSTNAME=service.lestario.com
echo $USE_HOSTNAME > /etc/hostname
hostname -F /etc/hostname
````

Download and install docker
````
curl -fsSL get.docker.com -o get-docker.sh
CHANNEL=stable sh get-docker.sh
rm get-docker.sh
````

Download and install docker-compose
WARNING: This download channel should be pretty up to date but don't hesitate to refer to the official docker compose documentation
````
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
source ~/.profile
docker-compose --version
````

Init the docker swarm
````
docker swarm init
docker node ls
````

WARNING: Depending on your server configuration you may need to assign the ip address manual using this command instead
````
docker swarm init --advertise-addr <YOUR_IP_ADDRESS>
````

Create the traefik public network
````
docker network create --driver=overlay traefik-public
````

Export those env vars 
````
export TAG=stag
export ENV_CONFIG=stag
export DOMAIN=yourdomain.com
export TRAEFIK_TAG=yourdomain.com
export STACK_NAME=yourdomain-com
````

WARNING: Depending on your project requirements you may want to avoid setting secret data using .env or variable export. A more production ready solution would be to use a secret manager.

IMPORTANT: Don't forget to add your project .env file. You will have to do this manually or via scp since the .env is not in the base repo

**Deploy your stack in one line**
````
bash scripts/deploy.sh
````


# Update your stack
Get the latest version of you repo
````
sudo git pull
````

Set the env vars:
````
export TAG=stag
export ENV_CONFIG=stag
export DOMAIN=yourdomain.com
export TRAEFIK_TAG=yourdomain.com
export STACK_NAME=yourdomain-com
````
Rebuild and deploy your project using the deploy.sh script. To make sure your changes are propagated to your website make sure to restart your backend container.
````
bash scripts/deploy.sh

docker service update --force your-stack-name_backend -d
````

You can now check the logs of your app and grab a coffee ☕️ while watching request popping in:
````
docker ps
docker logs <backend-container-id> -f
````

# How to completely delete my stack?
````
docker stack rm service-lestario-api
docker swarm leave --force
````

Remove containers and images of your project
````
docker rm -f $(docker ps -a -q)
docker volume rm $(docker volume ls -q)
````


You can also remove all the docker data with:
````
docker system prune
````