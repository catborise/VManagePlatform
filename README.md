## What is VManagePlatform?
KVM virtualization management platform

**Open Source Agreement**：[GNU General Public License v2](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html)

**Open Source Statement **: Welcome to star or fork my open source project, if you need to refer to the project code in your project, please declare agreement and copyright information in the project
## Development languages and frameworks
* Programming language Python2.7 + HTML + JScripts
* Front-end Web framework：Bootstrap 
* Backend Web framework：Django  
* Backend Task Framework：Celery + Redis

## QQ交流群
![image](https://github.com/welliamcao/OpsManage/blob/master/demo_imgs/qq_group.png)

## What are the features of VManagePlatform ?

* KVM VM 'lifecycle' management functions
    *  Resource utilization (eg: CPU, MEM, disk, network)
    *  Instance control (such as: life cycle management, snapshot technology, Web Console, etc.)
    *  Device resource control (such as: online adjustment of memory, CPU resources, hot add, delete hard disk)
* Storage pool management
    *   Increase or decrease volumes to support mainstream storage types
    *  Resource utilization
* Network Management
    *  SDN is supported, the underlying network uses OpenVSwitch/Linux Bridge, IP address allocation, network card traffic restrictions, and so on.
* User Management
    *  Support user rights, user groups, user virtual machine resource allocation, etc. 
* Host Machine
    *  Resource utilization, instance control

## Environmental requirements:
* Programming language：Python2.7 
* Operating System：CentOS 7 
* Network planning: Management network interface=1, virtualized data network>=1 (if you only need one network card to use OpenVswitch, you need to manually configure the network to avoid losing the network)
* SDN Requirements：OpenVswitch Or Linux Bridge

## TIPS：
* Management Server: Perform 1-10 steps
* Compute Node: Perform 2/3/4 steps and execute ssh-copy-id in Step 5 on the management server
* For a better experience, it is recommended to use Chrome or Firefox browser. If you want to get virtual machine ip, please install qemu-guest-agent in the virtual machine (centos 6 needs to install libvirt>=2.3.0 or more)
* The host list and user center - the data of my virtual machine is updated. Tasks need to be configured in the task schedule.

## Virtual machine add process:
* Step 1: the platform first adds the host (compute node)
* Step 2: adding a data type storage pool and a mirror storage pool
	* Mirrored Storage Pool: The compute node adds a dir type storage pool, puts the ISO image file in the storage pool, or can make the ISO image file an NFS share. When adding a storage pool, select the NFS mode. (Note: In order to add a virtual machine can be loaded into the system image)
	* Data storage pool: According to the page to add, it is mainly used to store virtual machine hard disk.
* Step 3: computing nodes add network, select bridge and nat mode
* Step 4: allocate virtual machines for compute nodes
* Step 5: Configure Task Scheduling to Automatically Update the VM Resource Information of Compute Nodes


## Installation Environment Configuration</br>

1. Configure Platform</br>
```
# yum install zlib zlib-devel readline-devel bzip2-devel openssl-devel gdbm-devel libdbi-devel ncurses-libs kernel-devel libxslt-devel libffi-devel python-devel libvirt libvirt-client libvirt-devel gcc git mysql-devel -y
# mkdir -p /opt/apps/ && cd /opt/apps/
# git clone https://github.com/welliamcao/VManagePlatform.git
# cd VManagePlatform
# pip install -r requirements.txt
```
2. Install KVM
```
A. turn off firewall，selinux
# systemctl stop firewalld.service && systemctl disable firewalld.service
# setenforce 0 (Temporary disabling)
# systemctl stop NetworkManager
# systemctl disable NetworkManager


B. install the kvm virtual machine
# yum install python-virtinst qemu-kvm virt-viewer bridge-utils virt-top libguestfs-tools ca-certificates libxml2-python audit-libs-python device-mapper-libs 
# Start the service
# systemctl start libvirtd
Note: download virtio-win-1.5.2-1.el6.noarch.rpm, if you do not install the window virtual machine or use the image with virtio driver can not be installed
# rpm -ivh virtio-win-1.5.2-1.el6.noarch.rpm

Node server does not have to perform
# yum -y install dnsmasq
# mkdir -p /var/run/dnsmasq/
```

3. Install OpenVswitch (If you use the underlying network using Linux Bridge can not be installed)
```
Install openvswitch
# yum install gcc make python-devel openssl-devel kernel-devel graphviz kernel-debug-devel autoconf automake rpm-build redhat-rpm-config libtool 
# wget http://openvswitch.org/releases/openvswitch-2.3.1.tar.gz
# tar xfz openvswitch-2.3.1.tar.gz
# mkdir -p ~/rpmbuild/SOURCES
# cp openvswitch-2.3.1.tar.gz rpmbuild/SOURCES
# sed 's/openvswitch-kmod, //g' openvswitch-2.3.1/rhel/openvswitch.spec > openvswitch-2.3.1/rhel/openvswitch_no_kmod.spec
# rpmbuild -bb --without check ~/openvswitch-2.3.1/rhel/openvswitch_no_kmod.spec
# yum localinstall /root/rpmbuild/RPMS/x86_64/openvswitch-2.3.1-1.x86_64.rpm
If there is a python dependency error
# vim openvswitch-2.3.1/rhel/openvswitch_no_kmod.spec
BuildRequires: openssl-devel
Then add,
AutoReq: no

# systemctl start openvswitch

```

4. Configure Libvirt use tcp connection
```
# vim /etc/sysconfig/libvirtd
LIBVIRTD_CONFIG=/etc/libvirt/libvirtd.conf
LIBVIRTD_ARGS="--listen"

# vim /etc/libvirt/libvirtd.conf 
listen_tls = 0
listen_tcp = 1
tcp_port = "16509"
listen_addr = "0.0.0.0"
auth_tcp = "none"
# systemctl restart libvirtd 
```
5. Configure SSH trust
```
# ssh-keygen -t  rsa
# ssh-copy-id -i ~/.ssh/id_rsa.pub  root@ipaddress
```

6. Install the database (MySQL, Redis)
```
Install MySQL
# yum install mysql-server mysql-client 
# systemctl start mysqld.service
# mysql -u root -p 
mysql> create database vmanage;
mysql> grant all privileges on vmanage.* to 'username'@'%' identified by 'userpasswd';
mysql>quit

Install Redis
# wget http://download.redis.io/releases/redis-3.2.8.tar.gz
# tar -xzvf redis-3.2.8.tar.gz
# cd redis-3.2.8
# make
# make install
# vim redis.conf
daemonize yes
loglevel warning
logfile "/var/log/redis.log"
bind "Your Server IP address"
# cd ../
# mv redis-3.2.8 /usr/local/redis
# /usr/local/redis/src/redis-server /usr/local/redis/redis.conf
```

7. Configure Django
```
# cd /opt/apps/VManagePlatform/VManagePlatform/
# vim settings.py
7.1、Edit BROKER_URL: change to your own address
7.2、Edit DATABASES：
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME':'vmanage',
        'USER':'Own set account',
        'PASSWORD': 'Own setting password',
        'HOST':'MySQL address'
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
7.3、Edit STATICFILES_DIRS
STATICFILES_DIRS = (
     '/opt/apps/VManagePlatform/VManagePlatform/static/',
    )
TEMPLATE_DIRS = (
#     os.path.join(BASE_DIR,'mysite\templates'),
    '/opt/apps/VManagePlatform/VManagePlatform/templates',
)
```

8. Generate VManagePlatform Data 
```
# cd /opt/apps/VManagePlatform/
# python manage.py migrate
# python manage.py createsuperuser
```
9. Start VManagePlatform
```
# cd /opt/apps/VManagePlatform/
# python manage.py runserver youripaddr:8000
```

10. Configration of Task System
```
# echo_supervisord_conf > /etc/supervisord.conf
# vim /etc/supervisord.conf

[program:celery-worker]
command=/usr/bin/python manage.py celery worker --loglevel=info -E -B  -c 2
directory=/opt/apps/VManagePlatform
stdout_logfile=/var/log/celery-worker.log
autostart=true
autorestart=true
redirect_stderr=true
stopsignal=QUIT
numprocs=1

[program:celery-beat]
command=/usr/bin/python manage.py celery beat
directory=/opt/apps/VManagePlatform
stdout_logfile=/var/log/celery-beat.log
autostart=true
autorestart=true
redirect_stderr=true
stopsignal=QUIT
numprocs=1

[program:celery-cam]
command=/usr/bin/python manage.py celerycam
directory=/opt/apps/VManagePlatform
stdout_logfile=/var/log/celery-celerycam.log
autostart=true
autorestart=true
redirect_stderr=true
stopsignal=QUIT
numprocs=1

Start Celery
# /usr/local/bin/supervisord -c /etc/supervisord.conf
# supervisorctl status
```

## Help

If you feel that VManagePlatform can help you, you can donate in the following ways. Thank you!

![image](https://github.com/welliamcao/OpsManage/blob/master/demo_imgs/donate.png)

## Some function screenshots:
    用户中心
![](https://github.com/welliamcao/VManagePlatform/raw/master/demo_images/user.png)</br>
    User Center
![](https://github.com/welliamcao/VManagePlatform/raw/master/demo_images/login.png)</br>
   User registration requires admin activation to login</br>
![](https://github.com/welliamcao/VManagePlatform/raw/master/demo_images/register.png)</br>
    Homapage
![](https://github.com/welliamcao/VManagePlatform/raw/master/demo_images/index.png)</br>
    Task Scheduling
![](https://github.com/welliamcao/VManagePlatform/raw/master/demo_images/task.png)</br>
    Host Resources</br>
![](https://github.com/welliamcao/VManagePlatform/raw/master/demo_images/server.png)</br>
    Virtual Machine Resources</br>
![](https://github.com/welliamcao/VManagePlatform/raw/master/demo_images/instance.png)</br>
    Web Console</br>
![](https://github.com/welliamcao/VManagePlatform/raw/master/demo_images/consle.png)</br>
