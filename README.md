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
* In the first step, the platform first adds the host (compute node)
* The second step, adding a data type storage pool and a mirror storage pool
	* Mirrored Storage Pool: The compute node adds a dir type storage pool, puts the ISO image file in the storage pool, or can make the ISO image file an NFS share. When adding a storage pool, select the NFS mode. (Note: In order to add a virtual machine can be loaded into the system image)
	* Data storage pool: According to the page to add, it is mainly used to store virtual machine hard disk.
* The third step, computing nodes add network, select bridge and nat mode
* The fourth step is to allocate virtual machines for compute nodes
* Step 5: Configure Task Scheduling to Automatically Update the VM Resource Information of Compute Nodes


## 安装环境配置</br>

一、配置需求模块</br>
```
# yum install zlib zlib-devel readline-devel bzip2-devel openssl-devel gdbm-devel libdbi-devel ncurses-libs kernel-devel libxslt-devel libffi-devel python-devel libvirt libvirt-client libvirt-devel gcc git mysql-devel -y
# mkdir -p /opt/apps/ && cd /opt/apps/
# git clone https://github.com/welliamcao/VManagePlatform.git
# cd VManagePlatform
# pip install -r requirements.txt
```
二、安装kvm
```
1、关闭防火墙，selinux
# systemctl stop firewalld.service && systemctl disable firewalld.service
# setenforce 0 临时关闭
# systemctl stop NetworkManager
# systemctl disable NetworkManager


2、安装kvm虚拟机
# yum install python-virtinst qemu-kvm virt-viewer bridge-utils virt-top libguestfs-tools ca-certificates libxml2-python audit-libs-python device-mapper-libs 
# 启动服务
# systemctl start libvirtd
注：下载virtio-win-1.5.2-1.el6.noarch.rpm，如果不安装window虚拟机或者使用带virtio驱动的镜像可以不用安装
# rpm -ivh virtio-win-1.5.2-1.el6.noarch.rpm

节点服务器不必执行
# yum -y install dnsmasq
# mkdir -p /var/run/dnsmasq/
```

三、安装OpenVswitch（如果使用底层网络使用Linux Bridge可以不必安装）
```
安装openvswitch
# yum install gcc make python-devel openssl-devel kernel-devel graphviz kernel-debug-devel autoconf automake rpm-build redhat-rpm-config libtool 
# wget http://openvswitch.org/releases/openvswitch-2.3.1.tar.gz
# tar xfz openvswitch-2.3.1.tar.gz
# mkdir -p ~/rpmbuild/SOURCES
# cp openvswitch-2.3.1.tar.gz rpmbuild/SOURCES
# sed 's/openvswitch-kmod, //g' openvswitch-2.3.1/rhel/openvswitch.spec > openvswitch-2.3.1/rhel/openvswitch_no_kmod.spec
# rpmbuild -bb --without check ~/openvswitch-2.3.1/rhel/openvswitch_no_kmod.spec
# yum localinstall /root/rpmbuild/RPMS/x86_64/openvswitch-2.3.1-1.x86_64.rpm
如果出现python依赖错误
# vim openvswitch-2.3.1/rhel/openvswitch_no_kmod.spec
BuildRequires: openssl-devel
后面添加
AutoReq: no

# systemctl start openvswitch

```

四、配置Libvirt使用tcp方式连接
```
# vim /etc/sysconfig/libvirtd
LIBVIRTD_CONFIG=/etc/libvirt/libvirtd.conf
LIBVIRTD_ARGS="--listen"

# vim /etc/libvirt/libvirtd.conf  #最后添加
listen_tls = 0
listen_tcp = 1
tcp_port = "16509"
listen_addr = "0.0.0.0"
auth_tcp = "none"
# systemctl restart libvirtd 
```
五、配置SSH信任
```
# ssh-keygen -t  rsa
# ssh-copy-id -i ~/.ssh/id_rsa.pub  root@ipaddress
```

六、安装数据库(MySQL,Redis)
```
安装配置MySQL
# yum install mysql-server mysql-client 
# systemctl start mysqld.service
# mysql -u root -p 
mysql> create database vmanage;
mysql> grant all privileges on vmanage.* to 'username'@'%' identified by 'userpasswd';
mysql>quit

安装配置Redis
# wget http://download.redis.io/releases/redis-3.2.8.tar.gz
# tar -xzvf redis-3.2.8.tar.gz
# cd redis-3.2.8
# make
# make install
# vim redis.conf
daemonize yes
loglevel warning
logfile "/var/log/redis.log"
bind 你的服务器ip地址
# cd ../
# mv redis-3.2.8 /usr/local/redis
# /usr/local/redis/src/redis-server /usr/local/redis/redis.conf
```

七、配置Django
```
# cd /opt/apps/VManagePlatform/VManagePlatform/
# vim settings.py
7.1、修改BROKER_URL：改为自己的地址
7.2、修改DATABASES：
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',
        'NAME':'vmanage',
        'USER':'自己的设置的账户',
        'PASSWORD':'自己的设置的密码',
        'HOST':'MySQL地址'
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
7.3、修改STATICFILES_DIRS
STATICFILES_DIRS = (
     '/opt/apps/VManagePlatform/VManagePlatform/static/',
    )
TEMPLATE_DIRS = (
#     os.path.join(BASE_DIR,'mysite\templates'),
    '/opt/apps/VManagePlatform/VManagePlatform/templates',
)
```

八、生成VManagePlatform数据表
```
# cd /opt/apps/VManagePlatform/
# python manage.py migrate
# python manage.py createsuperuser
```
九、启动VManagePlatform
```
# cd /opt/apps/VManagePlatform/
# python manage.py runserver youripaddr:8000
```

十、配置任务系统
```
# echo_supervisord_conf > /etc/supervisord.conf
# vim /etc/supervisord.conf
最后添加
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

启动celery
# /usr/local/bin/supervisord -c /etc/supervisord.conf
# supervisorctl status
```

## 提供帮助

如果您觉得VManagePlatform对您有所帮助，可以通过下列方式进行捐赠，谢谢！

![image](https://github.com/welliamcao/OpsManage/blob/master/demo_imgs/donate.png)

## 部分功能截图:
    用户中心
![](https://github.com/welliamcao/VManagePlatform/raw/master/demo_images/user.png)</br>
    登录页面
![](https://github.com/welliamcao/VManagePlatform/raw/master/demo_images/login.png)</br>
    用户注册需要admin激活才能登陆</br>
![](https://github.com/welliamcao/VManagePlatform/raw/master/demo_images/register.png)</br>
    主页
![](https://github.com/welliamcao/VManagePlatform/raw/master/demo_images/index.png)</br>
    任务调度
![](https://github.com/welliamcao/VManagePlatform/raw/master/demo_images/task.png)</br>
    宿主机资源</br>
![](https://github.com/welliamcao/VManagePlatform/raw/master/demo_images/server.png)</br>
    虚拟机资源</br>
![](https://github.com/welliamcao/VManagePlatform/raw/master/demo_images/instance.png)</br>
    Web Console</br>
![](https://github.com/welliamcao/VManagePlatform/raw/master/demo_images/consle.png)</br>
